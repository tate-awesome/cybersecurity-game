#include <Arduino.h>
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>
#include <math.h>

#ifndef PI
#define PI 3.14159265358979323846f
#endif

// ---------- WiFi ----------
const char* ssid     = "GL-SFT1200-ab1";
const char* password = "goodlife";
IPAddress serverIP(192, 168, 8, 243);  // <-- Master IP
String macAddress = "34:cd:b0:33:85:b4"; // <--- Master MAC

//// ---------- Encryption ----------
uint16_t key = 1234567891234567;
bool encrypt_on = true;

// ---------- Modbus ----------
ModbusIP mb;
const uint16_t HREG_X_PHYS       = 10;
const uint16_t HREG_Y_PHYS       = 11;
const uint16_t HREG_THETA_MRAD   = 12;
const uint16_t HREG_SPEED        = 3; 
const uint16_t HREG_RUDDER       = 4; 
const uint16_t HREG_ENCRYPTION = 5;

// ---------- Pins ----------
const int PIN_X   = 4;     // to PLC AI1
const int PIN_Y   = 5;     // to PLC AI2
const int PIN_T   = 18;    // to PLC AI3
const int PIN_TARGET_X = 6; 
const int PIN_TARGET_Y = 2; 

// ---------- Globals ----------
float current_duty_x = 0.5f;
float current_duty_y = 0.5f;

// ---------- Control Params ----------
const float HEAD_OFFSET_M = 2.0f; 
const float Kps = 0.1f;
const float Kp_rudder = 0.1f;
const float SpeedMax = 50.0f;
const float StopTol = 0.3f;
const float X_RANGE_M = 200.0f;
const float Y_RANGE_M = 200.0f;
const float RudderMax_deg = 60.0f;

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
    while (angle > PI) angle -= 2.0f * PI;
    while (angle < -PI) angle += 2.0f * PI;
    return angle;
}

void computeControlCommands(float target_x, float target_y, 
                          float state_x, float state_y, float state_theta,
                          float* speed_out, float* rudder_out) {
  float head_x = state_x + HEAD_OFFSET_M * cos(state_theta);
  float head_y = state_y + HEAD_OFFSET_M * sin(state_theta);
  float Xerr = target_x - head_x;
  float Yerr = target_y - head_y;
  
  float ThetaDes = atan2f(Yerr, Xerr);
  float HeadingErr = wrap_to_pi(ThetaDes - state_theta);
  float rho_rad = Kp_rudder * HeadingErr;

  // Clamp Rudder
  rho_rad = clampf_local(rho_rad, -PI/3.0f, PI/3.0f);

  float center_dist = sqrtf(powf(Xerr, 2) + powf(Yerr, 2));
  float SpeedCmd = (center_dist < StopTol) ? 0.0f : clampf_local(Kps * center_dist, 0.0f, SpeedMax);
  
  if (center_dist < StopTol) rho_rad = 0.0f;

  *speed_out = SpeedCmd;
  *rudder_out = rho_rad * 180.0f / PI;
}

uint16_t xorCipher(uint16_t value, uint16_t key) {
  return value ^ key;
}

void changeEncryptionState(){
  if(encrypt_on){
    encrypt_on = false;
  }else{
    encrypt_on = true;
  }
}

//// ---------- WIFI Characteristic Helper Functions ----------

String getIP(){
  return WiFi.localIP().toString();
}

String getMacAddress(){
  return WiFi.macAddress();
}

String isIPMACValid(){
  String ipSent = getIP();
  String macSent = getMacAddress();
  String ip = serverIP.toString();
  String mac = macAddress;

  if(ip !=  ipSent || mac != macSent){
    return "The communicating IP and MAC pair does not match the expected pair.";
  }else{
    return "";
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n[SLAVE] Booting S3 (Standard API)...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
  Serial.printf("\n[SLAVE] IP: %s\n", WiFi.localIP().toString().c_str());
  

  mb.server();
  mb.addHreg(HREG_X_PHYS, 10000);
  mb.addHreg(HREG_Y_PHYS, 10000);
  mb.addHreg(HREG_THETA_MRAD, 0);
  mb.addHreg(HREG_SPEED, 0);
  mb.addHreg(HREG_RUDDER, 0);

  ledcAttach(PIN_X, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcAttach(PIN_Y, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcAttach(PIN_T, LEDC_FREQ_HZ, LEDC_RES_BITS);

  pinMode(PIN_TARGET_X, INPUT_PULLUP);
  pinMode(PIN_TARGET_Y, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("[SLAVE] Ready.");
}

void loop() {
  mb.task();
  yield();
  isIPMACValid();

// Our default taegt values(safety net) if PLC
  static float target_x = 0.0f;
  static float target_y = 0.0f;

  unsigned long txHigh = pulseInLong(PIN_TARGET_X, HIGH, 10000);
  if (txHigh > 0) {
      float duty = (float)txHigh / 4100.0f; 
      current_duty_x = clampf_local(1.0f - duty, 0.0f, 1.0f);
      target_x = current_duty_x * X_RANGE_M;
      target_x = clampf_local(target_x, 0.0f, X_RANGE_M);
  }

  unsigned long tyHigh = pulseInLong(PIN_TARGET_Y, HIGH, 10000);
  if (tyHigh > 0) {
      float duty = (float)tyHigh / 4100.0f;
      current_duty_y = clampf_local(1.0f - duty, 0.0f, 1.0f);

      target_y = current_duty_y * Y_RANGE_M;
      target_y = clampf_local(target_y, 0.0f, Y_RANGE_M);
  }

  uint16_t h_x;
  uint16_t h_y;
  uint16_t h_th;

  if(encrypt_on){

      h_x = xorCipher(mb.Hreg(HREG_X_PHYS), key);
      h_y = xorCipher(mb.Hreg(HREG_Y_PHYS), key);
      h_th = xorCipher(mb.Hreg(HREG_THETA_MRAD), key);

  }else{

      h_x = mb.Hreg(HREG_X_PHYS);
      h_y = mb.Hreg(HREG_Y_PHYS);
      h_th = mb.Hreg(HREG_THETA_MRAD);

  }

  static float state_x = 100.0f, state_y = 100.0f, state_theta = 0.0f;
  if (h_x != 0 || h_y != 0) {
      state_x = clampf_local(h_x / 100.0f, 0.0f, X_RANGE_M);
      state_y = clampf_local(h_y / 100.0f, 0.0f, Y_RANGE_M);
      state_theta = ((int16_t)h_th) / 1000.0f;
  }

  ledcWrite(PIN_X, phys_to_pwm12(state_x));
  ledcWrite(PIN_Y, phys_to_pwm12(state_y));
  float theta_norm = (state_theta + PI) / (2.0f * PI);
  ledcWrite(PIN_T, (uint16_t)(clampf_local(theta_norm, 0, 1) * 4095.0f));

  float SpeedCmd = 0, RudderDeg = 0;
  computeControlCommands(target_x, target_y, state_x, state_y, state_theta, &SpeedCmd, &RudderDeg);

  float rud_norm = (RudderDeg / RudderMax_deg + 1.0f) / 2.0f;
  uint16_t unencrypted_speed = (uint16_t)lroundf(clampf_local(SpeedCmd/SpeedMax, 0, 1) * 4095.0f);
  uint16_t unencrypted_rudder = (uint16_t)lroundf(clampf_local(rud_norm, 0, 1) * 4095.0f);

  if(encrypt_on){

    uint16_t encrypted_speed = xorCipher(unencrypted_speed, key);
    uint16_t encrypted_rudder = xorCipher(unencrypted_rudder, key);
    mb.Hreg(HREG_SPEED, encrypted_speed);
    mb.Hreg(HREG_RUDDER, encrypted_rudder);

  }else{

    mb.Hreg(HREG_SPEED, unencrypted_speed);
    mb.Hreg(HREG_RUDDER, unencrypted_rudder);

  }

  // --- 6) Debug ---
  static uint32_t tPrint = 0;
  if (millis() - tPrint > 1000) {
    tPrint = millis();
    Serial.printf("[S3] Pos:%.1f,%.1f | Tar:%.1f,%.1f | DutyX:%.1f%% |DutyY:%.1f%% | Cmd:%.1f m/s, %.1f deg\n", 
                  state_x, state_y, target_x, target_y, current_duty_x*100.0,current_duty_y*100.0, SpeedCmd, RudderDeg);
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
}