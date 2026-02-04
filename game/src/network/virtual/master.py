from math import pi as PI

class Master:

    def __init__(self):
# // Version 15 MASTER (Corrected Kinematics to Match MATLAB)
# // - Set dt to be fixed at value
# // - Removed the deadband logic

#include <Arduino.h>
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

#ifndef PI
#define PI 3.14159265358979323846f
#endif

# //// ---------- WiFi ----------
# const char* ssid = "GL-SFT1200-ab1";
# const char* password = "goodlife";
# IPAddress serverIP(192, 168, 8, 137);  // <-- Slave IP

# ModbusIP mb;

# // Local pose state (Master-side)
# float state_x = 0.0f;     // meters, initial position (match MATLAB: starts at origin)
# float state_y = 0.0f;     // meters
# float state_theta = 0.0f; // radians (start facing East, matching MATLAB initial condition)
        self.state_x = 0.0
        self.state_y = 0.0
        self.state_theta = 0.0
# // dynamics params (MUST match MATLAB)
# const float L_vehicle = 0.07f;  // FIXED: L = 0.07 from MATLAB (not 20.0!)
# const float K_theta = 0.6f;     // FIXED: coefficient from MATLAB thetadot formula
# unsigned long lastUpdateMs = 0;
        self.L_vehicle = 0.07
        self.K_theta = 0.6
        self.last_update_ms = 0

# // Modbus register IDs on Slave (from your spec)
# const uint16_t HREG_X_PHYS = 10;
# const uint16_t HREG_Y_PHYS = 11;
# const uint16_t HREG_THETA_MRAD = 12;
        self.HREG_X_PHYS = 10
        self.HREG_Y_PHYS = 11
        self.HREG_THETA_MRAD = 12

# const uint16_t HREG_SPEED = 3;
# const uint16_t HREG_RUDDER = 4;
        self.HTREG_SPEED = 3
        self.HREG_RUDDER = 4

# //// ---------- Physical scaling constants ----------
# const float SpeedMax_m_s = 50.0f;    // max physical speed (m/s) - matches Slave & MATLAB
# const float RudderMax_deg = 60.0f;   // max rudder deflection (±60°) - matches Slave & MATLAB
        self.SpeedMax_m_s = 50.0
        self.RudderMax_deg = 60.0
# const float SPEED_DEADBAND_M_S = 0.5f;  // Reduced deadband
# const float RUDDER_DEADBAND_DEG = 1.0f; // Reduced deadband
        const self.SPEED_DEADBAND_M_S = 0.5
        const self.RUDDER_DEADBAND_DEG = 1.0
# //// ---------- Conversion Helpers ----------
# static inline uint16_t x_to_u16_100(float v) {
#   if (v < 0) v = 0;
#   if (v > 200) v = 200;
#   return (uint16_t)lroundf(v * 100.0f);
# }
        def x_to_int(x):
            if x < 0:
                x = 0
            if x > 200:
                x = 200
            return round(x * 100.0)

# static inline uint16_t theta_to_mrad_u16(float t) {
#   // Keep theta in 0 to 2*PI range (matching PLC/Slave expectation)
#   while (t < 0) t += 2.0f * PI;
#   while (t >= 2.0f * PI) t -= 2.0f * PI;
#   return (uint16_t)lroundf(t * 1000.0f);
# }
        def theta_to_mrad_int(t):
            while t < 0:
                t += 2.0 * PI
            while t >= 2.0 * PI:
                t -= 2.0 * PI
            return round(t * 1000.0)

# bool writeH(uint16_t addr, uint16_t val) {
#   if (!mb.isConnected(serverIP)) return false;
#   uint16_t tx = mb.writeHreg(serverIP, addr, val);
#   if (!tx) return false;
#   for (int i = 0; i < 12; i++) {
#     mb.task();
#     delay(3);
#   }
#   return true;
# }
        def writeH(self, addr, val):

# bool readH(uint16_t addr, uint16_t* buf, uint16_t n) {
#   if (!mb.isConnected(serverIP)) return false;
#   uint16_t tx = mb.readHreg(serverIP, addr, buf, n);
#   if (!tx) return false;
#   for (int i = 0; i < 16; i++) {
#     mb.task();
#     delay(3);
#   }
#   return true;
# }

# //// ---------- Send X/Y/Theta to Slave ----------
# void sendPose() {
#   uint16_t x_u = x_to_u16_100(state_x);
#   uint16_t y_u = x_to_u16_100(state_y);
#   uint16_t t_u = theta_to_mrad_u16(state_theta);

#   if (writeH(HREG_X_PHYS, x_u) && writeH(HREG_Y_PHYS, y_u) && writeH(HREG_THETA_MRAD, t_u)) {
#     // Success - values sent
#   } else {
#     Serial.println("[MASTER] ERR: Failed to send pose to Slave");
#   }
# }

# //// ---------- Setup ----------
# void setup() {
#   Serial.begin(115200);
#   delay(50);
#   Serial.println("\n[MASTER] Booting…");

#   WiFi.mode(WIFI_STA);
#   WiFi.begin(ssid, password);
#   Serial.print("[MASTER] Connecting to WiFi");
#   while (WiFi.status() != WL_CONNECTED) {
#     delay(300);
#     Serial.print(".");
#   }
#   Serial.printf("\n[MASTER] IP: %s\n", WiFi.localIP().toString().c_str());

#   WiFi.setSleep(false);
#   Serial.println("[MASTER] WiFi sleep disabled");

#   mb.connect(serverIP);
#   delay(500);

#   if (mb.isConnected(serverIP)) {
#     Serial.println("[MASTER] Connected to Slave Modbus server.");
#     // Send initial pose
#     sendPose();
#     Serial.println("[MASTER] Initial pose sent to Slave.");
#   } else {
#     Serial.println("[MASTER] WARNING: Could not connect to Slave initially.");
#   }
# }

# //// ---------- Loop ----------
# void loop() {
#   mb.task();
#   yield();

#   // Reconnect if disconnected
#   if (!mb.isConnected(serverIP)) {
#     static uint32_t lastTry = 0;
#     if (millis() - lastTry > 2000) {
#       lastTry = millis();
#       Serial.println("[MASTER] Reconnecting Modbus…");
#       mb.connect(serverIP);
#       if (mb.isConnected(serverIP)) {
#         Serial.println("[MASTER] Reconnected successfully!");
#         sendPose();
#       }
#     }
#     delay(10);
#     return;
#   }

#   // Read feedback and update pose
#   static uint32_t lastRead = 0;
#   if (millis() - lastRead > 50) {  // Update at ~20Hz
#     lastRead = millis();

#     uint16_t rb[2];
#     if (readH(HREG_SPEED, rb, 2)) {
#       uint16_t speed_counts = rb[0];
#       uint16_t rudder_counts = rb[1];

#       // Convert counts to physical units
#       float speed_m_s = (speed_counts / 4095.0f) * SpeedMax_m_s;
#       float rudder_deg = ((rudder_counts / 4095.0f) - 0.5f) * 2.0f * RudderMax_deg;

#       // --- Update local pose using MATLAB dynamics ---
#       unsigned long now = millis();
#       float dt = 0.05f;

#       // Only integrate if there's meaningful motion
#       if (speed_counts > 0) {
#         float v = speed_m_s;
#         float rho = radians(rudder_deg);
        
#         float xdot = v * cos(rho + state_theta);
#         float ydot = v * sin(rho + state_theta);
#         float thetadot = 0.0f;
        
#         if (fabs(rho) > 0.001f) {  // Only turn if rudder is not centered
#           thetadot = K_theta / (L_vehicle / tan(rho));
#         }

#         state_x += xdot * dt;
#         state_y += ydot * dt;
#         state_theta += thetadot * dt;

#         // Serial.printf("[MASTER] DYNAMICS  xdot=%.4f  ydot=%.4f  thetadot=%.4f\n",
#         //       xdot, ydot, thetadot);

#         // Normalize theta to [0, 2*PI]
#         while (state_theta < 0) state_theta += 2.0f * PI;
#         while (state_theta >= 2.0f * PI) state_theta -= 2.0f * PI;

#         // Clamp X, Y to valid range
#         if (state_x < 0.0f) state_x = 0.0f;
#         if (state_x > 200.0f) state_x = 200.0f;
#         if (state_y < 0.0f) state_y = 0.0f;
#         if (state_y > 200.0f) state_y = 200.0f;
#       }

#       // Send updated pose back to Slave
#       sendPose();

#       // Print diagnostics every second
#       static uint32_t lastPrint = 0;
#       if (millis() - lastPrint > 1000) {
#         lastPrint = millis();

#         Serial.printf("[MASTER] RECV  Speed = %.3f m/s  |  Rudder = %.2f deg  (raw: %u, %u)\n",
#                       speed_m_s, rudder_deg, speed_counts, rudder_counts);
#         Serial.printf("[MASTER] POS   x=%.3f m  y=%.3f m  theta=%.4f rad (deg=%.2f)\n",
#                       state_x, state_y, state_theta, degrees(state_theta));
        
#       }

#     } else {
#       Serial.println("[MASTER] ERR  read feedback failed");
#     }
#   }

#   delay(5);
# }