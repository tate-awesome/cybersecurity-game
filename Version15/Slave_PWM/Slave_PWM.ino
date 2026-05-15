// Version16
// - Including the control logic from PLC

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

// ---------- Modbus ----------
ModbusIP mb;

// ---------- PWM OUT -> PLC Analog Inputs (LEDC pins) ----------
const int PIN_X   = 4;     // to PLC AI1
const int PIN_Y   = 5;     // to PLC AI2
const int PIN_T   = 18;    // to PLC AI3

// ---------- PWM IN <- PLC PWM outputs (after level shifter to 3.3V) ----------
const int PIN_SPD = 6;    // from PLC Speed PWM (input capture)
const int PIN_RUD = 2;     // from PLC Rudder PWM (input capture)

// ---------- LEDC (ESP32 PWM) config ----------
const int LEDC_RES_BITS   = 12;    // resolution bits (0..4095)
const int LEDC_FREQ_HZ    = 500;   // PWM frequency (Hz) -> period = 2000 us

// ---------- Physical mappings ----------
const float X_RANGE_M       = 200.0f;   // full-scale X (meters)
const float Y_RANGE_M       = 200.0f;   // full-scale Y (meters)
const float SpeedMax_m_s    = 50.0f;     // maximum commanded speed (m/s)
const float RudderMax_deg   = 60.0f;    // maximum rudder deflection in degrees (±60°)

// ---------- Data structures for PWM capture ----------
struct PwmCapture {
  volatile uint32_t riseTime = 0;
  volatile uint32_t pulseWidth = 0;  // Time from rising to falling edge
  volatile uint32_t period   = 0;
  volatile bool     haveRise = false;
  volatile bool     newData  = false;
};

PwmCapture speedPWM, rudderPWM;

// ---------- Utility helpers ----------
static inline uint16_t clamp_u16(uint32_t v) { return (v > 65535u) ? 65535u : (uint16_t)v; }
static inline float clampf_local(float v, float lo, float hi) {
  if (isnan(v)) return lo;
  if (v < lo) return lo;
  if (v > hi) return hi;
  return v;
}

// Map physical position 0..200 m -> 12-bit duty 0..4095
static inline uint16_t phys_to_pwm12(float phys_0_200) {
  if (isnan(phys_0_200)) phys_0_200 = 0.0f;
  if (phys_0_200 < 0.0f) phys_0_200 = 0.0f;
  if (phys_0_200 > 200.0f) phys_0_200 = 200.0f;
  return (uint16_t)lroundf((phys_0_200 / 200.0f) * 4095.0f);
}

// ---------- Setup ----------
void setup() {
  Serial.begin(115200);
  delay(50);
  Serial.println("\n[SLAVE] Booting...");

  // WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("[SLAVE] Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.printf("\n[SLAVE] IP: %s\n", WiFi.localIP().toString().c_str());
  WiFi.setSleep(false);

  // Modbus server & regs
  mb.server();
  mb.addHreg(HREG_X_PHYS, 0);
  mb.addHreg(HREG_Y_PHYS, 0);
  mb.addHreg(HREG_THETA_MRAD, 0);
  mb.addHreg(HREG_SPEED, 0);
  mb.addHreg(HREG_RUDDER, 0);
  mb.addHreg(HREG_SPER, 0);
  mb.addHreg(HREG_RPER, 0);

  // Initialize safe defaults so slave shows sane values if Master isn't connected yet
  // Store scaled values (meters * 100) and theta (mrad)
  mb.Hreg(HREG_X_PHYS, (uint16_t)10000);    // 100.00 m -> 10000
  mb.Hreg(HREG_Y_PHYS, (uint16_t)010000;    // 100.00 m
  mb.Hreg(HREG_THETA_MRAD, (uint16_t)10000); // ~3.141 rad *1000

  // Setup LEDC using new ESP32 Core 3.x API
  // ledcAttach(pin, freq, resolution_bits)
  ledcAttach(PIN_X, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcAttach(PIN_Y, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcAttach(PIN_T, LEDC_FREQ_HZ, LEDC_RES_BITS);
  
  // Initialize to 0 duty (new API uses pin numbers directly)
  ledcWrite(PIN_X, 0);
  ledcWrite(PIN_Y, 0);
  ledcWrite(PIN_T, 0);

  // PWM inputs (from PLC)
  pinMode(PIN_SPD, INPUT_PULLUP);
  pinMode(PIN_RUD, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_SPD), isrSpeed, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_RUD), isrRudder, CHANGE);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Serial.println("[SLAVE] Ready.\n");
}

// ---------- Loop ----------
void loop() {
  mb.task();
  yield();

  // Add to Slave_PWM.ino setup()
mb.addHreg(20, 0); // HREG_PING

// Add to Slave_PWM.ino loop()
// The Modbus library handles Hreg storage automatically. 
// However, to ensure the Slave has "processed" it:
uint16_t pingIn = mb.Hreg(20); 
// We don't actually need to do anything else; mb.task() 
// handles the Master's read request for this same register.

// Interpret theta as signed milli-radians -> convert to radians
int16_t th_signed = (int16_t)h_th;        // permit negative if used

// clamp to physical ranges to be defensive
x_phys = clampf_local(x_phys, 0.0f, X_RANGE_M);
y_phys = clampf_local(y_phys, 0.0f, Y_RANGE_M);
// theta clamp to [0, 2*PI]
theta_rad = clampf_local(theta_rad, 0.0f, 2.0f * PI);

// --- 2) Convert physical commands to 12-bit LEDC duties ---
uint16_t x_pwm12 = phys_to_pwm12(x_phys);     // 0..4095
uint16_t y_pwm12 = phys_to_pwm12(y_phys);     // 0..4095
// Theta mapping: map 0..2*PI -> 0..4095
// PLC sends theta in range [0, 2*PI], stored as milli-radians
float theta_norm = theta_rad / (2.0f * PI);    // normalize to 0..1
theta_norm = clampf_local(theta_norm, 0.0f, 1.0f);
uint16_t t_pwm12 = (uint16_t)lroundf(theta_norm * 4095.0f);

// --- 3) Write to LEDC pins (new API uses pin numbers directly) ---
ledcWrite(PIN_X, x_pwm12);
ledcWrite(PIN_Y, y_pwm12);
ledcWrite(PIN_T, t_pwm12);

// --- 5) Debug / status print once a second ---
static uint32_t tPrint = 0;
if (millis() - tPrint > 1000) {
  tPrint = millis();

  // Compute last observed duty % for debug (showing actual active time)
  float spdDutyPct = 0.0f, rudDutyPct = 0.0f;
  uint32_t spdP = speedPWM.period, rudP = rudderPWM.period;
  uint32_t spdH = speedPWM.pulseWidth, rudH = rudderPWM.pulseWidth;
  
  // Calculate active (LOW) duty percentage
  if (spdP > 0 && spdH <= spdP && spdH > 0) {
    spdDutyPct = (1.0f - ((float)spdH / (float)spdP)) * 100.0f;
  }
  if (rudP > 0 && rudH <= rudP && rudH > 0) {
    rudDutyPct = (1.0f - ((float)rudH / (float)rudP)) * 100.0f;
  }

  // Print computed physical values, duties, and captures
  Serial.printf("X=%.3fm Y=%.3fm Th_rad=%.4f | pwm12: X=%u Y=%u T=%u | ",
                x_phys, y_phys, theta_rad, x_pwm12, y_pwm12, t_pwm12);

  Serial.printf("SpeedCmd=%.3f m/s (%.1f%% duty, %lu/%lu us) | Rudder=%.2f deg (%.1f%% duty, %lu/%lu us)\n",
                SpeedCmd_m_s, (double)spdDutyPct, 
                (unsigned long)(spdP - spdH), (unsigned long)spdP,
                RudderAngle_deg, (double)rudDutyPct, 
                (unsigned long)(rudP - rudH), (unsigned long)rudP);
}

  // Blink heartbeat LED
  static uint32_t tBlink = 0;
  if (millis() - tBlink > 500) {
    tBlink = millis();
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
  // tiny delay to yield (keeps loop friendly)
  delay(2);
}