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

const uint16_t HREG_X_PHYS       = 10;
const uint16_t HREG_Y_PHYS       = 11;
const uint16_t HREG_THETA_MRAD   = 12;

const uint16_t HREG_SPEED        = 3; // Receiving from master
const uint16_t HREG_RUDDER       = 4; // Receiving from master
const uint16_t HREG_SPER         = 5;
const uint16_t HREG_RPER         = 6;

const float HEAD_OFFSET_M = 0.0f;     // Head position offset from vehicle center
const float Kps = 0.1f;                 // Speed proportional gain
const float Kp_rudder = 0.1f;          // Rudder proportional gain
const float SpeedMax = 50.0f;           // Maximum speed (m/s)
const float StopTol = 1.0f;             // Stop tolerance (meters)

const int PIN_X   = 4;     // to PLC AI1
const int PIN_Y   = 5;     // to PLC AI2
const int PIN_T   = 18;    // to PLC AI3


// ---------- PWM IN FORM PLC
const int PIN_TARGET_X = 6;  // Target X from PLC HMI
const int PIN_TARGET_Y = 2;  // Target Y from PLC HMI

// ---------- LEDC (ESP32 PWM) config ----------
const int LEDC_RES_BITS   = 12;    // resolution bits (0..4095)
const int LEDC_FREQ_HZ    = 500;   // PWM frequency (Hz) -> period = 2000 us

// ---------- Physical mappings ----------
const float X_RANGE_M       = 200.0f;   // full-scale X (meters)
const float Y_RANGE_M       = 200.0f;   // full-scale Y (meters)
const float RudderMax_deg   = 60.0f;    // maximum rudder deflection in degrees (±60°)

#ifndef LED_BUILTIN
  #define LED_BUILTIN 2  // Change to the correct GPIO for your specific board (often 2 or 5)
#endif

// ---------- Data structures for PWM capture ----------
struct PwmCapture {
  volatile uint32_t riseTime = 0;
  volatile uint32_t pulseWidth = 0;  // Time from rising to falling edge
  volatile uint32_t period   = 0;
  volatile bool     haveRise = false;
  volatile bool     newData  = false;
  volatile uint32_t seq = 0;  
};

PwmCapture targetXPWM, targetYPWM;

void IRAM_ATTR isrTargetX() {
  uint32_t now = micros();
  int state = digitalRead(PIN_TARGET_X);
  
  if (state == HIGH) { // Rising edge
    if (targetXPWM.haveRise) {
      targetXPWM.period = now - targetXPWM.riseTime; // Captured a full cycle
    }
    targetXPWM.riseTime = now;
    targetXPWM.haveRise = true;
  } else { // Falling edge
    if (targetXPWM.haveRise) {
      targetXPWM.seq++;
      targetXPWM.pulseWidth = now - targetXPWM.riseTime;
      targetXPWM.newData = true;
    }
  }
}

void IRAM_ATTR isrTargetY() {
  uint32_t now = micros();
  int state = digitalRead(PIN_TARGET_Y);
  
  if (state == HIGH) { // Rising edge
    if (targetYPWM.haveRise) {
      targetYPWM.period = now - targetYPWM.riseTime;
    }
    targetYPWM.riseTime = now;
    targetYPWM.haveRise = true;
  } else { // Falling edge
    if (targetYPWM.haveRise) {
      targetYPWM.seq++;
      targetYPWM.pulseWidth = now - targetYPWM.riseTime;
      targetYPWM.newData = true;
    }
  }
}

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

  // --- Helper Function: atan2 Approximation ---
  float atan2_approx(float y, float x) {
    // Handle near-zero inputs
    if (fabs(x) < 0.001f && fabs(y) < 0.001f) {
      return 0.0f;
    }
    
    // Get absolute values
    float ax = fabs(x);
    float ay = fabs(y);
    
    // Determine dominant axis
    float m, n;
    bool cond_m;
    if (ax > ay) {
      m = ax;
      n = ay;
      cond_m = true;
    } else {
      m = ay;
      n = ax;
      cond_m = false;
    }
    
    // Ratio for approximation
    float r = n / (m + 0.001f);
    
    // atan approximation
    float approx;
    if (cond_m) {
      approx = r / (1.0f + 0.28f * r * r);
    } else {
      approx = (PI / 2.0f) - r / (1.0f + 0.28f * r * r);
    }
    
    // Quadrant correction
    float ThetaDes = approx;
    if (x < 0 && y >= 0) {
      ThetaDes = PI - approx;
    } else if (x < 0 && y < 0) {
      ThetaDes = -(PI - approx);
    } else if (x >= 0 && y < 0) {
      ThetaDes = -approx;
    }
    
    return ThetaDes;
  }

  // --- Helper Function: Wrap Angle to [-PI, PI] ---
  float wrap_to_pi(float angle) {
    while (angle > PI) {
      angle -= 2.0f * PI;
    }
    while (angle < -PI) {
      angle += 2.0f * PI;
    }
    return angle;
  }

void computeControlCommands(float target_x, float target_y, 
                          float state_x, float state_y, float state_theta,
                          float* speed_out, float* rudder_out) {
  
  // 1. Compute head position (offset from vehicle center)
  float head_x = state_x + HEAD_OFFSET_M * cos(state_theta);
  float head_y = state_y + HEAD_OFFSET_M * sin(state_theta);
  
  // 2. Position errors (target relative to head position)
  float Xerr = target_x - head_x;
  float Yerr = target_y - head_y;
  // Serial.printf("Xerror  Speed=%.2f m/s (%u counts) | Rudder=%.2f° (%u counts)\n",
  //                 SpeedCmd_m_s, spd_counts, RudderAngle_deg, rud_counts);
  
  // 3. Get absolute values
  float ax = fabs(Xerr);
  float ay = fabs(Yerr);
  
  // 4. Calculate desired heading using atan2 approximation
  float ThetaDes = atan2_approx(Yerr, Xerr); // changed from Yerr, Xerr
  
  // 5. Heading error (wrap to -PI...+PI)
  float HeadingErr = ThetaDes - state_theta;
  HeadingErr = wrap_to_pi(HeadingErr);
  
  // 6. Rudder command (proportional control)
  float rho_rad = Kp_rudder * HeadingErr;
  
  // Clamp rudder to ±π/3 (±60°)
  if (rho_rad >= PI / 3.0f) {
    rho_rad = PI / 3.0f;
  } else if (rho_rad <= -PI / 3.0f) {
    rho_rad = -PI / 3.0f;
  }
  float center_dist = sqrt(pow(target_x - head_x, 2) + pow(target_y - head_y, 2));
  
  // 7. Distance approximation (avoids sqrt)
  // float m, n;
  // if (ax > ay) {
  //   m = ax;
  //   n = ay;
  // } else {
  //   m = ay;
  //   n = ax;
  // }
  float SpeedCmd = 0;
  //float dist = sqrt((ax*ax)+(ay*ay));

  // 8. Speed command (proportional control)
  SpeedCmd = Kps * center_dist;

  
  // Clamp to SpeedMax
  if (SpeedCmd > SpeedMax) {
    SpeedCmd = SpeedMax;
  }
  
  // 9. Stop condition
  if (center_dist < StopTol) {
    SpeedCmd = 0.0f;
    rho_rad = 0.0f;
  }
  
  // 10. Convert rudder from radians to degrees for output
  *speed_out = SpeedCmd;  // m/s
  *rudder_out = rho_rad * 180.0f / PI;  // degrees
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
  mb.Hreg(HREG_Y_PHYS, (uint16_t)10000);    // 100.00 m
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
  pinMode(PIN_TARGET_X, INPUT_PULLUP);
  pinMode(PIN_TARGET_Y, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_TARGET_X), isrTargetX, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_TARGET_Y), isrTargetY, CHANGE);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Serial.println("[SLAVE] Ready.\n");
}

// ---------- Loop ----------
void loop() {
  static uint32_t lastLoopTime = 0;
  uint32_t loopStart = micros();
  mb.task();
  yield();

  uint16_t raw_h_x = mb.Hreg(HREG_X_PHYS);
  uint16_t raw_h_y = mb.Hreg(HREG_Y_PHYS);

  static uint16_t last_raw_x = 0;
  if (raw_h_x != last_raw_x) {
      Serial.printf("[DEBUG-MB] Master updated HREG_X: %u (Previous: %u)\n", raw_h_x, last_raw_x);
      last_raw_x = raw_h_x;
  }

  // --- 1) Read Current State from Master via Modbus ---
  uint16_t h_x = mb.Hreg(HREG_X_PHYS);
  uint16_t h_y = mb.Hreg(HREG_Y_PHYS);
  uint16_t h_th = mb.Hreg(HREG_THETA_MRAD);

  if (h_x == 0 && h_y == 0 && h_th == 0) {
  Serial.println("[SLAVE] WARNING: Received all zeros from Master - using last valid state");
  return;  // Skip this cycle
  }

  if (h_x > 20000 || h_y > 20000) {
    Serial.printf("[SLAVE] WARNING: Invalid position from Master: X=%u Y=%u - ignoring\n", h_x, h_y);
    return;  // Skip this cycle
  }

  // Convert to physical units
  static float state_x = 100.0f;      // Current vehicle X position (meters)
  static float state_y = 100.0f;      // Current vehicle Y position (meters)
  static float state_theta = 0.0f;    // Current vehicle heading (radians)
  
  state_x = ((int32_t)h_x) / 100.0f;    // meters
  state_y = ((int32_t)h_y) / 100.0f;    // meters
  
  // Interpret theta as signed milli-radians -> convert to radians
  int16_t th_signed = (int16_t)h_th;
  state_theta = ((float)th_signed) / 1000.0f;  // mrad -> rad

  // Clamp to physical ranges
  state_x = clampf_local(state_x, 0.0f, X_RANGE_M);
  state_y = clampf_local(state_y, 0.0f, Y_RANGE_M);
  state_theta = clampf_local(state_theta, 0.0f, 2.0f * PI);

  // --- 2) Output Current State to PLC for HMI Display ---
  uint16_t x_pwm12 = phys_to_pwm12(state_x);     // 0..4095
  uint16_t y_pwm12 = phys_to_pwm12(state_y);     // 0..4095
  
  // Theta mapping: 0..2*PI -> 0..4095
  float theta_norm = state_theta / (2.0f * PI);    // normalize to 0..1
  theta_norm = clampf_local(theta_norm, 0.0f, 1.0f);
  uint16_t t_pwm12 = (uint16_t)lroundf(theta_norm * 4095.0f);

  ledcWrite(PIN_X, x_pwm12);
  ledcWrite(PIN_Y, y_pwm12);
  ledcWrite(PIN_T, t_pwm12);

  // --- 3) Capture Target Position from PLC PWM Inputs ---
  static float target_x = 100.0f;
  static float target_y = 100.0f;

  if (targetXPWM.newData) {
  uint32_t h, p, s1, s2;
  
  // Atomic read with sequence check - retry if interrupted
  do {
    noInterrupts();
    s1 = targetXPWM.seq;
    h = targetXPWM.pulseWidth;
    p = targetXPWM.period;
    s2 = targetXPWM.seq;
    interrupts();
  } while (s1 != s2);  // If seq changed, we got interrupted - retry
  
  // Clear flag after successful read
  noInterrupts();
  targetXPWM.newData = false;
  interrupts();

  // --- Inside if (targetXPWM.newData) ---
  if (p < 3000 || p > 5000) {
      Serial.printf("[DEBUG-PWM] TIMING GLITCH! Period: %lu us, Pulse: %lu us, Seq: %lu\n", 
                    (unsigned long)p, (unsigned long)h, (unsigned long)s1);
  }

  if (p > 3000 && p < 5000 && h > 0 && h <= p) {
    float duty = 1.0f - ((float)h / (float)p);
    duty = clampf_local(duty, 0.10f, 0.90f);
    // target_x = ((duty - 0.10f) / 0.80f) * X_RANGE_M;
    target_x = 100;
  }
}

// Same for Target Y:
if (targetYPWM.newData) {
  uint32_t h, p, s1, s2;
  
  // Atomic read with sequence check
  do {
    noInterrupts();
    s1 = targetYPWM.seq;
    h = targetYPWM.pulseWidth;
    p = targetYPWM.period;
    s2 = targetYPWM.seq;
    interrupts();
  } while (s1 != s2);
  
  // Clear flag after successful read
  noInterrupts();
  targetYPWM.newData = false;
  interrupts();

  if (p > 3000 && p < 5000 && h > 0 && h <= p) {
    float duty = 1.0f - ((float)h / (float)p);
    duty = clampf_local(duty, 0.10f, 0.90f);
    //target_y = ((duty - 0.10f) / 0.80f) * Y_RANGE_M;
    target_y = 100;
  }
}

  // // Process Target X PWM
  // if (targetXPWM.newData) {
  //   noInterrupts();
  //   uint32_t h = targetXPWM.pulseWidth;
  //   uint32_t p = targetXPWM.period;
  //   targetXPWM.newData = false;
  //   interrupts();

  //   if (p > 3000 && p < 5000 && h > 0 && h <= p) {
  //     // Active-low PWM: invert the duty cycle
  //     float duty = 1.0f - ((float)h / (float)p);
      
  //     // Clamp to expected range 0.10 to 0.90 (10-90%)
  //     duty = clampf_local(duty, 0.10f, 0.90f);
      
  //     // Map 10-90% duty to 0-200m range
  //     target_x = ((duty - 0.10f) / 0.80f) * X_RANGE_M;
  //   }
  // }

  // // Process Target Y PWM
  // if (targetYPWM.newData) {
  //   noInterrupts();
  //   uint32_t h = targetYPWM.pulseWidth;
  //   uint32_t p = targetYPWM.period;
  //   targetYPWM.newData = false;
  //   interrupts();

  //   if (p > 3000 && p < 5000 && h > 0 && h <= p) {
  //     // Active-low PWM: invert the duty cycle
  //     float duty = 1.0f - ((float)h / (float)p);
      
  //     // Clamp to expected range 0.10 to 0.90 (10-90%)
  //     duty = clampf_local(duty, 0.10f, 0.90f);
      
  //     // Map 10-90% duty to 0-200m range
  //     target_y = ((duty - 0.10f) / 0.80f) * Y_RANGE_M;
  //   }
  // }

  // --- 4) Run Controller Logic (Placeholder - will be added next) ---
  static float SpeedCmd_m_s = 0.0f;
  static float RudderAngle_deg = 0.0f;

  computeControlCommands(target_x, target_y, 
                        state_x, state_y, state_theta,
                        &SpeedCmd_m_s, &RudderAngle_deg);

  // --- 5) Publish Speed and Rudder Commands to Modbus for Master ---
  
  // Convert Speed to Modbus counts (0-4095 representing 0-50 m/s)
  float speed_normalized = SpeedCmd_m_s / SpeedMax;  // 0..1
  speed_normalized = clampf_local(speed_normalized, 0.0f, 1.0f);
  uint16_t spd_counts = (uint16_t)lroundf(speed_normalized * 4095.0f);
  mb.Hreg(HREG_SPEED, spd_counts);
  
  // Convert Rudder to Modbus counts (0-4095 representing -60° to +60°)
  float rudder_normalized = (RudderAngle_deg / RudderMax_deg + 1.0f) / 2.0f;  // -60..+60 -> 0..1
  rudder_normalized = clampf_local(rudder_normalized, 0.0f, 1.0f);
  uint16_t rud_counts = (uint16_t)lroundf(rudder_normalized * 4095.0f);
  mb.Hreg(HREG_RUDDER, rud_counts);

  // --- 6) Debug / status print once a second ---
  static uint32_t tPrint = 0;
  if (millis() - tPrint > 1000) {
    tPrint = millis();

    // Compute last observed duty % for Target inputs
    float targetXDuty = 0.0f, targetYDuty = 0.0f;
    uint32_t txP = targetXPWM.period, tyP = targetYPWM.period;
    uint32_t txH = targetXPWM.pulseWidth, tyH = targetYPWM.pulseWidth;
    
    if (txP > 0 && txH <= txP && txH > 0) {
      targetXDuty = (1.0f - ((float)txH / (float)txP)) * 100.0f;
    }
    if (tyP > 0 && tyH <= tyP && tyH > 0) {
      targetYDuty = (1.0f - ((float)tyH / (float)tyP)) * 100.0f;
    }

    Serial.printf("[SLAVE] State: X=%.2fm Y=%.2fm Θ=%.3frad | Target: X=%.2fm Y=%.2fm\n",
                  state_x, state_y, state_theta, target_x, target_y);
    
    Serial.printf("[SLAVE] Target PWM: X=%.1f%% (%lu/%lu us) | Y=%.1f%% (%lu/%lu us)\n",
                  (double)targetXDuty, (unsigned long)(txP - txH), (unsigned long)txP,
                  (double)targetYDuty, (unsigned long)(tyP - tyH), (unsigned long)tyP);

    // Calculate the real meter values from the duty cycle
    
    Serial.printf("[SLAVE] Commands: Speed=%.2f m/s (%u counts) | Rudder=%.2f° (%u counts)\n",
                  SpeedCmd_m_s, spd_counts, RudderAngle_deg, rud_counts);
  }

  // Blink heartbeat LED
  static uint32_t tBlink = 0;
  if (millis() - tBlink > 500) {
    tBlink = millis();
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }

  uint32_t loopDuration = micros() - loopStart;
  if (loopDuration > 5000) { // If loop takes longer than 5ms
      Serial.printf("[DEBUG-PERF] Long Loop Detected: %lu us\n", (unsigned long)loopDuration);
  }

  delay(2);
}