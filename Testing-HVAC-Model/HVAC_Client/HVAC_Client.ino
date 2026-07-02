#include <Arduino.h>
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

// WiFi Configuration
const char* AP_SSID     = "ESP32-Config";
const char* AP_PASSWORD = "admin1234"; 

// Modbus Settings
IPAddress serverIP(192, 168, 4, 10);
ModbusIP mb;

const uint16_t HREG_TEMP_EST   = 10;
const uint16_t HREG_DAMPER_CMD = 3;

// --- Physical Simulation Variables (Fahrenheit) ---
float true_room_temp = 71.6f; // Starts at 71.6°F
float state_damper   = 0.0f;
float ambient_temp   = 59.0f;

const float SCALE = 100.0f;

void setup() {
    Serial.begin(115200); 
    
    WiFi.mode(WIFI_STA); 
    WiFi.begin(AP_SSID, AP_PASSWORD); 
    Serial.print("[CLIENT] Connecting to Thermostat AP"); 
    while (WiFi.status() != WL_CONNECTED) { 
        delay(500); 
        Serial.print("."); 
    }
    Serial.println("\n[CLIENT] WiFi Connected."); 

    mb.connect(serverIP);
}

void loop() {
    mb.task();
    yield();

    // Reconnection handling
    if (!mb.isConnected(serverIP)) {
        static uint32_t lastTry = 0;
        if (millis() - lastTry > 2000) {
            lastTry = millis();
            Serial.println("[CLIENT] Reconnecting Modbus...");
            mb.connect(serverIP);
        }
        return;
    }

    // Run physics simulation loop at 10Hz (every 100ms)
    static uint32_t lastUpdate = 0; 
    if (millis() - lastUpdate >= 100) {
        lastUpdate = millis();
        float dt = 0.1f;

        // 1. Read Damper Actuator Command from Server
        uint16_t raw_damper = 0; 
        if (mb.isConnected(serverIP)) { 
            uint16_t trans_id = mb.readHreg(serverIP, HREG_DAMPER_CMD, &raw_damper, 1); 
            while (mb.isTransaction(trans_id)) { mb.task(); delay(1); }
            
            state_damper = (float)raw_damper / 100.0f;
        }

        // Thermal Dynamics Physics Simulation 
        // Heat Loss to environment
        float heat_loss = 0.05f * (true_room_temp - ambient_temp); 
        // Heat Gain from HVAC unit (Scaled to Fahrenheit: 5.0 * 1.8 = 9.0)
        float heat_gain = state_damper * 9.0f; 
        
        // Update true temperature with physical laws + small random ambient drift
        true_room_temp += (heat_gain - heat_loss) * dt; 
        true_room_temp += (random(-18, 19) / 100.0f); // Random physical perturbation scaled to °F (-0.18°F to +0.18°F)

        // 3. Noisy Sensor Reading (Raw measurement)
        // Heavy sensor noise scaled to Fahrenheit (-1.5°C to +1.5°C becomes -2.7°F to +2.7°F)
        float noise = (random(-270, 271) / 100.0f); 
        float noisy_measurement = true_room_temp + noise;

        // 4. Send RAW Noisy Measurement Directly to Server
        uint16_t tx_val = (uint16_t)lroundf(noisy_measurement * SCALE);
        mb.writeHreg(serverIP, HREG_TEMP_EST, tx_val);

        // Print Diagnostics
        Serial.printf("[CLIENT] True Room Temp: %.2f°F | Sent Raw Measurement: %.2f°F | Damper: %.1f%%\n",
                      true_room_temp, noisy_measurement, state_damper * 100.0f); 
    }
}