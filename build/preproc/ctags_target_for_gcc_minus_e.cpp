# 1 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino"
// ════════════════════════════════════════════════════════════════════════
//  Combined Client — Submarine pose-tracking client + HVAC thermostat
//  client, in one sketch. Only one model's logic runs at a time; which one
//  is decided by AP_ESP32.ino's submarine_mode, polled continuously below.
//  This device never sets the mode itself — it only reads it.
// ════════════════════════════════════════════════════════════════════════


//#define DEBUG_SERIAL      // Comment out to disable debug output

# 12 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 13 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 14 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 15 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 16 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 17 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 18 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 19 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino" 2
# 34 "/home/martin/Desktop/cybersecurity-game/Testing-HVAC-Model/Combined_Client/Combined_Client.ino"
// ════════════════════════════════════════════════════════════════════════
//  SHARED — network, Modbus, mode sync. Identical regardless of which
//  model is active; neither Submarine nor HVAC needed a different WiFi
//  or Modbus setup, so none of this branches.
// ════════════════════════════════════════════════════════════════════════

const char* AP_SSID = "AP-Config";
const char* AP_PASSWORD = "admin1234";
const char* CONFIG_URL = "http://192.168.4.1/config";
const char* REST_URL = "http://192.168.4.1/data";

IPAddress serverIP(192, 168, 4, 10); // Server lives here regardless of mode
ModbusIP mb;

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Which model is currently active. Learned from the AP via syncModeFromAP()
// below — this device never sets it locally. Defaults true so behavior is
// unchanged if the AP can't be reached yet, matching HVAC_Server.ino's
// existing convention for the same flag.
bool g_submarine_mode = true;

// Generic Modbus holding-register write with one retry on timeout. Used by
// both models — neither needs anything register-specific baked in here.
bool writeH(uint16_t addr, uint16_t val) {
  if (!mb.isConnected(serverIP)) {
    ;
    return false;
  }
  for (int attempt = 0; attempt < 2; attempt++) {
    uint16_t tx = mb.writeHreg(serverIP, addr, val);
    if (!tx) {
      ;
      return false; // retrying won't help so exit immediately.
    }
    uint32_t start = millis();
    while (millis() - start < 300) {
      mb.task();
      if (!mb.isTransaction(tx)) return true;
      delay(3);
    }
    ;
    for (int i = 0; i < 5; i++) { mb.task(); delay(5); }
  }
  return false;
}

// Generic Modbus holding-register read with one retry on timeout.
bool readH(uint16_t addr, uint16_t* buf, uint16_t n) {
  if (!mb.isConnected(serverIP)) {
    ;
    return false;
  }
  for (int attempt = 0; attempt < 2; attempt++) {
    uint16_t tx = mb.readHreg(serverIP, addr, buf, n);
    if (!tx) {
      ;
      return false; // retrying won't help so bail immediately.
    }
    uint32_t start = millis();
    while (millis() - start < 300) {
      mb.task();
      if (!mb.isTransaction(tx)) return true;
    }
    ;
    for (int i = 0; i < 5; i++) { mb.task(); delay(5); }
  }
  return false;
}

void connectWifi() {
  WiFi.mode(WIFI_MODE_STA);
  WiFi.begin(AP_SSID, AP_PASSWORD);
  Serial0.print("[CLIENT] Connecting to ESP32-Config AP");

  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(300);
    Serial0.print(".");
  }
  Serial0.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial0.printf("[CLIENT] Connected to AP — IP: %s\n", WiFi.localIP().toString().c_str());
  } else {
    Serial0.println("[CLIENT] WiFi failed!");
    while (1) { delay(1000); }
  }

  WiFi.setSleep(false);
  Serial0.println("[CLIENT] WiFi sleep disabled");
}

void connectModbus() {
  mb.connect(serverIP);
  delay(500);
}

// Forward declaration — sendPoseAuto() is defined in the Submarine section
// below, but the shared reconnect logic needs to call it.
void sendPoseAuto();

void reconnectModbusIfNeeded() {
  if (mb.isConnected(serverIP)) return;

  static uint32_t lastTry = 0;
  if (millis() - lastTry > 2000) {
    lastTry = millis();
    Serial0.println("[CLIENT] Reconnecting Modbus...");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Reconnecting...");

    mb.connect(serverIP);
    if (mb.isConnected(serverIP)) {
      Serial0.println("[CLIENT] Reconnected successfully!");
      // Submarine re-establishes pose immediately on reconnect, matching
      // its original behavior. HVAC has no equivalent "push on reconnect"
      // step — its next 100ms tick handles that naturally.
      if (g_submarine_mode) {
        sendPoseAuto();
      }
    }
  }
}

// Polls AP_ESP32's /config — the single source of truth for which model
// should be active. Runs continuously regardless of which model's cycle
// function is currently executing, so a mode flip is always noticed even
// while the *other* model has been running for a while.
void syncModeFromAP() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(CONFIG_URL);
  int code = http.GET();
  if (code == HTTP_CODE_OK) {
    StaticJsonDocument<256> doc;
    if (!deserializeJson(doc, http.getString())) {
      if (doc.containsKey("submarine_mode")) {
        g_submarine_mode = doc["submarine_mode"].as<bool>();
      }
    }
  }
  http.end();
}

// ════════════════════════════════════════════════════════════════════════
//  SUBMARINE MODE — pose estimation, Kalman filtering, telemetry
// ════════════════════════════════════════════════════════════════════════

using namespace BLA;
bool filtering = true;

BLA::Matrix<3,1> xhat; // [x;y;heading angle]
BLA::Matrix<3,3> P; // covariance matrix
BLA::Matrix<3,3> R; // measurement noise matrix
BLA::Matrix<2,2> Qu; // control input noise
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
float state_speed = 0.0f;
float state_rudder = 0.0f;

const float L_vehicle = 0.07f;
const float K_theta = 0.6f;

const uint16_t HREG_X_PHYS = 10;
const uint16_t HREG_Y_PHYS = 11;
const uint16_t HREG_THETA_MRAD = 12;
const uint16_t HREG_SPEED = 3;
const uint16_t HREG_RUDDER = 4;

static int readAttempts = 0;
static int readFailures = 0;

static String key = (String)1234;

const float SpeedMax_m_s = 50.0f;
const float RudderMax_deg = 60.0f;


  const uint32_t REST_INTERVAL_MS = 2000;
  static uint32_t lastRestMs = 0;
  static bool encrypt_status = false;


float wrapToPi(float a) {
  while (a > 3.1415926535897932384626433832795) a -= 2.0f * 3.1415926535897932384626433832795;
  while (a < -3.1415926535897932384626433832795) a += 2.0f * 3.1415926535897932384626433832795;
  return a;
}

void ekfStep(float speed_m_s, float rudder_rad, const BLA::Matrix<3,1>& z_meas, float dt)
{
  // Predict
  BLA::Matrix<3,1> x_pred;
  float th = xhat(2,0);

  x_pred(0,0) = xhat(0,0) + speed_m_s * cos(th + rudder_rad) * dt;
  x_pred(1,0) = xhat(1,0) + speed_m_s * sin(th + rudder_rad) * dt;
  x_pred(2,0) = wrapToPi(xhat(2,0) + K_theta * (tan(rudder_rad) / L_vehicle) * dt);

  Matrix<3,3> F = {
    1, 0, -speed_m_s * sin(th + rudder_rad) * dt,
    0, 1, speed_m_s * cos(th + rudder_rad) * dt,
    0, 0, 1
  };

  Matrix<3,2> G = {
    cos(th + rudder_rad) * dt, -speed_m_s * sin(th + rudder_rad) * dt,
    sin(th + rudder_rad) * dt, speed_m_s * cos(th + rudder_rad) * dt,
    0, (K_theta * dt / L_vehicle) * (1.0f / (cos(rudder_rad) * cos(rudder_rad)))
  };

  Matrix<3,3> P_pred = F * P * ~F + G * Qu * ~G;

  // Update
  Matrix<3,3> S = P_pred + R; // H = I
  Matrix<3,3> K = P_pred * Inverse(S);

  Matrix<3,1> y = z_meas - x_pred;
  y(2,0) = wrapToPi(y(2,0));

  xhat = x_pred + K * y;
  xhat(2,0) = wrapToPi(xhat(2,0));

  P = (I3 - K) * P_pred;
}

static inline uint16_t x_to_u16_100(float v) {
  if (v < 0) v = 0;
  if (v > 200) v = 200;
  return (uint16_t)lroundf(v * 100.0f);
}

static inline uint16_t theta_to_mrad_u16(float t) {
  while (t < 0) t += 2.0f * 3.1415926535897932384626433832795;
  while (t >= 2.0f * 3.1415926535897932384626433832795) t -= 2.0f * 3.1415926535897932384626433832795;
  return (uint16_t)lroundf(t * 1000.0f);
}

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
  return (uint16_t)sum;
}

void sendPose() {
  uint16_t x_u = x_to_u16_100(state_x);
  uint16_t y_u = x_to_u16_100(state_y);
  uint16_t t_u = theta_to_mrad_u16(state_theta);

  if (writeH(HREG_X_PHYS, x_u) && writeH(HREG_Y_PHYS, y_u) && writeH(HREG_THETA_MRAD, t_u)) {
    // Success - values sent
  } else {
    Serial0.println("[CLIENT] ERR: Failed to send pose to Server");
  }
}

void sendPoseEncrypted(){
  uint16_t x_u = xorCipher(x_to_u16_100(state_x), keyToUint(key));
  uint16_t y_u = xorCipher(x_to_u16_100(state_y), keyToUint(key));
  uint16_t t_u = xorCipher(theta_to_mrad_u16(state_theta), keyToUint(key));

  bool x = writeH(HREG_X_PHYS, x_u);
  bool y = writeH(HREG_Y_PHYS, y_u);
  bool theta = writeH(HREG_THETA_MRAD, t_u);
  if (x && y && theta) {
    // Success - values sent
  } else {
    Serial0.print("[CLIENT] ERR: Failed to send pose to Server.");
  }
}

// Picks plain vs encrypted pose send based on current encrypt_status.
// Used by setup(), the reconnect path, and the periodic update — the
// original files repeated this if/else at all three call sites verbatim.
void sendPoseAuto() {
  if (encrypt_status) sendPoseEncrypted();
  else sendPose();
}

void initSubmarineState() {
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
}


void restPost() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(REST_URL);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<128> doc;
  doc["source"] = "client";
  doc["timestamp"] = (uint32_t)(millis() / 1000);
  doc["x"] = state_x;
  doc["y"] = state_y;
  doc["theta"] = state_theta;
  doc["speed"] = state_speed;
  doc["rudder"] = state_rudder;
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
    Serial0.printf("[CLIENT] REST POST failed  HTTP %d\n", code);
  }

  http.end();
}


// Runs the full Submarine pose-feedback cycle. Internally gated at ~20Hz
// for the Modbus feedback loop and its own slower timers for pose pushes,
// LCD updates, and REST posts — exactly the original timing, just no
// longer the only thing in loop().
void runSubmarineCycle() {
  static uint32_t lastReadS = 0;
  static uint32_t lastPoseMs = 0;
  if (millis() - lastReadS >= 50) { // Update at ~20Hz
    uint32_t currentMs = millis();
    lastReadS = currentMs;
    float dt = 0.05f;

    uint16_t rb[2];
    readAttempts++;
    if (readH(HREG_SPEED, rb, 2)) {

      if (encrypt_status) {
        xorArrayDecrypt(rb, keyToUint(key));
      }

      uint16_t speed_counts = rb[0];
      uint16_t rudder_counts = rb[1];

      float speed_m_s = (speed_counts / 4095.0f) * SpeedMax_m_s;
      float rudder_deg = ((rudder_counts / 4095.0f) - 0.5f) * 2.0f * RudderMax_deg;
      state_speed = speed_m_s;
      state_rudder = rudder_deg;

      if (fabs(speed_m_s) > 0.01f) {
        float v = speed_m_s;
        float rho = ((rudder_deg) * 0.017453292519943295769236907684886);

        if (!filtering) {
          float xdot = v * cos(rho + state_theta);
          float ydot = v * sin(rho + state_theta);
          float thetadot = 0.0f;

          if (fabs(rho) > 0.001f) {
            thetadot = K_theta / (L_vehicle / tan(rho));
          }

          state_x += (xdot * dt) + random(-500, 500) / 100.0f;
          state_y += (ydot * dt) + random(-500, 500) / 100.0f;
          state_theta += (thetadot * dt) + ((random(-100, 100) / 100.0f) * 0.017453292519943295769236907684886);

        } else {
          BLA::Matrix<3,1> z_meas;
          z_meas(0,0) = state_x + random(-500, 500) / 100.0f;
          z_meas(1,0) = state_y + random(-500, 500) / 100.0f;
          z_meas(2,0) = state_theta + ((random(-100, 100) / 100.0f) * 0.017453292519943295769236907684886);

          ekfStep(v, rho, z_meas, dt);

          bool xCheck = abs(z_meas(0,0) - xhat(0,0)) > 8;
          bool yCheck = abs(z_meas(1,0) - xhat(1,0)) > 8;
          float thetaError = wrapToPi(z_meas(2,0) - xhat(2,0));
          bool thetaCheck = fabs(thetaError) > 3;
          bool anomalyDetected = xCheck || yCheck || thetaCheck;
          g_anomaly_detected = anomalyDetected;

          if ((anomalyDetected && kalman_correction) || !anomalyDetected) {
            state_x = xhat(0,0);
            state_y = xhat(1,0);
            state_theta = xhat(2,0);
          } else if (anomalyDetected && !kalman_correction) {
            state_x = z_meas(0,0);
            state_y = z_meas(1,0);
            state_theta = z_meas(2,0);
          }
        }

        while (state_theta < 0) state_theta += 2.0f * 3.1415926535897932384626433832795;
        while (state_theta >= 2.0f * 3.1415926535897932384626433832795) state_theta -= 2.0f * 3.1415926535897932384626433832795;

        if (state_x < 0.0f) state_x = 0.0f;
        if (state_x > 200.0f) state_x = 200.0f;
        if (state_y < 0.0f) state_y = 0.0f;
        if (state_y > 200.0f) state_y = 200.0f;
      }

      if (millis() - lastPoseMs >= 200) {
        lastPoseMs = millis();
        sendPoseAuto();
      }

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
        lcd.print((char)223); // degree symbol
        lcd.print(" R:");
        lcd.print(rudder_counts);
      }

      static uint32_t lastPrint = 0;
      if (millis() - lastPrint > 1000) {
        lastPrint = millis();

        Serial0.printf("[CLIENT] RECV  Speed = %.3f m/s  |  Rudder = %.2f deg  (raw: %u, %u)\n",
                      speed_m_s, rudder_deg, speed_counts, rudder_counts);
        Serial0.printf("[CLIENT] POS   x=%.3f m  y=%.3f m  theta=%.4f rad (deg=%.2f)"

                        " e_stat=%d"

                        "\n",
                        state_x, state_y, state_theta, ((state_theta) * 57.295779513082320876798154814105)

                        , encrypt_status

          );
      }

    } else {
      readFailures++;
      ;

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


    if (millis() - lastRestMs >= REST_INTERVAL_MS) {
      lastRestMs = millis();
      restPost();
    }

}

// ════════════════════════════════════════════════════════════════════════
//  HVAC MODE — thermal physics simulation
// ════════════════════════════════════════════════════════════════════════

float true_room_temp = 71.6f; // Starts at 71.6°F (Equivalent to 22°C)
float state_damper = 0.0f;
float ambient_temp = 59.0f;

// Scale factor to preserve decimals across Modbus integer registers
// (e.g., 71.64°F -> 7164)
const float SCALE = 100.0f;

const uint16_t HREG_TEMP_EST = 10;
const uint16_t HREG_DAMPER_CMD = 3;

// Runs the HVAC thermal physics tick. Internally gated at 10Hz, matching
// HVAC_Client.ino's original rate. Now routed through the shared
// writeH()/readH() helpers instead of raw mb.readHreg()/writeHreg() calls —
// this also fixes the same "wrong transaction ID" class of bug we found
// and patched in the standalone HVAC_Client.ino earlier, by construction.
void runHvacCycle() {
  static uint32_t lastUpdate = 0;
  if (millis() - lastUpdate < 100) return;
  lastUpdate = millis();
  float dt = 0.1f;

  // 1. Read Damper Actuator Command from Server
  uint16_t raw_damper = 0;
  if (readH(HREG_DAMPER_CMD, &raw_damper, 1)) {
    state_damper = (float)raw_damper / 100.0f; // Decode 0-100% back to 0.0-1.0
  } else {
    ;
  }

  // Thermal Dynamics Physics Simulation
  float heat_loss = 0.05f * (true_room_temp - ambient_temp);
  float heat_gain = state_damper * 9.0f;

  true_room_temp += (heat_gain - heat_loss) * dt;
  true_room_temp += (random(-18, 19) / 100.0f); // Random physical perturbation (-0.18 to +0.18°F)

  // 3. Noisy Sensor Reading (Raw measurement)
  float noise = (random(-270, 271) / 100.0f); // -2.7°F to +2.7°F
  float noisy_measurement = true_room_temp + noise;

  // 4. Send RAW Noisy Measurement Directly to Server
  uint16_t tx_val = (uint16_t)lroundf(noisy_measurement * SCALE);
  if (!writeH(HREG_TEMP_EST, tx_val)) {
    ;
  }

  Serial0.printf("[CLIENT] True Room Temp: %.2f°F | Sent Raw Measurement: %.2f°F | Damper: %.1f%%\n",
                true_room_temp, noisy_measurement, state_damper * 100.0f);

  // Optional LCD readout for HVAC mode — the original HVAC_Client.ino had
  // no LCD output, but since this is the same physical board the Submarine
  // side already drives an LCD on, leaving it showing stale Submarine data
  // while HVAC is actually active would be confusing. Remove this block if
  // no LCD is wired up on the HVAC test rig.
  static uint32_t lastLcdUpdate = 0;
  if (millis() - lastLcdUpdate > 500) {
    lastLcdUpdate = millis();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("HVAC Room:");
    lcd.print(true_room_temp, 1);
    lcd.setCursor(0, 1);
    lcd.print("Damper:");
    lcd.print((int)(state_damper * 100.0f));
    lcd.print("%");
  }
}

// ════════════════════════════════════════════════════════════════════════
//  SETUP / LOOP
// ════════════════════════════════════════════════════════════════════════

void setup() {
  Serial0.begin(115200);
  delay(50);
  Serial0.println("\n[CLIENT] Booting (combined Submarine/HVAC)...");

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Client Init...");

  lcd.setCursor(0, 1);
  lcd.print("WiFi connect...");
  connectWifi();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi: OK");
  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());
  delay(1500);

  // Submarine state init runs unconditionally — the mode could flip to
  // SUBMARINE at any point after boot, so the Kalman filter needs to be
  // ready regardless of which model starts out active.
  initSubmarineState();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connect Server..");
  connectModbus();

  if (mb.isConnected(serverIP)) {
    Serial0.println("[CLIENT] Connected to Server Modbus.");
    lcd.setCursor(0, 1);
    lcd.print("Server: OK");
    delay(500);
    sendPoseAuto(); // Matches original setup() behavior — harmless if
                       // HVAC turns out to be the active mode, since the
                       // Server simply ignores registers it's not using.
  } else {
    Serial0.println("[CLIENT] WARNING: Could not connect to Server initially.");
    lcd.setCursor(0, 1);
    lcd.print("Server: FAIL");
    delay(1000);
  }

  syncModeFromAP(); // Best-effort initial mode read before loop() starts
  lcd.clear();
}

void loop() {
  mb.task();
  yield();

  reconnectModbusIfNeeded();
  if (!mb.isConnected(serverIP)) {
    delay(10);
    return;
  }

  static uint32_t lastModeSync = 0;
  if (millis() - lastModeSync >= 1000) {
    lastModeSync = millis();
    syncModeFromAP();
  }

  if (g_submarine_mode) {
    runSubmarineCycle();
  } else {
    runHvacCycle();
  }

  delay(5);
}
