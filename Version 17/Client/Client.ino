#define REST_API_ENABLED  // Comment out to disable REST API
//#define DEBUG_SERIAL      // Comment out to disable debug output

#include <Arduino.h>
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>
#include <Wire.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h>  // Frank de Brabander
#include <BasicLinearAlgebra.h>

#ifndef PI
#define PI 3.14159265358979323846f
#endif

//  AP ESP32 is always at this address 
const char* AP_SSID     = "AP-Config";
const char* AP_PASSWORD = "admin1234";
const char* CONFIG_URL  = "http://192.168.4.1/config";
const char* REST_URL    = "http://192.168.4.1/data";

static bool g_submarine_mode = true;

#ifdef REST_API_ENABLED
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

IPAddress serverIP(192, 168, 4, 10);   // ← was 192.168.8.137

ModbusIP mb;

using namespace BLA;
bool filtering = true;

BLA::Matrix<3,1> xhat;   // [x;y;heading angle]
BLA::Matrix<3,3> P;     // covariance matrix
BLA::Matrix<3,3> R;    // measurment noise matrix
BLA::Matrix<2,2> Qu;  // control input noise 
BLA::Matrix<3,3> I3; // identity matrix

float sigma_x = 0.01;
float sigma_y = 0.01;
float sigma_theta = 0.01;

float sigma_meas_x = 8.3f;
float sigma_meas_y = 8.3f;
float sigma_meas_theta = 0.01f;

float sigma_speed = 0.01f;
float sigma_rudder = 0.01f;

bool kalman_correction = true;
bool g_anomaly_detected = false;

float state_x = 0.0f;
float state_y = 0.0f;
float state_theta = 0.0f;
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

static String key = (String)1234;

static float avX = 0.0f;
static float avY = 0.0f;
static float avT = 0.0f;
static uint32_t countX = 0;
static uint32_t countY = 0;
static uint32_t countT = 0;

bool targetChanged = false;

//// Physical scaling constants 
const float SpeedMax_m_s = 50.0f;
const float RudderMax_deg = 60.0f;

//// Kalman Filter Helper Functions 

float wrapToPi(float a) {
  while (a > PI)  a -= 2.0f * PI;
  while (a < -PI) a += 2.0f * PI;
  return a;
}

void ekfStep(float speed_m_s, float rudder_rad, const Matrix<3,1>& z_meas, float dt)
{
  // Predict
  BLA::Matrix<3,1> x_pred;
  float th = xhat(2,0);

  x_pred(0,0) = xhat(0,0) + speed_m_s * cos(th + rudder_rad) * dt;
  x_pred(1,0) = xhat(1,0) + speed_m_s * sin(th + rudder_rad) * dt;
  x_pred(2,0) = wrapToPi(xhat(2,0) + K_theta * (tan(rudder_rad) / L_vehicle) * dt);

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

  // Update
  Matrix<3,3> S = P_pred + R;      // H = I
  Matrix<3,3> K = P_pred * Inverse(S);

  Matrix<3,1> y = z_meas - x_pred;
  y(2,0) = wrapToPi(y(2,0));

  xhat = x_pred + K * y;
  xhat(2,0) = wrapToPi(xhat(2,0));

  P = (I3 - K) * P_pred;
}

void resetEKF(float x0, float y0, float theta0)
{
  // Reset state estimate to a safe starting point
  xhat(0,0) = x0;
  xhat(1,0) = y0;
  xhat(2,0) = theta0;

  // Reset uncertainty
  P = {
    sigma_x, 0.0f,   0.0f,
    0.0f,    sigma_y, 0.0f,
    0.0f,    0.0f,    sigma_theta
  };

  // Clear anomaly state
  g_anomaly_detected = false;
}

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
    DBG_PRINTF("[CLIENT] writeH FAIL addr=%u: not connected\n", addr);
    return false;
  }
  // One retry on timeout to handle occasional WiFi jitter
  for (int attempt = 0; attempt < 2; attempt++) {
    uint16_t tx = mb.writeHreg(serverIP, addr, val);
    if (!tx) {
      DBG_PRINTF("[CLIENT] writeH FAIL addr=%u: writeHreg returned 0 (queue full or busy)\n", addr);
      return false;  // retrying won't help so exit immediately.
    }
    // Poll until the transaction clears, up to a hard timeout of 300ms.
    uint32_t start = millis();
    while (millis() - start < 300) {
      mb.task();
      if (!mb.isTransaction(tx)) return true;
      delay(3);
    }
    DBG_PRINTF("[CLIENT] writeH addr=%u: transaction timed out (attempt %d/2)\n", addr, attempt + 1);
    for (int i = 0; i < 5; i++) { mb.task(); delay(5); }
  }
  return false;
}

bool readH(uint16_t addr, uint16_t* buf, uint16_t n) {
  if (!mb.isConnected(serverIP)) {
    DBG_PRINTLN("[CLIENT] readH FAIL: not connected");
    return false;
  }
  // 1 retry on timeout to handle occasional WiFi jitter
  for (int attempt = 0; attempt < 2; attempt++) {
    uint16_t tx = mb.readHreg(serverIP, addr, buf, n);
    if (!tx) {
      DBG_PRINTLN("[CLIENT] readH FAIL: readHreg returned 0 (queue full or busy)");
      return false;  // retrying won't help so bail immediately.
    }
    // Poll until the transaction clears, up to a hard timeout of 300ms.
    uint32_t start = millis();
    while (millis() - start < 300) {
      mb.task();
      if (!mb.isTransaction(tx)) return true;
    }
    DBG_PRINTF("[CLIENT] readH FAIL: transaction timed out (attempt %d/2)\n", attempt + 1);
    for (int i = 0; i < 5; i++) { mb.task(); delay(5); }
  }
  return false;
}

//// Encryption Helper Functions 
uint16_t xorCipher(uint16_t value, uint16_t key){
  return value ^ key;
}

void xorArrayDecrypt(uint16_t data[2], uint16_t key){
  for(int i = 0; i < 2; i++){
    data[i] ^= key;
  }
}

uint16_t keyToUint(const String& key){

  int sum = 0;

  for(int i = 0; i< key.length(); i++){
    sum += key.charAt(i);
  }

  return(uint16_t)sum;
}

void sendPose() {
  uint16_t x_u = x_to_u16_100(state_x);
  uint16_t y_u = x_to_u16_100(state_y);
  uint16_t t_u = theta_to_mrad_u16(state_theta);

  if (writeH(HREG_X_PHYS, x_u) && writeH(HREG_Y_PHYS, y_u) && writeH(HREG_THETA_MRAD, t_u)) {
    // Success - values sent
  } else {
    Serial.println("[CLIENT] ERR: Failed to send pose to Server");
  }
}

void sendPoseEncrypted(){
  uint16_t x_u = xorCipher(x_to_u16_100(state_x), keyToUint(key));
  uint16_t y_u = xorCipher(x_to_u16_100(state_y), keyToUint(key));
  uint16_t t_u = xorCipher(theta_to_mrad_u16(state_theta), keyToUint(key));

  bool x = writeH(HREG_X_PHYS, x_u);
  bool y = writeH(HREG_Y_PHYS, y_u);
  bool theta = writeH(HREG_THETA_MRAD, t_u);
  if(x && y && theta){    
  }else{
    Serial.print("[CLIENT] ERR: Failed to send pose to Server.");
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
  doc["source"] = "client";
  doc["timestamp"] = (uint32_t)(millis() / 1000);
  doc["x"]         = state_x;
  doc["y"]         = state_y;
  doc["theta"]     = state_theta;
  doc["speed"]     = state_speed;
  doc["rudder"]    = state_rudder;
  doc["anomaly_detected"] = g_anomaly_detected;

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
        }
        if (resp.containsKey("filter_correction")) { 
            kalman_correction = resp["filter_correction"].as<bool>();
        }
        if (resp.containsKey("submarine_mode")) {
            g_submarine_mode = resp["submarine_mode"].as<bool>();
        }
    }
  } else {
    Serial.printf("[CLIENT] REST POST failed  HTTP %d\n", code);
  }

  http.end();
}
#endif

void setup() {
  Serial.begin(115200);
  delay(50);
  Serial.println("\n[MASTER] Booting...");

  // Initialize LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Master Init...");

  // Connect directly to AP ESP32
  lcd.setCursor(0, 1);
  lcd.print("WiFi connect...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(AP_SSID, AP_PASSWORD);
  Serial.print("[MASTER] Connecting to ESP32-Config AP");

  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(300);
    Serial.print(".");
  }
  Serial.println();

  lcd.clear();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("[MASTER] Connected to AP — IP: %s\n",
                  WiFi.localIP().toString().c_str());
    lcd.setCursor(0, 0);
    lcd.print("WiFi: OK");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
    delay(2000);
  } else {
    lcd.setCursor(0, 0);
    lcd.print("WiFi: FAILED!");
    Serial.println("[MASTER] WiFi failed!");
    while(1) { delay(1000); }
  }

  WiFi.setSleep(false);
  Serial.println("[MASTER] WiFi sleep disabled");

  // Connect to Slave via Modbus
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connect Slave...");
  mb.connect(serverIP);
  delay(500);

  xhat.Fill(0);
  xhat(0,0) = state_x;
  xhat(1,0) = state_y;
  xhat(2,0) = state_theta;

  P = {
    sigma_x, 0.0f, 0.0f,
    0.0f, sigma_y, 0.0f,
    0.0f, 0.0f, sigma_theta
    };

  R = {
    sigma_meas_x, 0.0f, 0.0f,
    0.0f, sigma_meas_y, 0.0f,
    0.0f, 0.0f, sigma_meas_theta
    };

  Qu = {
    sigma_speed, 0.0f,
    0.0f, sigma_rudder
    };

  I3 = {1.0f, 0.0f, 0.0f,
        0.0f, 1.0f, 0.0f,
        0.0f, 0.0f, 1.0f
    };

  if (mb.isConnected(serverIP)) {
    Serial.println("[MASTER] Connected to Slave Modbus server.");
    lcd.setCursor(0, 1);
    lcd.print("Slave: OK");
    delay(1000);
    if (encrypt_status) {
      sendPoseEncrypted();
    } else {
      sendPose();
    }
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

void loop() {
  mb.task();
  yield();

  // Reconnect if disconnected
  if (!mb.isConnected(serverIP)) {
    static uint32_t lastTry = 0;
    if (millis() - lastTry > 2000) {
      lastTry = millis();
      Serial.println("[CLIENT] Reconnecting Modbus…");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Reconnecting...");
      
      mb.connect(serverIP);
      if (mb.isConnected(serverIP)) {
        Serial.println("[CLIENT] Reconnected successfully!");
        if(encrypt_status){
          sendPoseEncrypted();
        }else{
          sendPose();
        }
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

      if(encrypt_status){
        xorArrayDecrypt(rb, keyToUint(key));
      }

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

      if(!filtering){

        float xdot = v * cos(rho + state_theta);
        float ydot = v * sin(rho + state_theta);
        float thetadot = 0.0f;
        
        // Only turn if rudder is not centered
        if (fabs(rho) > 0.001f) {
          thetadot = K_theta / (L_vehicle / tan(rho));
        }

        state_x += (xdot * dt) + random(-500,500)/100.0f;
        state_y += (ydot * dt) + random(-500,500)/100.0f;
        state_theta += (thetadot * dt) + radians(random(-100,100)/100.0f);

        }
        else{

          BLA::Matrix<3,1> z_meas;
          z_meas(0,0) = state_x + random(-500,500)/100.0f;
          z_meas(1,0) = state_y + random(-500,500)/100.0f;
          z_meas(2,0) = state_theta + radians(random(-100,100)/100.0f);

          if(targetChanged){
            resetEKF(z_meas(0,0), z_meas(1,0), z_meas(2,0));
            targetChanged = !targetChanged;
          }

          ekfStep(v, rho, z_meas, dt);

          countX++;
          countY++;
          countT++;

          float xError = abs( z_meas(0,0) - xhat(0,0) );
          float yError = abs( z_meas(1,0) - xhat(1,0) );
          float tError = wrapToPi(z_meas(2,0) - xhat(2,0)); 

          avX += (xError - avX) / countX;
          avY += (yError - avY) / countY;
          avT += (fabs(tError)-avT) / countT;

          // Serial.printf("Average Errors: X = %.3f, Y = %.3f, Theta = %.3f\n",
          //     avX, avY, avT);

          bool xCheck = xError > 8;
          bool yCheck = yError > 8;
          bool thetaCheck = fabs(tError) > 3;
          bool anomalyDetected = xCheck || yCheck || thetaCheck;
          g_anomaly_detected = anomalyDetected;

          if( (anomalyDetected && kalman_correction) || !anomalyDetected){
            state_x     = xhat(0,0);
            state_y     = xhat(1,0);
            state_theta = xhat(2,0);
          }

          else if( anomalyDetected && !kalman_correction){
            state_x = z_meas(0,0);
            state_y = z_meas(1,0);
            state_theta = z_meas(2,0);
          }

        }
        
        while (state_theta < 0) state_theta += 2.0f * PI;
        while (state_theta >= 2.0f * PI) state_theta -= 2.0f * PI;


        if (state_x < 0.0f) state_x = 0.0f;
        if (state_x > 200.0f) state_x = 200.0f;
        if (state_y < 0.0f) state_y = 0.0f;
        if (state_y > 200.0f) state_y = 200.0f;
      }

      // Send updated pose back to Server
      if (millis() - lastPoseMs >= 200) {
        lastPoseMs = millis();
        if(encrypt_status){
          sendPoseEncrypted();
         }else{
          sendPose();
        }
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

        Serial.printf("[CLIENT] RECV  Speed = %.3f m/s  |  Rudder = %.2f deg  (raw: %u, %u)\n",
                      speed_m_s, rudder_deg, speed_counts, rudder_counts);
        Serial.printf("[CLIENT] POS   x=%.3f m  y=%.3f m  theta=%.4f rad (deg=%.2f)"
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
      DBG_PRINTF("[CLIENT] ERR  read feedback failed (%d/%d failures)\n", readFailures, readAttempts);
      
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