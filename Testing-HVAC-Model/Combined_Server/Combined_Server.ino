//  Combined Server — Submarine pose-control server + HVAC thermostat
//  server, in one sketch. 

#define REST_API_ENABLED  // Comment out to disable REST API
//#define DEBUG_SERIAL      // Comment out to disable debug output

#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ModbusIP_ESP8266.h>
#include <math.h>
#include <BasicLinearAlgebra.h>

#ifndef PI
#define PI 3.14159265358979323846f
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

#ifndef LED_BUILTIN
  #define LED_BUILTIN 2
#endif

//  SHARED — network, Modbus server setup, mode sync. 

const char* AP_SSID     = "AP-Config";
const char* AP_PASSWORD = "admin1234";
const char* CONFIG_URL  = "http://192.168.4.1/config";
const char* REST_URL    = "http://192.168.4.1/data";
const char* CLIENT_STATE_URL   = "http://192.168.4.1/client_state";
const char* SERVER_CONTROL_URL = "http://192.168.4.1/server_control";

float g_client_x = 0.0f;
float g_client_y = 0.0f;
float g_client_theta = 0.0f;
bool  g_has_client_pose = false;

ModbusIP mb;
bool g_submarine_mode = true;
bool AP_communication = false;

const uint16_t HREG_X_PHYS     = 10;
const uint16_t HREG_Y_PHYS     = 11;
const uint16_t HREG_THETA_MRAD = 12;
const uint16_t HREG_SPEED      = 3;
const uint16_t HREG_RUDDER     = 4;

const uint16_t HREG_TEMP_EST   = 10;  // == HREG_X_PHYS
const uint16_t HREG_DAMPER_CMD = 3;   // == HREG_SPEED

float setpoint_temp = 75.2f; // Target room temperature 75.2°F

void connectWifi() {
  IPAddress staticIP(192, 168, 4, 10);
  IPAddress gateway(192, 168, 4, 1);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.config(staticIP, gateway, subnet);

  WiFi.mode(WIFI_STA);
  WiFi.begin(AP_SSID, AP_PASSWORD);
  Serial.print("[SERVER] Connecting to ESP32-Config AP");

  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(300);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("[SERVER] Connected to AP — IP: %s\n", WiFi.localIP().toString().c_str());
  } else {
    Serial.println("[SERVER] WiFi FAILED!");
    while (1) { delay(1000); }
  }

  WiFi.setSleep(false);
}

void setupModbusRegisters() {
  mb.server();
  // Register 10's initial value picks Submarine's default (10000) since
  // it collides with HVAC's (7160) — doesn't matter functionally, since
  // whichever Client is actually active overwrites it within ~100ms of
  // boot anyway. Register 3 had no real conflict; both models defaulted
  // it to 0.
  mb.addHreg(HREG_X_PHYS,     10000);
  mb.addHreg(HREG_Y_PHYS,     10000);
  mb.addHreg(HREG_THETA_MRAD, 0);
  mb.addHreg(HREG_SPEED,      0);
  mb.addHreg(HREG_RUDDER,     0);
}


void syncModeFromAPConfig() {
  if (WiFi.status() != WL_CONNECTED) return;

  static uint32_t lastConfigSync = 0;
  if (millis() - lastConfigSync < 1000) return;
  lastConfigSync = millis();

  HTTPClient http;
  http.begin(CONFIG_URL);
  int httpCode = http.GET();
  if (httpCode == HTTP_CODE_OK) {
    StaticJsonDocument<256> doc;
    DeserializationError jsonErr = deserializeJson(doc, http.getString());
    if (!jsonErr) {
      if (doc.containsKey("target_temp")) {
        setpoint_temp = doc["target_temp"];
      }
      if (doc.containsKey("submarine_mode")) {
        g_submarine_mode = doc["submarine_mode"].as<bool>();
      }
      if (doc.containsKey("AP_communication")) {
        AP_communication = doc["AP_communication"].as<bool>();
      }
    }
  }
  http.end();
}

// ════════════════════════════════════════════════════════════════════════
//  SUBMARINE MODE — proportional pose control, PWM I/O, telemetry


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
static float g_target_x = 100.0f;
static float g_target_y = 100.0f;
static bool g_state_anomaly_detected = false;

using namespace BLA;

BLA::Matrix<3,1> xhat;   // [x;y;heading angle]
BLA::Matrix<3,3> P;     // covariance matrix
BLA::Matrix<3,3> R;    // measurment noise matrix
BLA::Matrix<2,2> Qu;  // control input noise 
BLA::Matrix<3,3> I3; // identity matrix

float u_prev_speed = 0.0f;
float u_prev_rudder = 0.0f;

float var_x        = 0.5;
float var_y        = 0.5;
float var_theta    = 0.05;

float var_meas_x = 8.33333f;
float var_meas_y = 8.33333f;
float var_meas_theta = 0.01f;

float var_speed    = 0.2f;
float var_rudder   = 0.2f;

// ---------- Encryption ----------
String key = (String)1234;

#ifdef REST_API_ENABLED
  const uint32_t REST_INTERVAL_MS = 2000;
  static uint32_t lastRestMs   = 0;
  static bool encrypt_status   = false;
#endif

// ---------- Control Params ----------
const float HEAD_OFFSET_M  = 2.0f;
const float Kps            = 0.1f;
const float Kp_rudder      = 0.1f;
const float SpeedMax       = 50.0f;
const float StopTol        = 0.3f;
const float X_RANGE_M      = 200.0f;
const float Y_RANGE_M      = 200.0f;
const float RudderMax_deg  = 60.0f;
const float K_theta = 0.6f;
const float L_vehicle = 0.07f;

const int LEDC_RES_BITS = 12;
const int LEDC_FREQ_HZ  = 500;

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

void ekfStep(float speed_m_s, float rudder_rad, const BLA::Matrix<3,1>& z_meas, float dt){

  BLA::Matrix<3,1> x_pred;
  float th = xhat(2,0);

  x_pred(0,0) = xhat(0,0) + speed_m_s * cos(th + rudder_rad) * dt;
  x_pred(1,0) = xhat(1,0) + speed_m_s * sin(th + rudder_rad) * dt;
  x_pred(2,0) = wrap_to_pi(th + K_theta * (tan(rudder_rad) / L_vehicle) * dt);

  Matrix<3,3> F = {
    1, 0, -speed_m_s * sin(th + rudder_rad) * dt,
    0, 1,  speed_m_s * cos(th + rudder_rad) * dt,
    0, 0,  1
  };

  Matrix<3,2> G = {
    cos(th + rudder_rad) * dt, -speed_m_s * sin(th + rudder_rad) * dt,
    sin(th + rudder_rad) * dt,  speed_m_s * cos(th + rudder_rad) * dt,
    0, (K_theta * dt / L_vehicle) * (1.0f / (cos(rudder_rad) * cos(rudder_rad)))
  };

  Matrix<3,3> P_pred = F * P * ~F + G * Qu * ~G;

  Matrix<3,3> S = P_pred + R;      // H = I
  Matrix<3,3> K = P_pred * Inverse(S);

  Matrix<3,1> y = z_meas - x_pred;
  y(2,0) = wrap_to_pi(y(2,0));

  xhat = x_pred + K * y;

  P = (I3 - K) * P_pred; 
}

void computeControlCommands(float target_x, float target_y, float state_x, float state_y, float state_theta, float* speed_out, float* rudder_out) {
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

uint16_t xorCipher(uint16_t value, uint16_t key){
    return value ^ key;
}

uint16_t keyToUint(const String& key){
  int sum = 0;
  for(int i = 0; i< key.length(); i++){
    sum += key.charAt(i);
  }
  return (uint16_t)sum;
}

#ifdef REST_API_ENABLED
void restPost() {
    if (WiFi.status() != WL_CONNECTED) return;

    HTTPClient http;
    http.begin(REST_URL);
    http.addHeader("Content-Type", "application/json");

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
        StaticJsonDocument<128> resp;
        if (!deserializeJson(resp, body)) {
            if (resp.containsKey("encryption_status")) {
                encrypt_status = resp["encryption_status"].as<bool>();
                key = resp["encryption_key"].as<String>();
                Serial.printf("[SERVER] encryption_key=%s\n", key.c_str());
            }

            if (resp.containsKey("target_x") && resp.containsKey("target_y")) {
                g_target_x = resp["target_x"].as<float>();
                g_target_y = resp["target_y"].as<float>();
                Serial.printf("[SERVER] Target updated: %.1f, %.1f\n", g_target_x, g_target_y);
            }

            if (resp.containsKey("submarine_mode")) {
                g_submarine_mode = resp["submarine_mode"].as<bool>();
            }
        }
        Serial.printf("[SERVER] REST OK  encrypt_status=%d\n", encrypt_status);
    } else {
        Serial.printf("[SERVER] REST POST failed  HTTP %d\n", code);
    }

    http.end();
}
#endif

bool fetchClientState() {
    if (WiFi.status() != WL_CONNECTED) {
        g_has_client_pose = false;
        return false;
    }

    HTTPClient http;
    http.begin(CLIENT_STATE_URL);
    int code = http.GET();

    if (code == HTTP_CODE_OK) {
        StaticJsonDocument<128> doc;
        if (!deserializeJson(doc, http.getString())) {
            bool valid = doc["valid"] | false;
            uint32_t age = doc["age_ms"] | 999999;

            if (valid && age <= 500) {
                g_client_x = doc["x"] | 0.0f;
                g_client_y = doc["y"] | 0.0f;
                g_client_theta = doc["heading"] | 0.0f;
                g_has_client_pose = true;
                http.end();
                return true;
            }
        }
    }

    g_has_client_pose = false;
    http.end();
    return false;
}

void postServerControl() {
    if (WiFi.status() != WL_CONNECTED) return;

    HTTPClient http;
    http.begin(SERVER_CONTROL_URL);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<128> doc;
    doc["source"]   = "server";
    doc["velocity"] = g_speed_cmd;
    doc["rudder"]   = g_rudder_deg;

    String body;
    serializeJson(doc, body);

    int code = http.POST(body);
    if (code != 200) {
        Serial.printf("[SERVER] postServerControl failed HTTP %d\n", code);
    }

    http.end();
}


void runSubmarineCycle() {
    float target_x = g_target_x;
    float target_y = g_target_y;

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

    uint16_t h_x, h_y, h_th;
    float last_state_x, last_state_y, last_state_theta;
    bool new_value = false;

    // Read state from Modbus registers (written by Client)
    if (encrypt_status) {
        h_x  = xorCipher(mb.Hreg(HREG_X_PHYS), keyToUint(key));
        h_y  = xorCipher(mb.Hreg(HREG_Y_PHYS), keyToUint(key));
        h_th = xorCipher(mb.Hreg(HREG_THETA_MRAD), keyToUint(key));
    } else {
        h_x  = mb.Hreg(HREG_X_PHYS);
        h_y  = mb.Hreg(HREG_Y_PHYS);
        h_th = mb.Hreg(HREG_THETA_MRAD);
    }

    if (h_x != 0 || h_y != 0) {
        g_state_x     = clampf_local(h_x / 100.0f, 0.0f, X_RANGE_M);
        g_state_y     = clampf_local(h_y / 100.0f, 0.0f, Y_RANGE_M);
        g_state_theta = ((int16_t)h_th) / 1000.0f;
    }

    if(AP_communication){
      fetchClientState();
      if(g_has_client_pose){
        g_state_x     = clampf_local(g_client_x, 0.0f, X_RANGE_M);
        g_state_y     = clampf_local(g_client_y, 0.0f, Y_RANGE_M);
        g_state_theta = wrap_to_pi(g_client_theta);
      }else{
        return;
      }
    }

    if(last_state_x == g_state_x && last_state_y == g_state_y && last_state_theta == g_state_theta){
      new_value = true;
    }

    last_state_x = g_state_x;
    last_state_y = g_state_y;
    last_state_theta = g_state_theta;

    BLA::Matrix<3,1> z_meas;

    z_meas(0,0) = g_state_x;
    z_meas(1,0) = g_state_y;
    z_meas(2,0) = wrap_to_pi(g_state_theta);

    if(new_value){
      ekfStep(u_prev_speed, u_prev_rudder, z_meas, 0.05f);

      g_state_x = xhat(0,0);
      g_state_y = xhat(1,0);
      g_state_theta = xhat(2,0);

      float xError = abs( z_meas(0,0) - xhat(0,0) );
      float yError = abs( z_meas(1,0) - xhat(1,0) );
      float tError = wrap_to_pi(z_meas(2,0) - xhat(2,0));

      bool xCheck = xError > 8;
      bool yCheck = yError > 8;
      bool thetaCheck = fabs(tError) > 3;

      g_state_anomaly_detected = xCheck || yCheck || thetaCheck;
    }

    // Drive PWM outputs
    ledcWrite(PIN_X, phys_to_pwm12(g_state_x));
    ledcWrite(PIN_Y, phys_to_pwm12(g_state_y));
    float theta_norm = (g_state_theta + PI) / (2.0f * PI);
    ledcWrite(PIN_T, (uint16_t)(clampf_local(theta_norm, 0, 1) * 4095.0f));

    // Compute control commands
    computeControlCommands(target_x, target_y, g_state_x, g_state_y, g_state_theta, &g_speed_cmd, &g_rudder_deg);

    u_prev_speed = g_speed_cmd;
    u_prev_rudder = g_rudder_deg * PI / 180.0f;

    if(AP_communication){
      postServerControl();
    }

    // Write speed/rudder back to Modbus
    float rud_norm = (g_rudder_deg / RudderMax_deg + 1.0f) / 2.0f;
    uint16_t unencrypted_speed = (uint16_t)lroundf(clampf_local(g_speed_cmd / SpeedMax, 0, 1) * 4095.0f);
    uint16_t unencrypted_rudder = (uint16_t)lroundf(clampf_local(rud_norm, 0, 1) * 4095.0f);

    if (encrypt_status) {
        uint16_t encrypted_speed = xorCipher(unencrypted_speed, keyToUint(key));
        uint16_t encrypted_rudder = xorCipher(unencrypted_rudder, keyToUint(key));
        mb.Hreg(HREG_SPEED, encrypted_speed);
        mb.Hreg(HREG_RUDDER, encrypted_rudder);
    } else {
        mb.Hreg(HREG_SPEED, unencrypted_speed);
        mb.Hreg(HREG_RUDDER, unencrypted_rudder);
    }

    #ifdef REST_API_ENABLED
    if (millis() - lastRestMs >= REST_INTERVAL_MS) {
        lastRestMs = millis();
        restPost();
    }
    #endif

    static uint32_t tPrint = 0;
    if (millis() - tPrint > 1000) {
        tPrint = millis();
        Serial.printf("[SERVER] Pos:%.1f,%.1f | Tar:%.1f,%.1f | DutyX:%.1f%% | DutyY:%.1f%% | Cmd:%.1f m/s, %.1f deg"
            #ifdef REST_API_ENABLED
                        " | encrypt=%d"
            #endif
                        "\n",
                        g_state_x, g_state_y, g_target_x, g_target_y,
                        current_duty_x * 100.0, current_duty_y * 100.0,
                        g_speed_cmd, g_rudder_deg
            #ifdef REST_API_ENABLED
                        , encrypt_status
            #endif
            );
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    }
}

// ════════════════════════════════════════════════════════════════════════
//  HVAC MODE — hysteresis (on/off) thermostat control

float hysteresis_band = 0.5f;
bool heater_on = false;

const float SCALE = 100.0f;


void postHvacStatus(float current_temp) {
  static uint32_t lastStatusPost = 0;
  if (WiFi.status() != WL_CONNECTED || millis() - lastStatusPost < 1000) return;
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

void runHvacCycle() {
    static uint32_t lastControlTime = 0;
    if (millis() - lastControlTime < 100) return;
    lastControlTime = millis();

    uint16_t raw_temp = mb.Hreg(HREG_TEMP_EST);
    float current_temp = (float)raw_temp / SCALE;

    float lower_threshold = setpoint_temp - hysteresis_band;
    float upper_threshold = setpoint_temp + hysteresis_band;

    if (current_temp <= lower_threshold) {
        heater_on = true;   // Too cold -> switch heat ON
    } else if (current_temp >= upper_threshold) {
        heater_on = false;  // Too warm -> switch heat OFF
    }
    // else: inside the deadband -> hold whatever state we were already in

    uint16_t damper_pct_out = heater_on ? 100 : 0;
    mb.Hreg(HREG_DAMPER_CMD, damper_pct_out);

    Serial.printf("[SERVER] Setpoint: %.2f°F | Current: %.2f°F | Band: [%.2f, %.2f]°F | Heater: %s\n",
                  setpoint_temp, current_temp, lower_threshold, upper_threshold, heater_on ? "ON" : "OFF");

    postHvacStatus(current_temp);
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n[SERVER] Booting (combined Submarine/HVAC)...");

  connectWifi();
  setupModbusRegisters();

  // Submarine-specific pin setup runs unconditionally — the mode could
  // flip to SUBMARINE at any point after boot, so the PWM/PLC I/O pins
  // need to be ready regardless of which model starts out active.
  ledcAttach(PIN_X, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcAttach(PIN_Y, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcAttach(PIN_T, LEDC_FREQ_HZ, LEDC_RES_BITS);
  pinMode(PIN_TARGET_X, INPUT_PULLUP);
  pinMode(PIN_TARGET_Y, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);

  xhat.Fill(0);
  xhat(0,0) = g_state_x;
  xhat(1,0) = g_state_y;
  xhat(2,0) = g_state_theta;

  P = {
    var_x, 0.0f, 0.0f,
    0.0f, var_y, 0.0f,
    0.0f, 0.0f, var_theta
    };

  R = {
    var_meas_x, 0.0f, 0.0f,
    0.0f, var_meas_y, 0.0f,
    0.0f, 0.0f, var_meas_theta
    };

  Qu = {
    var_speed, 0.0f,
    0.0f, var_rudder
    };

  I3 = {1.0f, 0.0f, 0.0f,
        0.0f, 1.0f, 0.0f,
        0.0f, 0.0f, 1.0f
    };

  Serial.println("[SERVER] Ready.");
}

void loop() {
    mb.task();
    yield();

    syncModeFromAPConfig();   // Always runs (internally rate-limited to ~1Hz)

    if (g_submarine_mode) {
        runSubmarineCycle();
    } else {
        runHvacCycle();
    }
}