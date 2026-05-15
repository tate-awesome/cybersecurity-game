// Version 16 Client
// Removed delay(3) from readH and writeH
// Calculated dt value instead of fixed value
// Trying to use batch pose function to send x,y,theta all in one packet

#include <Arduino.h>
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

#ifndef PI
#define PI 3.14159265358979323846f
#endif

//// ---------- WiFi ----------
const char* ssid = "GL-SFT1200-ab1";
const char* password = "goodlife";
IPAddress serverIP(192, 168, 8, 137);  // <-- Slave IP

ModbusIP mb;

// Local pose state (Master-side)
float state_x = 0.0f;     // meters, initial position
float state_y = 0.0f;     // meters
float state_theta = 0.0f; // radians (start facing East)

// dynamics params (MUST match MATLAB)
const float L_vehicle = 0.07f;  // Vehicle length (meters)
const float K_theta = 0.6f;     // Coefficient from MATLAB thetadot formula
unsigned long lastUpdateMs = 0;

// Modbus register IDs on Slave
const uint16_t HREG_X_PHYS = 10;
const uint16_t HREG_Y_PHYS = 11;
const uint16_t HREG_THETA_MRAD = 12;

const uint16_t HREG_SPEED = 3;
const uint16_t HREG_RUDDER = 4;

//// ---------- Physical scaling constants ----------
const float SpeedMax_m_s = 50.0f;    // max physical speed (m/s)
const float RudderMax_deg = 60.0f;   // max rudder deflection (±60°)

//// ---------- Conversion Helpers ----------
static inline uint16_t x_to_u16_100(float v) {
  if (v < 0) v = 0;
  if (v > 200) v = 200;
  return (uint16_t)lroundf(v * 100.0f);
}

static inline uint16_t theta_to_mrad_u16(float t) {
  // Keep theta in 0 to 2*PI range
  while (t < 0) t += 2.0f * PI;
  while (t >= 2.0f * PI) t -= 2.0f * PI;
  return (uint16_t)lroundf(t * 1000.0f);
}

bool writeH(uint16_t addr, uint16_t val) {
  if (!mb.isConnected(serverIP)) return false;
  uint16_t tx = mb.writeHreg(serverIP, addr, val);
  if (!tx) return false;
  for (int i = 0; i < 12; i++) {
    mb.task();
  }
  return true;
}

bool readH(uint16_t addr, uint16_t* buf, uint16_t n) {
  if (!mb.isConnected(serverIP)) return false;
  uint16_t tx = mb.readHreg(serverIP, addr, buf, n);
  if (!tx) return false;
  for (int i = 0; i < 16; i++) {
    mb.task();
  }
  return true;
}

//// ---------- Send X/Y/Theta to Slave ----------
// void sendPose() {
//   uint16_t x_u = x_to_u16_100(state_x);
//   uint16_t y_u = x_to_u16_100(state_y);
//   uint16_t t_u = theta_to_mrad_u16(state_theta);

//   if (writeH(HREG_X_PHYS, x_u) && writeH(HREG_Y_PHYS, y_u) && writeH(HREG_THETA_MRAD, t_u)) {
//     // Success - values sent
//   } else {
//     Serial.println("[MASTER] ERR: Failed to send pose to Slave");
//   }
// }

void sendPoseBatch() {
    if (!mb.isConnected(serverIP)) return;

    uint16_t poseData[3];
    poseData[0] = (uint16_t)lroundf(constrain(state_x, 0, 200) * 100.0f);
    poseData[1] = (uint16_t)lroundf(constrain(state_y, 0, 200) * 100.0f);
    
    // Normalize and convert Theta
    float t = state_theta;
    while (t < 0) t += 2.0f * PI;
    while (t >= 2.0f * PI) t -= 2.0f * PI;
    poseData[2] = (uint16_t)lroundf(t * 1000.0f);

    // Send all 3 registers in ONE packet
    mb.writeHreg(serverIP, 10, poseData, 3);
}

//// ---------- Setup ----------
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n[MASTER] Booting…");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  Serial.print("[MASTER] Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.printf("\n[MASTER] IP: %s\n", WiFi.localIP().toString().c_str());

  
  Serial.println("[MASTER] WiFi sleep disabled");

  mb.connect(serverIP);
  delay(500);

  if (mb.isConnected(serverIP)) {
    Serial.println("[MASTER] Connected to Slave Modbus server.");
    // Send initial pose
    sendPoseBatch();
    Serial.println("[MASTER] Initial pose sent to Slave.");
  } else {
    Serial.println("[MASTER] WARNING: Could not connect to Slave initially.");
  }
}


void loop() {
  mb.task();
  yield();

  if (!mb.isConnected(serverIP)) {
    static uint32_t lastConnectTry = 0;
    if (millis() - lastConnectTry > 2000) {
      lastConnectTry = millis();
      Serial.println("[MASTER] Link Lost. Reconnecting...");
      mb.connect(serverIP);
    }
    return;
  }

  static uint32_t lastUpdateMs = 0;
  if (millis() - lastUpdateMs >= 50) { 
    uint32_t currentMs = millis();
    float dt = (currentMs - lastUpdateMs) / 1000.0f; 
    lastUpdateMs = currentMs;

    uint16_t feedback[2];
    if (mb.readHreg(serverIP, HREG_SPEED, feedback, 2)) {
      
      float speed_m_s = (feedback[0] / 4095.0f) * SpeedMax_m_s;
      float rudder_deg = ((feedback[1] / 4095.0f) - 0.5f) * 2.0f * RudderMax_deg;

      if (fabs(speed_m_s) > 0.01f) {
        float v = speed_m_s;
        float rho = radians(rudder_deg);
        
        float xdot = v * cos(rho + state_theta);
        float ydot = v * sin(rho + state_theta);
        float thetadot = 0.0f;
        
        if (fabs(rho) > 0.001f) {
          // thetadot = (v / R) where R = L / tan(rho)
          thetadot = (K_theta * v) / (L_vehicle / tan(rho));
        }

        // Euler integration
        state_x += xdot * dt;
        state_y += ydot * dt;
        state_theta += thetadot * dt;

        state_x = constrain(state_x, 0.0f, 200.0f);
        state_y = constrain(state_y, 0.0f, 200.0f);
        
        while (state_theta < 0) state_theta += 2.0f * PI;
        while (state_theta >= 2.0f * PI) state_theta -= 2.0f * PI;
      }

      // We package X, Y, and Theta into one array to send in one TCP packet
      uint16_t poseData[3];
      poseData[0] = (uint16_t)lroundf(state_x * 100.0f);     // HREG 10
      poseData[1] = (uint16_t)lroundf(state_y * 100.0f);     // HREG 11
      poseData[2] = (uint16_t)lroundf(state_theta * 1000.0f);// HREG 12

      mb.task();


      if (!mb.writeHreg(serverIP, HREG_X_PHYS, poseData, 3)) {
        static uint32_t lastErrPrint = 0;
        if (millis() - lastErrPrint > 1000) { // Log error max once per second
            Serial.println("[MASTER] ERR: Pose Batch Write Failed (Stack Busy)");
            lastErrPrint = millis();
        }
        // Serial.println("[MASTER] ERR: Pose Batch Write Failed");
      }

      static uint32_t lastPrint = 0;
      if (millis() - lastPrint > 1000) {
        lastPrint = millis();
        Serial.printf("[MASTER] V:%.2fm/s R:%.1fdeg | x=%.3f m y=%.3f m theta=%.4f\n", 
                      speed_m_s, rudder_deg, state_x, state_y, state_theta);
      }
    }
  }
  delay(1); 
}