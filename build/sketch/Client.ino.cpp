#line 1 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
#define REST_API_ENABLED  // Comment out to disable REST API
//#define DEBUG_SERIAL      // Comment out to disable debug output

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ModbusIP_ESP8266.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>  // Frank de Brabander

#ifndef PI
#define PI 3.14159265358979323846f
#endif

#ifdef REST_API_ENABLED
  #include <HTTPClient.h>
  #include <ArduinoJson.h>
  const char* REST_URL = "http://192.168.8.114:5000/data";
  const uint32_t REST_INTERVAL_MS = 2000;
  static uint32_t lastRestMs = 0;
  static bool encrypt_status = false;
#endif

#ifdef DEBUG_SERIAL
  #define DBG_PRINT(...)  Serial.print(__VA_ARGS__)
  #define DBG_PRINTLN(...) Serial.println(__VA_ARGS__)
  #define DBG_PRINTF(...) Serial.printf(__VA_ARGS__)
#else
  #define DBG_PRINT(...)
  #define DBG_PRINTLN(...)
  #define DBG_PRINTF(...)
#endif

LiquidCrystal_I2C lcd(0x27, 16, 2);

const char* ssid = "GL-SFT1200-ab1";
const char* password = "goodlife";
IPAddress serverIP(192, 168, 8, 137);

ModbusIP mb;

float state_x = 0.0f;
float state_y = 0.0f;
float state_theta = 0.0f; // radians (start facing East)
float state_speed  = 0.0f;
float state_rudder = 0.0f;


const float L_vehicle = 0.07f;
const float K_theta = 0.6f;
unsigned long lastUpdateMs = 0;

const uint16_t HREG_X_PHYS = 10;
const uint16_t HREG_Y_PHYS = 11;
const uint16_t HREG_THETA_MRAD = 12;

const uint16_t HREG_SPEED = 3;
const uint16_t HREG_RUDDER = 4;

static int readAttempts = 0;
static int readFailures = 0;

//// ---------- Physical scaling constants ----------
const float SpeedMax_m_s = 50.0f;    // max physical speed (m/s)
const float RudderMax_deg = 60.0f;   // max rudder deflection (±60°)

//// ---------- Conversion Helpers ----------
#line 69 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
static uint16_t x_to_u16_100(float v);
#line 75 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
static uint16_t theta_to_mrad_u16(float t);
#line 83 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
bool writeH(uint16_t addr, uint16_t val);
#line 108 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
bool readH(uint16_t addr, uint16_t* buf, uint16_t n);
#line 134 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
void sendPose();
#line 147 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
void restPost();
#line 188 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
void setup();
#line 264 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
void loop();
#line 69 "/home/martin/Desktop/cybersecurity-game/Version 17/Client/Client.ino"
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
  if (!mb.isConnected(serverIP)) {
    DBG_PRINTF("[MASTER] writeH FAIL addr=%u: not connected\n", addr);
    return false;
  }
  // One retry on timeout to handle occasional WiFi jitter
  for (int attempt = 0; attempt < 2; attempt++) {
    uint16_t tx = mb.writeHreg(serverIP, addr, val);
    if (!tx) {
      DBG_PRINTF("[MASTER] writeH FAIL addr=%u: writeHreg returned 0 (queue full or busy)\n", addr);
      return false;  // retrying won't help so exit immediately.
    }
    // Poll until the transaction clears, up to a hard timeout of 300ms.
    uint32_t start = millis();
    while (millis() - start < 300) {
      mb.task();
      if (!mb.isTransaction(tx)) return true;
      delay(3);
    }
    DBG_PRINTF("[MASTER] writeH addr=%u: transaction timed out (attempt %d/2)\n", addr, attempt + 1);
    for (int i = 0; i < 5; i++) { mb.task(); delay(5); }
  }
  return false;
}

bool readH(uint16_t addr, uint16_t* buf, uint16_t n) {
  if (!mb.isConnected(serverIP)) {
    DBG_PRINTLN("[MASTER] readH FAIL: not connected");
    return false;
  }
  // 1 retry on timeout to handle occasional WiFi jitter
  for (int attempt = 0; attempt < 2; attempt++) {
    uint16_t tx = mb.readHreg(serverIP, addr, buf, n);
    if (!tx) {
      DBG_PRINTLN("[MASTER] readH FAIL: readHreg returned 0 (queue full or busy)");
      return false;  // retrying won't help so bail immediately.
    }
    // Poll until the transaction clears, up to a hard timeout of 300ms.
    uint32_t start = millis();
    while (millis() - start < 300) {
      mb.task();
      if (!mb.isTransaction(tx)) return true;
      delay(3);
    }
    DBG_PRINTF("[MASTER] readH FAIL: transaction timed out (attempt %d/2)\n", attempt + 1);
    for (int i = 0; i < 5; i++) { mb.task(); delay(5); }
  }
  return false;
}

//// ---------- Send X/Y/Theta to Slave ----------
void sendPose() {
  uint16_t x_u = x_to_u16_100(state_x);
  uint16_t y_u = x_to_u16_100(state_y);
  uint16_t t_u = theta_to_mrad_u16(state_theta);

  if (writeH(HREG_X_PHYS, x_u) && writeH(HREG_Y_PHYS, y_u) && writeH(HREG_THETA_MRAD, t_u)) {
    // Success - values sent
  } else {
    Serial.println("[MASTER] ERR: Failed to send pose to Slave");
  }
}

#ifdef REST_API_ENABLED
void restPost() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(REST_URL);
  http.addHeader("Content-Type", "application/json");

  // Build payload
  StaticJsonDocument<128> doc;
  doc["timestamp"] = (uint32_t)(millis() / 1000);
  doc["x"]         = state_x;
  doc["y"]         = state_y;
  doc["theta"]     = state_theta;
  doc["speed"]     = state_speed;
  doc["rudder"]    = state_rudder;

  String payload;
  serializeJson(doc, payload);

  int code = http.POST(payload);

  if (code == 200) {
    String body = http.getString();

    StaticJsonDocument<64> resp;
    if (!deserializeJson(resp, body)) {
      if (resp.containsKey("encryption_status")) {
        encrypt_status = resp["encryption_status"].as<bool>();
        String key = resp["encryption_key"].as<String>();
        // Serial.printf("[MASTER] encryption_key=%s\n", key.c_str());
      }
    }
  } else {
    Serial.printf("[MASTER] REST POST failed  HTTP %d\n", code);
  }

  http.end();
}
#endif

//// ---------- Setup ----------
void setup() {
  Serial.begin(115200);
  delay(50);
  Serial.println("\n[MASTER] Booting…");

  // Initialize LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Master Init...");

  // WiFi
  lcd.setCursor(0, 1);
  lcd.print("WiFi connect...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("[MASTER] Connecting to WiFi");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(300);
    Serial.print(".");
    attempts++;
  }

  lcd.clear();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\n[MASTER] IP: %s\n", WiFi.localIP().toString().c_str());
    lcd.setCursor(0, 0);
    lcd.print("WiFi: OK");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
    delay(2000);
  } else {
    lcd.setCursor(0, 0);
    lcd.print("WiFi: FAILED!");
    Serial.println("\n[MASTER] WiFi failed!");
    while(1) { delay(1000); }
  }

  WiFi.setSleep(false);
  Serial.println("[MASTER] WiFi sleep disabled");

  // Connect to Slave
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connect Slave...");
  mb.connect(serverIP);
  delay(500);

  if (mb.isConnected(serverIP)) {
    Serial.println("[MASTER] Connected to Slave Modbus server.");
    lcd.setCursor(0, 1);
    lcd.print("Slave: OK");
    delay(1000);
    
    // Send initial pose
    sendPose();
    Serial.println("[MASTER] Initial pose sent to Slave.");
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Feedback Loop:");
    lcd.setCursor(0, 1);
    lcd.print("Starting...");
    delay(1000);
  } else {
    Serial.println("[MASTER] WARNING: Could not connect to Slave initially.");
    lcd.setCursor(0, 1);
    lcd.print("Slave: FAIL");
    delay(2000);
  }
}

//// ---------- Loop ----------
void loop() {
  mb.task();
  yield();

  // Reconnect if disconnected
  if (!mb.isConnected(serverIP)) {
    static uint32_t lastTry = 0;
    if (millis() - lastTry > 2000) {
      lastTry = millis();
      Serial.println("[MASTER] Reconnecting Modbus…");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Reconnecting...");
      
      mb.connect(serverIP);
      if (mb.isConnected(serverIP)) {
        Serial.println("[MASTER] Reconnected successfully!");
        sendPose();
      }
    }
    delay(10);
    return;
  }

  // Read feedback and update pose
  static uint32_t lastReadS = 0;
  static uint32_t lastPoseMs = 0;
  if (millis() - lastReadS >= 50) {  // Update at ~20Hz
    uint32_t currentMs = millis();
    lastReadS = currentMs;
    float dt = 0.05f;

    uint16_t rb[2];
    readAttempts++;
    if (readH(HREG_SPEED, rb, 2)) {
      uint16_t speed_counts = rb[0];
      uint16_t rudder_counts = rb[1];

      // Convert counts to physical units
      float speed_m_s = (speed_counts / 4095.0f) * SpeedMax_m_s;
      float rudder_deg = ((rudder_counts / 4095.0f) - 0.5f) * 2.0f * RudderMax_deg;
      state_speed  = speed_m_s;
      state_rudder  = rudder_deg;

      // Only integrate if there's meaningful motion
      if (fabs(speed_m_s) > 0.01f) {
        float v = speed_m_s;
        float rho = radians(rudder_deg);
        
        // MATLAB-style kinematic update
        float xdot = v * cos(rho + state_theta);
        float ydot = v * sin(rho + state_theta);
        float thetadot = 0.0f;
        
        // Only turn if rudder is not centered
        if (fabs(rho) > 0.001f) {
          thetadot = K_theta / (L_vehicle / tan(rho));
        }

        state_x += xdot * dt;
        state_y += ydot * dt;
        state_theta += thetadot * dt;

        // Normalize theta to [0, 2*PI]
        while (state_theta < 0) state_theta += 2.0f * PI;
        while (state_theta >= 2.0f * PI) state_theta -= 2.0f * PI;

        // Clamp X, Y to valid range
        if (state_x < 0.0f) state_x = 0.0f;
        if (state_x > 200.0f) state_x = 200.0f;
        if (state_y < 0.0f) state_y = 0.0f;
        if (state_y > 200.0f) state_y = 200.0f;
      }

      // Send updated pose back to Slave
      if (millis() - lastPoseMs >= 200) {
        lastPoseMs = millis();
        sendPose();
      }

      // Update LCD every 500ms
      static uint32_t lastLcdUpdate = 0;
      if (millis() - lastLcdUpdate > 500) {
        lastLcdUpdate = millis();
        
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("X:");
        lcd.print((int)state_x);
        lcd.print(" Y:");
        lcd.print((int)state_y);
        lcd.print(" S:");
        lcd.print(speed_counts);
        
        lcd.setCursor(0, 1);
        lcd.print("H:");
        lcd.print((int)(state_theta * 57.3));
        lcd.print((char)223);  // degree symbol
        lcd.print(" R:");
        lcd.print(rudder_counts);
      }

      // Print diagnostics every second
      static uint32_t lastPrint = 0;
      if (millis() - lastPrint > 1000) {
        lastPrint = millis();

        Serial.printf("[MASTER] RECV  Speed = %.3f m/s  |  Rudder = %.2f deg  (raw: %u, %u)\n",
                      speed_m_s, rudder_deg, speed_counts, rudder_counts);
        Serial.printf("[MASTER] POS   x=%.3f m  y=%.3f m  theta=%.4f rad (deg=%.2f)"
          #ifdef REST_API_ENABLED
                        " e_stat=%d"
          #endif
                        "\n",
                        state_x, state_y, state_theta, degrees(state_theta)
          #ifdef REST_API_ENABLED
                        , encrypt_status
          #endif
          );
      }

    } else {
      readFailures++;
      DBG_PRINTF("[MASTER] ERR  read feedback failed (%d/%d failures)\n", readFailures, readAttempts);
      
      static uint32_t lastErrLcd = 0;
      if (millis() - lastErrLcd > 2000) {
        lastErrLcd = millis();
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Feedback Loop:");
        lcd.setCursor(0, 1);
        lcd.print("Read FAIL!");
      }
    }
  }

  #ifdef REST_API_ENABLED
    if (millis() - lastRestMs >= REST_INTERVAL_MS) {
      lastRestMs = millis();
      restPost();
    }
  #endif
  delay(5);
}
