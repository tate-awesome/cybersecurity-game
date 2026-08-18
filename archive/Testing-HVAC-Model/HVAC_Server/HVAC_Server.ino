#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

// WiFi credentials for AP_ESP32's network (Server joins as a station)
const char* AP_SSID     = "ESP32-Config"; 
const char* AP_PASSWORD = "admin1234"; 

ModbusIP mb;

const uint16_t HREG_TEMP_EST   = 10;
const uint16_t HREG_DAMPER_CMD = 3;

float setpoint_temp = 75.2f; // Target room temperature 75.2°F
float hysteresis_band = 0.5f;
bool heater_on = false; 
bool hvac_mode_active = true;

const float SCALE = 100.0f; 

void setup() {
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);

    IPAddress staticIP(192, 168, 4, 10);
    IPAddress gateway(192, 168, 4, 1); 
    IPAddress subnet(255, 255, 255, 0); 
    WiFi.config(staticIP, gateway, subnet);

    WiFi.begin(AP_SSID, AP_PASSWORD);
    Serial.print("[SERVER] Connecting to Thermostat AP");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\n[SERVER] WiFi Connected.");
    Serial.printf("[SERVER] IP Address: %s\n", WiFi.localIP().toString().c_str()); 
    mb.server(); 
    mb.addHreg(HREG_TEMP_EST, 7160);
    mb.addHreg(HREG_DAMPER_CMD, 0); 
}

void loop() {
    mb.task();
    yield();

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin("http://192.168.4.1/config");
        int httpCode = http.GET();
        if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            StaticJsonDocument<256> doc;
            DeserializationError jsonErr = deserializeJson(doc, payload);
            if (!jsonErr) {
                if (doc.containsKey("target_temp")) {
                    setpoint_temp = doc["target_temp"]; // Dynamically overrides 75.2f
                }
                if (doc.containsKey("submarine_mode")) {
                    hvac_mode_active = !(doc["submarine_mode"].as<bool>());
                }
            }
        }
        http.end();
    }

    // Run thermostat control loop at 10Hz (every 100ms)
    static uint32_t lastControlTime = 0; 
    if (millis() - lastControlTime >= 100) { 
        lastControlTime = millis();

        uint16_t raw_temp = mb.Hreg(HREG_TEMP_EST); 
        float current_temp = (float)raw_temp / SCALE; 

        if (!hvac_mode_active) {
            heater_on = false;
            mb.Hreg(HREG_DAMPER_CMD, 0);
            Serial.printf("[SERVER] HVAC inactive (AP in SUBMARINE mode) | Current: %.2f°F | Heater: OFF\n",
                          current_temp);
        } else {
            float lower_threshold = setpoint_temp - hysteresis_band;
            float upper_threshold = setpoint_temp + hysteresis_band;

            if (current_temp <= lower_threshold) {
                heater_on = true;   // Too cold -> switch heat ON
            } else if (current_temp >= upper_threshold) {
                heater_on = false;  // Too warm -> switch heat OFF
            }

            uint16_t damper_pct_out = heater_on ? 100 : 0;
            mb.Hreg(HREG_DAMPER_CMD, damper_pct_out); 

            Serial.printf("[SERVER] Setpoint: %.2f°F | Current: %.2f°F | Band: [%.2f, %.2f]°F | Heater: %s\n",
                          setpoint_temp, current_temp, lower_threshold, upper_threshold, heater_on ? "ON" : "OFF"); 
        }

        // Throttled to 1Hz, separate from the 10Hz control rate above —
        // posting an HTTP request every single 100ms tick would be
        / unnecessary
        static uint32_t lastStatusPost = 0;
        if (WiFi.status() == WL_CONNECTED && millis() - lastStatusPost >= 1000) {
            lastStatusPost = millis();
            HTTPClient statusHttp;
            statusHttp.begin("http://192.168.4.1/hvac_status");
            statusHttp.addHeader("Content-Type", "application/json");
            StaticJsonDocument<128> statusDoc;
            statusDoc["current_temp"] = current_temp;
            statusDoc["heater_on"]    = heater_on;
            String statusBody;
            serializeJson(statusDoc, statusBody);
            statusHttp.POST(statusBody);
            statusHttp.end();
        }
    }
}