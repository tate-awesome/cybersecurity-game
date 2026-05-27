//#define REST_API_ENABLED  // Comment out to disable REST API

#include <Arduino.h>
#include <WiFi.h>
#ifdef REST_API_ENABLED
  #include <HTTPClient.h>
  #include <ArduinoJson.h>
#endif
#include <ModbusIP_ESP8266.h>
#include <math.h>

#ifndef PI
#define PI 3.14159265358979323846f
#endif

// ---------- WiFi ----------
const char* ssid     = "GL-SFT1200-ab1";
const char* password = "goodlife";

// ---------- REST ----------
#ifdef REST_API_ENABLED
  const char* REST_URL         = "http://192.168.8.167:5000/data";
  const uint32_t REST_INTERVAL_MS = 2000;
  static uint32_t lastRestMs   = 0;
  static bool encrypt_status   = false;
#endif

// ---------- Modbus ----------
ModbusIP mb;
const uint16_t HREG_X_PHYS       = 10;
const uint16_t HREG_Y_PHYS       = 11;
const uint16_t HREG_THETA_MRAD   = 12;
const uint16_t HREG_SPEED        = 3;
const uint16_t HREG_RUDDER       = 4;

// ---------- Pins ----------
const int PIN_X        = 4;
const int PIN_Y        = 5;
const int PIN_T        = 18;
const int PIN_TARGET_X = 6;
const int PIN_TARGET_Y = 2;

// ---------- Globals ----------
float current_duty_x = 0.5f;
float current_duty_y = 0.5f;

// Expose current state so restPost() can read them
static float g_state_x     = 100.0f;
static float g_state_y     = 100.0f;
static float g_state_theta = 0.0f;
static float g_speed_cmd   = 0.0f;
static float g_rudder_deg  = 0.0f;

// ---------- Control Params ----------
const float HEAD_OFFSET_M  = 2.0f;
const float Kps            = 0.1f;
const float Kp_rudder      = 0.1f;
const float SpeedMax       = 50.0f;
const float StopTol        = 0.3f;
const float X_RANGE_M      = 200.0f;
const float Y_RANGE_M      = 200.0f;
const float RudderMax_deg  = 60.0f;

const int LEDC_RES_BITS = 12;
const int LEDC_FREQ_HZ  = 500;

#ifndef LED_BUILTIN
  #define LED_BUILTIN 2
#endif

// ---------- Helpers ----------
static inline float clampf_local(float v, float lo, float hi) {
    if (isnan(v)) return lo;
    return (v < lo) ? lo : (v > hi ? hi : v);
}

static inline uint16_t phys_to_pwm12(float phys_0_200) {
    float val = clampf_local(phys_0_200, 0.0f, 200.0f);
    return (uint16_t)lroundf((val / 200.0f) * 4095.0f);
}

float wrap_to_pi(float angle) {
    while (angle > PI)  angle -= 2.0f * PI;
    while (angle < -PI) angle += 2.0f * PI;
    return angle;
}

void computeControlCommands(float target_x, float target_y,
                            float state_x, float state_y, float state_theta,
                            float* speed_out, float* rudder_out) {
    float head_x = state_x + HEAD_OFFSET_M * cos(state_theta);
    float head_y = state_y + HEAD_OFFSET_M * sin(state_theta);
    float Xerr   = target_x - head_x;
    float Yerr   = target_y - head_y;

    float ThetaDes   = atan2f(Yerr, Xerr);
    float HeadingErr = wrap_to_pi(ThetaDes - state_theta);
    float rho_rad    = Kp_rudder * HeadingErr;

    rho_rad = clampf_local(rho_rad, -PI / 3.0f, PI / 3.0f);

    float center_dist = sqrtf(powf(Xerr, 2) + powf(Yerr, 2));
    float SpeedCmd    = (center_dist < StopTol) ? 0.0f
                        : clampf_local(Kps * center_dist, 0.0f, SpeedMax);

    if (center_dist < StopTol) rho_rad = 0.0f;

    *speed_out  = SpeedCmd;
    *rudder_out = rho_rad * 180.0f / PI;
}
#ifdef REST_API_ENABLED
void restPost() {
    if (WiFi.status() != WL_CONNECTED) return;

    HTTPClient http;
    http.begin(REST_URL);
    http.addHeader("Content-Type", "application/json");

    // Build JSON payload with current state
    StaticJsonDocument<128> doc;
    doc["timestamp"] = (uint32_t)(millis() / 1000);
    doc["source"]    = "server"; 
    doc["x"]         = g_state_x;
    doc["y"]         = g_state_y;
    doc["theta"]     = g_state_theta;
    doc["speed"]     = g_speed_cmd;
    doc["rudder"]    = g_rudder_deg;

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
                Serial.printf("[SERVER] encryption_key=%s\n", key.c_str());
            }
        }
        Serial.printf("[SERVER] REST OK  encrypt_status=%d\n", encrypt_status);
    } else {
        Serial.printf("[SERVER] REST POST failed  HTTP %d\n", code);
    }

    http.end();
}
#endif

// ---------- Setup ----------
void setup() {
    Serial.begin(115200);
    delay(500);
    Serial.println("\n[SERVER] Booting...");

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    WiFi.setSleep(false);
    while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
    Serial.printf("\n[SERVER] IP: %s\n", WiFi.localIP().toString().c_str());

    // Modbus server
    mb.server();
    mb.addHreg(HREG_X_PHYS,     10000);
    mb.addHreg(HREG_Y_PHYS,     10000);
    mb.addHreg(HREG_THETA_MRAD, 0);
    mb.addHreg(HREG_SPEED,      0);
    mb.addHreg(HREG_RUDDER,     0);

    ledcAttach(PIN_X, LEDC_FREQ_HZ, LEDC_RES_BITS);
    ledcAttach(PIN_Y, LEDC_FREQ_HZ, LEDC_RES_BITS);
    ledcAttach(PIN_T, LEDC_FREQ_HZ, LEDC_RES_BITS);

    pinMode(PIN_TARGET_X, INPUT_PULLUP);
    pinMode(PIN_TARGET_Y, INPUT_PULLUP);
    pinMode(LED_BUILTIN, OUTPUT);

    Serial.println("[SERVER] Ready.");
}

// ---------- Loop ----------
void loop() {
    mb.task();
    yield();

    static float target_x = 100.0f;
    static float target_y = 100.0f;

    // Read target X from PWM pin
    unsigned long txHigh = pulseInLong(PIN_TARGET_X, HIGH, 10000);
    if (txHigh > 0) {
        float duty    = (float)txHigh / 4100.0f;
        current_duty_x = clampf_local(1.0f - duty, 0.0f, 1.0f);
        target_x       = clampf_local(current_duty_x * X_RANGE_M, 0.0f, X_RANGE_M);
    }

    // Read target Y from PWM pin
    unsigned long tyHigh = pulseInLong(PIN_TARGET_Y, HIGH, 10000);
    if (tyHigh > 0) {
        float duty     = (float)tyHigh / 4100.0f;
        current_duty_y = clampf_local(1.0f - duty, 0.0f, 1.0f);
        target_y       = clampf_local(current_duty_y * Y_RANGE_M, 0.0f, Y_RANGE_M);
    }

    // Read state from Modbus registers (written by Client/Master)
    uint16_t h_x  = mb.Hreg(HREG_X_PHYS);
    uint16_t h_y  = mb.Hreg(HREG_Y_PHYS);
    uint16_t h_th = mb.Hreg(HREG_THETA_MRAD);

    if (h_x != 0 || h_y != 0) {
        g_state_x     = clampf_local(h_x / 100.0f, 0.0f, X_RANGE_M);
        g_state_y     = clampf_local(h_y / 100.0f, 0.0f, Y_RANGE_M);
        g_state_theta = ((int16_t)h_th) / 1000.0f;
    }

    // Drive PWM outputs
    ledcWrite(PIN_X, phys_to_pwm12(g_state_x));
    ledcWrite(PIN_Y, phys_to_pwm12(g_state_y));
    float theta_norm = (g_state_theta + PI) / (2.0f * PI);
    ledcWrite(PIN_T, (uint16_t)(clampf_local(theta_norm, 0, 1) * 4095.0f));

    // Compute control commands and write back to Modbus
    computeControlCommands(target_x, target_y,
                           g_state_x, g_state_y, g_state_theta,
                           &g_speed_cmd, &g_rudder_deg);

    mb.Hreg(HREG_SPEED,  (uint16_t)lroundf(clampf_local(g_speed_cmd / SpeedMax, 0, 1) * 4095.0f));
    float rud_norm = (g_rudder_deg / RudderMax_deg + 1.0f) / 2.0f;
    mb.Hreg(HREG_RUDDER, (uint16_t)lroundf(clampf_local(rud_norm, 0, 1) * 4095.0f));

    // REST POST every 2 seconds
    #ifdef REST_API_ENABLED
    if (millis() - lastRestMs >= REST_INTERVAL_MS) {
        lastRestMs = millis();
        restPost();
    }
    #endif

    // Debug print every second
    static uint32_t tPrint = 0;
    if (millis() - tPrint > 1000) {
        tPrint = millis();
        // Serial.printf("[SERVER] Pos:%.1f,%.1f | Tar:%.1f,%.1f | DutyX:%.1f%% | DutyY:%.1f%% | Cmd:%.1f m/s, %.1f deg | encrypt=%d\n",
        //               g_state_x, g_state_y, target_x, target_y,
        //               current_duty_x * 100.0, current_duty_y * 100.0,
        //               g_speed_cmd, g_rudder_deg, encrypt_status);
        Serial.printf("[SERVER] Pos:%.1f,%.1f | Tar:%.1f,%.1f | DutyX:%.1f%% | DutyY:%.1f%% | Cmd:%.1f m/s, %.1f deg"
            #ifdef REST_API_ENABLED
                        " | encrypt=%d"
            #endif
                        "\n",
                        g_state_x, g_state_y, target_x, target_y,
                        current_duty_x * 100.0, current_duty_y * 100.0,
                        g_speed_cmd, g_rudder_deg
            #ifdef REST_API_ENABLED
                        , encrypt_status
            #endif
            );
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    }
}
