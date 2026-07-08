#include <Arduino.h>
#include <WiFi.h>
#include <Preferences.h>          // NVS (non-volatile) storage
#include <ESPAsyncWebServer.h>    // Async web server
#include <HTTPClient.h>           // Forward requests to Flask
#include <DNSServer.h>
#include <map>
#include <ArduinoJson.h>          // JSON relay parsing

// ─── Soft-AP credentials (permanent, never change) ───────────
const char* AP_SSID     = "AP-Config";
const char* AP_PASSWORD = "admin1234";
const IPAddress AP_IP   (192, 168, 4, 1);
const IPAddress AP_GW   (192, 168, 4, 1);
const IPAddress AP_SUBNET(255, 255, 255, 0);

DNSServer dnsServer;
const byte DNS_PORT = 53;

// ─── NVS key names ────────────────────────────────────────────
#define NVS_NAMESPACE   "netcfg"
#define NVS_KEY_SSID    "ssid"
#define NVS_KEY_PASS    "password"
#define NVS_KEY_FLASK   "flask_ip"

// ─── Globals ──────────────────────────────────────────────────
Preferences   prefs;
AsyncWebServer server(80);
bool g_submarine_mode = true;

String g_ssid     = "";
String g_password = "";
String g_flask_ip = "192.168.8.167";


String g_client_payload = "{}";
String g_server_payload = "{}";

#define MAX_POINTS 20 

struct DeviceInfo {
  String ip;
  uint32_t lastSeenMs;
  int pointCount;
};
std::map<String, DeviceInfo> g_devices;

StaticJsonDocument<8192> g_client_doc;  // stores array of points
StaticJsonDocument<8192> g_server_doc;
JsonArray g_client_arr = g_client_doc.to<JsonArray>();
JsonArray g_server_arr = g_server_doc.to<JsonArray>();

bool g_encryption_status = false;
String g_encryption_key  = "1234";
float g_target_x = 100.0;
float g_target_y = 100.0;

bool g_filter_correction = false;
float g_target_temp = 75.2f;

// Live HVAC readings, reported in by HVAC_Server.ino's /hvac_status posts.
// AP doesn't compute these itself — it just relays whatever the Server last sent.
float g_current_room_temp = 0.0f;
bool  g_heater_on          = false;

// ─── Live submarine telemetry position ─────────────────────────
//   Most recent (x, y) reported by each source via POST /data.
//   NOTE: this assumes the incoming /data payload includes numeric
//   "x" and "y" fields — adjust the field names below if the
//   Submarine_Client/Submarine_Server sketches use different keys.
bool  g_has_client_live = false;
float g_client_live_x   = 0.0f;
float g_client_live_y   = 0.0f;
bool  g_has_server_live = false;
float g_server_live_x   = 0.0f;
float g_server_live_y   = 0.0f;
bool  g_has_live_speed  = false;
float g_live_speed      = 0.0f;
bool  g_has_live_rudder = false;
float g_live_rudder     = 0.0f;



// ─── HVAC temperature history (for the setpoint-vs-live chart) ─
#define HVAC_HISTORY_LEN 40
struct HvacSample {
  uint32_t ms;
  float    room;
  float    target;
};
HvacSample g_hvac_history[HVAC_HISTORY_LEN];
int g_hvac_history_count = 0;
int g_hvac_history_head  = 0;   // circular buffer write index

void recordHvacSample(float room, float target) {
  g_hvac_history[g_hvac_history_head] = { millis(), room, target };
  g_hvac_history_head = (g_hvac_history_head + 1) % HVAC_HISTORY_LEN;
  if (g_hvac_history_count < HVAC_HISTORY_LEN) g_hvac_history_count++;
}

// ─── Forward declarations ─────────────────────────────────────
void loadPreferences();
void savePreferences(const String& ssid, const String& pass, const String& flask_ip);
void startAP();
//void connectSTA();
void setupRoutes();
String buildConfigPage();
void forwardToFlask(const String& endpoint, const String& body);

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n[AP] Booting...");

  loadPreferences();
  startAP();

  g_client_arr = g_client_doc.to<JsonArray>();
  g_server_arr = g_server_doc.to<JsonArray>();
  recordHvacSample(g_current_room_temp, g_target_temp);

  setupRoutes();
  server.begin();
  Serial.println("[AP] Web server started on http://192.168.4.1");
}

void loop() {
  dnsServer.processNextRequest();
  delay(10);
}

void loadPreferences() {
  prefs.begin(NVS_NAMESPACE, true);   // read-only
  g_ssid     = prefs.getString(NVS_KEY_SSID,  "");
  g_password = prefs.getString(NVS_KEY_PASS,  "");
  g_flask_ip = prefs.getString(NVS_KEY_FLASK, "192.168.8.167");
  prefs.end();

  Serial.printf("[AP] Loaded NVS — SSID: '%s'  Flask: '%s'\n",g_ssid.c_str(), g_flask_ip.c_str());
}

void savePreferences(const String& ssid, const String& pass, const String& flask_ip) {
  prefs.begin(NVS_NAMESPACE, false);  // read-write
  prefs.putString(NVS_KEY_SSID,  ssid);
  prefs.putString(NVS_KEY_PASS,  pass);
  prefs.putString(NVS_KEY_FLASK, flask_ip);
  prefs.end();
  Serial.println("[AP] Preferences saved to NVS.");
}

void startAP() {
  WiFi.mode(WIFI_AP);   // ← was WIFI_AP_STA
  WiFi.softAPConfig(AP_IP, AP_GW, AP_SUBNET);
  WiFi.softAP(AP_SSID, AP_PASSWORD);
  Serial.printf("[AP] Soft-AP started: SSID='%s'  IP=%s\n", AP_SSID, WiFi.softAPIP().toString().c_str());

  //captive portal
  dnsServer.start(DNS_PORT, "*", AP_IP);
  Serial.println("[AP] Captive portal DNS started.");
}

// ============================================================
//  HTML Config Page
// ============================================================
String buildConfigPage() {
      String html = R"rawhtml(
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Access Point Network Configuration</title>
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          font-family: 'Segoe UI', Arial, sans-serif;
          background: #1a1a2e;
          color: #e0e0e0;
          min-height: 100vh;
          display: flex;
          align-items: flex-start;
          justify-content: center;
          padding: 20px;
        }

        .layout {
          display: flex;
          gap: 16px;
          width: 100%;
          max-width: 960px;
          flex-wrap: wrap;
        }

        .column {
          flex: 1;
          min-width: 280px;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .card {
          background: #16213e;
          border: 1px solid #0f3460;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }

        .header {
          display: flex;
          align-items: center;
          gap: 12px;
          padding-bottom: 16px;
          border-bottom: 1px solid #0f3460;
          margin-bottom: 16px;
        }

        .header-icon { font-size: 24px; }

        h1 {
          font-size: 1.1rem;
          color: #e94560;
          letter-spacing: 0.5px;
        }

        h1 span {
          display: block;
          font-size: 0.72rem;
          color: #888;
          font-weight: normal;
          margin-top: 2px;
        }

        .section-title {
          font-size: 0.70rem;
          text-transform: uppercase;
          letter-spacing: 1.5px;
          color: #e94560;
          margin-bottom: 12px;
          margin-top: 20px;
        }

        .section-title:first-child { margin-top: 0; }

        .form-group { margin-bottom: 14px; }

        label {
          display: block;
          font-size: 0.80rem;
          color: #aaa;
          margin-bottom: 5px;
        }

        input[type="text"],
        input[type="password"] {
          width: 100%;
          padding: 9px 12px;
          background: #0a0a1a;
          border: 1px solid #0f3460;
          border-radius: 8px;
          color: #e0e0e0;
          font-size: 0.90rem;
          outline: none;
          transition: border-color 0.2s;
        }

        input:focus { border-color: #e94560; }
        input::placeholder { color: #444; }

        .btn {
          width: 100%;
          padding: 10px;
          border: none;
          border-radius: 8px;
          font-size: 0.95rem;
          font-weight: 600;
          cursor: pointer;
          margin-top: 6px;
          transition: opacity 0.2s, transform 0.1s;
        }

        .btn-mode {
          padding: 3px 10px;
          border: 1px solid #e94560;
          border-radius: 6px;
          background: transparent;
          color: #e94560;
          font-size: 0.72rem;
          font-weight: 600;
          cursor: pointer;
          letter-spacing: 0.5px;
          transition: background 0.2s, color 0.2s;
        }
        .btn-mode:hover {
          background: #e94560;
          color: #fff;
        }

        .btn:active { transform: scale(0.98); }
        .btn-primary { background: #e94560; color: #fff; margin-top: 20px; }
        .btn-primary:hover { opacity: 0.9; }
        .btn-secondary { background: #0f3460; color: #e0e0e0; margin-top: 8px; }
        .btn-secondary:hover { opacity: 0.85; }

        .toast {
          display: none;
          background: #0f3460;
          border-left: 3px solid #e94560;
          border-radius: 6px;
          padding: 9px 12px;
          font-size: 0.82rem;
          margin-top: 14px;
        }

        /* ── Status Panel ── */
        .stat-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 10px;
          margin-bottom: 4px;
        }

        .stat-box {
          background: #0a0a1a;
          border: 1px solid #0f3460;
          border-radius: 8px;
          padding: 10px 12px;
          text-align: center;
        }

        .stat-value {
          font-size: 1.4rem;
          font-weight: 700;
          color: #e94560;
          line-height: 1.2;
        }

        .stat-label {
          font-size: 0.68rem;
          color: #888;
          text-transform: uppercase;
          letter-spacing: 0.8px;
          margin-top: 2px;
        }

        .status-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 6px 0;
          border-bottom: 1px solid #0f3460;
          font-size: 0.82rem;
        }

        .status-row:last-child { border-bottom: none; }
        .status-key { color: #888; }
        .status-val { color: #e0e0e0; font-weight: 500; }
        .status-val.green { color: #4caf50; }
        .status-val.red   { color: #e94560; }

        /* ── Device Table ── */
        .device-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 0.80rem;
          margin-top: 4px;
        }

        .device-table th {
          text-align: left;
          color: #888;
          font-weight: normal;
          font-size: 0.70rem;
          text-transform: uppercase;
          letter-spacing: 0.8px;
          padding: 4px 6px 8px;
          border-bottom: 1px solid #0f3460;
        }

        .device-table td {
          padding: 8px 6px;
          border-bottom: 1px solid #0a0a1a;
          color: #e0e0e0;
        }

        .device-table tr:last-child td { border-bottom: none; }

        .dot {
          display: inline-block;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          margin-right: 6px;
        }

        .dot-green { background: #4caf50; }
        .dot-yellow { background: #ff9800; }
        .dot-red { background: #e94560; }

        .no-devices {
          text-align: center;
          color: #555;
          font-size: 0.82rem;
          padding: 16px 0;
        }

        .footer {
          font-size: 0.72rem;
          color: #555;
          text-align: center;
          margin-top: 16px;
        }

        /* ── Tabs ── */
        .tab-bar {
          display: flex;
          gap: 8px;
          max-width: 960px;
          width: 100%;
          margin: 0 auto 16px;
        }

        .tab-btn {
          flex: 1;
          padding: 12px;
          background: #16213e;
          border: 1px solid #0f3460;
          border-radius: 10px;
          color: #888;
          font-size: 0.85rem;
          font-weight: 600;
          letter-spacing: 0.3px;
          cursor: pointer;
          transition: color 0.2s, border-color 0.2s, background 0.2s;
        }

        .tab-btn:hover { color: #ccc; }

        .tab-btn.active {
          color: #fff;
          background: #e94560;
          border-color: #e94560;
        }

        .tab-panel { display: none; }
        .tab-panel.active { display: block; }

        .page-wrap {
          width: 100%;
          max-width: 960px;
          margin: 0 auto;
        }

        /* ── Model cards (Submarine vs HVAC) ── */
        .mode-banner {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
        }

        .mode-banner-text {
          font-size: 0.80rem;
          color: #aaa;
          max-width: 560px;
          line-height: 1.4;
        }

        .mode-banner-text strong { color: #e0e0e0; }

        .model-badge {
          display: inline-block;
          font-size: 0.62rem;
          font-weight: 700;
          letter-spacing: 0.6px;
          text-transform: uppercase;
          padding: 3px 8px;
          border-radius: 20px;
          margin-left: 8px;
          vertical-align: middle;
        }

        .badge-active {
          background: rgba(76, 175, 80, 0.15);
          color: #4caf50;
          border: 1px solid #4caf50;
        }

        .badge-inactive {
          background: rgba(136, 136, 136, 0.12);
          color: #888;
          border: 1px solid #444;
        }

        .model-card {
          position: relative;
          border-width: 1px;
          transition: opacity 0.25s, border-color 0.25s;
        }

        .model-card.model-active {
          border-color: #e94560;
        }

        .model-card.model-inactive {
          opacity: 0.45;
        }

        .model-card.model-inactive input,
        .model-card.model-inactive button {
          pointer-events: none;
        }

        .model-note {
          font-size: 0.70rem;
          color: #666;
          margin-top: 10px;
          line-height: 1.4;
        }

        /* ── Target mini-map ── */
        .minimap-wrap {
          margin: 12px 0 14px;
        }

        .minimap-svg {
          width: 100%;
          height: 160px;
          background: #0a0a1a;
          border: 1px solid #0f3460;
          border-radius: 8px;
          display: block;
        }

        .minimap-caption {
          font-size: 0.65rem;
          color: #555;
          text-align: right;
          margin-top: 4px;
        }

        .legend-row {
          display: flex;
          gap: 14px;
          flex-wrap: wrap;
          margin-top: 8px;
          font-size: 0.68rem;
          color: #999;
        }

        .legend-item {
          display: flex;
          align-items: center;
          gap: 5px;
        }

        .legend-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          display: inline-block;
        }

        .legend-line {
          width: 14px;
          height: 0;
          border-top: 2px solid;
          display: inline-block;
        }

        .legend-line.dashed {
          border-top-style: dashed;
        }

        /* ── HVAC history chart ── */
        .chart-wrap {
          margin: 4px 0 4px;
        }

        .chart-svg {
          width: 100%;
          height: 160px;
          background: #0a0a1a;
          border: 1px solid #0f3460;
          border-radius: 8px;
          display: block;
        }
      </style>
    </head>
    <body>
      <div class="page-wrap">

        <div class="tab-bar">
          <button class="tab-btn active" id="tab-btn-system" onclick="showTab('system')">System Parameters</button>
          <button class="tab-btn" id="tab-btn-network" onclick="showTab('network')">Network Details</button>
        </div>

        <!-- ══════════════════ TAB: System Parameters ══════════════════ -->
        <div class="tab-panel active" id="tab-system">

          <!-- Operation Mode banner — the one shared control that decides
               which model below is live. Only one model runs at a time. -->
          <div class="card mode-banner" style="margin-bottom:16px;">
            <div class="mode-banner-text">
              <strong>Operation Mode</strong> — <span id="stat-mode">—</span>.
              The AP runs <strong>one model at a time</strong>; switching modes
              hands control to the other model and its targeting parameters below.
            </div>
            <button class="btn-mode" id="mode-toggle-btn" onclick="toggleMode()">Switch</button>
          </div>

          <div class="layout">

            <!-- Left column: Submarine Model -->
            <div class="column">
              <div class="card model-card" id="model-submarine">
                <div class="header">
                  <div class="header-icon">&#128993;</div>
                  <h1>Submarine Model
                    <span class="model-badge" id="badge-submarine">—</span>
                    <span style="display:block; font-size:0.72rem; color:#888; font-weight:normal; margin-top:2px;">
                      Encryption, Kalman filtering, X/Y targeting
                    </span>
                  </h1>
                </div>

                <div class="status-row">
                  <span class="status-key">Encryption</span>
                  <span class="status-val" id="stat-enc">—</span>
                </div>
                <div class="status-row">
                  <span class="status-key">Key</span>
                  <span class="status-val" id="stat-enc-key">—</span>
                </div>
                <div class="status-row">
                  <span class="status-key">Kalman Filter</span>
                  <span class="status-val" id="stat-filter">—</span>
                </div>
                <div class="status-row" style="margin-bottom:14px;">
                  <span class="status-key">Current Target X / Y</span>
                  <span class="status-val" id="stat-target">—</span>
                </div>
                                <div class="status-row">
                  <span class="status-key">Speed</span>
                  <span class="status-val" id="stat-speed">—</span>
                </div>
                <div class="status-row" style="margin-bottom:14px;">
                  <span class="status-key">Rudder</span>
                  <span class="status-val" id="stat-rudder">—</span>
                </div>


                <div class="minimap-wrap">
                  <svg class="minimap-svg" id="target-minimap" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
                    <!-- grid -->
                    <g stroke="#16213e" stroke-width="1">
                      <line x1="10" y1="55"  x2="210" y2="55" />
                      <line x1="10" y1="110" x2="210" y2="110" />
                      <line x1="10" y1="165" x2="210" y2="165" />
                      <line x1="65"  y1="10" x2="65"  y2="210" />
                      <line x1="110" y1="10" x2="110" y2="210" />
                      <line x1="165" y1="10" x2="165" y2="210" />
                    </g>
                    <!-- border -->
                    <rect x="10" y="10" width="200" height="200" fill="none" stroke="#0f3460" stroke-width="1.5" />
                    <!-- crosshair -->
                    <line id="target-cross-h" x1="10" y1="110" x2="210" y2="110" stroke="#e94560" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" />
                    <line id="target-cross-v" x1="110" y1="10" x2="110" y2="210" stroke="#e94560" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" />
                    <!-- live telemetry positions -->
                    <circle id="live-server-dot" cx="110" cy="110" r="4.5" fill="#ffb84f" stroke="#0a0a1a" stroke-width="1" opacity="0" />
                    <circle id="live-client-dot" cx="110" cy="110" r="4.5" fill="#4fd1ff" stroke="#0a0a1a" stroke-width="1" opacity="0" />
                    <!-- target -->
                    <circle id="target-dot" cx="110" cy="110" r="5" fill="#e94560" stroke="#fff" stroke-width="1.5" />
                  </svg>
                  <div class="legend-row">
                    <span class="legend-item"><span class="legend-dot" style="background:#e94560;"></span>Target</span>
                    <span class="legend-item"><span class="legend-dot" style="background:#4fd1ff;"></span>Client Live</span>
                    <span class="legend-item"><span class="legend-dot" style="background:#ffb84f;"></span>Server Live</span>
                  </div>
                  <div class="minimap-caption">Display range: 0–200 on each axis</div>
                </div>

                <div class="section-title">Set Target Position</div>
                <div class="form-group">
                  <label for="sub_target_x">Target X</label>
                  <input type="number" step="0.1" id="sub_target_x" placeholder="e.g. 100.0">
                </div>
                <div class="form-group">
                  <label for="sub_target_y">Target Y</label>
                  <input type="number" step="0.1" id="sub_target_y" placeholder="e.g. 100.0">
                </div>
                <button class="btn btn-primary" onclick="setSubmarineTarget()">
                  Set Target
                </button>

                <div class="model-note">
                  Active only while Operation Mode is set to SUBMARINE.
                </div>
              </div>
            </div>

            <!-- Right column: HVAC Model -->
            <div class="column">
              <!-- ── HVAC Targeting (TEMPORARY test tool) ──
                   This card exists only to verify HVAC_Client/HVAC_Server
                   are wired up correctly. Remove once defender.py owns
                   setpoint control in production. -->
              <div class="card model-card" id="model-hvac">
                <div class="header">
                  <div class="header-icon">&#127777;</div>
                  <h1>HVAC Model
                    <span class="model-badge" id="badge-hvac">—</span>
                    <span style="display:block; font-size:0.72rem; color:#888; font-weight:normal; margin-top:2px;">
                      Current and Target Temperature
                    </span>
                  </h1>
                </div>

                <div class="status-row">
                  <span class="status-key">Current Room Temp</span>
                  <span class="status-val" id="stat-room-temp">—</span>
                </div>
                <div class="status-row">
                  <span class="status-key">Heater</span>
                  <span class="status-val" id="stat-heater">—</span>
                </div>
                <div class="status-row" style="margin-bottom:14px;">
                  <span class="status-key">Current Setpoint</span>
                  <span class="status-val" id="stat-hvac-target">—</span>
                </div>

                <div class="chart-wrap">
                  <svg class="chart-svg" id="hvac-chart" viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg">
                    <text x="200" y="85" text-anchor="middle" font-size="12" fill="#555">Collecting data&#8230;</text>
                  </svg>
                  <div class="legend-row">
                    <span class="legend-item"><span class="legend-line" style="border-color:#e94560;"></span>Live Temp</span>
                    <span class="legend-item"><span class="legend-line dashed" style="border-color:#4fd1ff;"></span>Target Setpoint</span>
                  </div>
                </div>

                <div class="section-title">Set Target Temperature</div>
                <div class="form-group">
                  <label for="hvac_target">Target Temperature (&deg;F)</label>
                  <input type="number" step="0.1" id="hvac_target" placeholder="e.g. 75.2">
                </div>

                <button class="btn btn-primary" onclick="setHvacTarget()">
                  Set Temperature
                </button>

                <div class="model-note">
                  Active only while Operation Mode is set to HVAC.
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- ══════════════════ TAB: Network Details ══════════════════ -->
        <div class="tab-panel" id="tab-network">
          <div class="layout">

            <!-- Left column: connection config -->
            <div class="column">
              <div class="card">
                <div class="header">
                  <div class="header-icon">&#128268;</div>
                  <h1> Network Config
                    <span>Access Point / Relay Node</span>
                  </h1>
                </div>

                <div class="section-title">Router Credentials</div>

                <div class="form-group">
                  <label for="ssid">Network SSID</label>
                  <input type="text" id="ssid" placeholder="e.g. MyLabRouter" value=")rawhtml" + g_ssid + R"rawhtml(">
                </div>

                <div class="form-group">
                  <label for="password">Password</label>
                  <input type="password" id="password" placeholder="Router password">
                </div>

                <div class="section-title">Flask Server</div>

                <div class="form-group">
                  <label for="flask_ip">Flask Server IP</label>
                  <input type="text" id="flask_ip" placeholder="e.g. 192.168.8.167" value=")rawhtml" + g_flask_ip + R"rawhtml(">
                </div>

                <button class="btn btn-primary" onclick="saveConfig()">
                  &#128190; Save &amp; Reconnect
                </button>

                <button class="btn btn-secondary" onclick="clearData()">
                  &#128465; Clear Telemetry Data
                </button>

                <button class="btn btn-secondary" onclick="rebootDevice()">
                  &#128260; Reboot System
                </button>

                <div class="toast" id="toast"></div>

                <div class="footer" style="margin-top:20px;">
                  AP IP: 192.168.4.1 &nbsp;|&nbsp; SSID: AP-Config
                </div>
              </div>
            </div>

            <!-- Right column: connection stats + devices -->
            <div class="column">

              <!-- Connection Stats Card -->
              <div class="card">
                <div class="section-title" style="margin-top:0;">Connection Status
                  <span style="float:right; color:#555; font-size:0.65rem; letter-spacing:0;">
                    auto-refresh 5s
                  </span>
                </div>

                <div class="stat-grid">
                  <div class="stat-box">
                    <div class="stat-value" id="stat-clients">—</div>
                    <div class="stat-label">Connected</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-value" id="stat-uptime">—</div>
                    <div class="stat-label">Uptime</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-value" id="stat-client-pts">—</div>
                    <div class="stat-label">Client Points</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-value" id="stat-server-pts">—</div>
                    <div class="stat-label">Server Points</div>
                  </div>
                </div>

                <div style="margin-top: 14px;">
                  <div class="status-row">
                    <span class="status-key">AP IP</span>
                    <span class="status-val">192.168.4.1</span>
                  </div>
                </div>
              </div>

              <!-- Connected Devices Card -->
              <div class="card">
                <div class="section-title" style="margin-top:0;">Connected Devices</div>
                <table class="device-table">
                  <thead>
                    <tr>
                      <th>IP Address</th>
                      <th>Status</th>
                      <th>Last Seen</th>
                      <th>Points</th>
                    </tr>
                  </thead>
                  <tbody id="device-tbody">
                    <tr><td colspan="4" class="no-devices">No devices seen yet</td></tr>
                  </tbody>
                </table>
              </div>

            </div>
          </div>
        </div>

      </div>

      <script>
        // ── Tab switching ──────────────────────────────────────────
        function showTab(name) {
          document.getElementById('tab-system').classList.toggle('active', name === 'system');
          document.getElementById('tab-network').classList.toggle('active', name === 'network');
          document.getElementById('tab-btn-system').classList.toggle('active', name === 'system');
          document.getElementById('tab-btn-network').classList.toggle('active', name === 'network');
        }

        // ── Toast helper ──────────────────────────────────────────
        function showToast(msg) {
          const t = document.getElementById('toast');
          t.textContent = msg;
          t.style.display = 'block';
          setTimeout(() => t.style.display = 'none', 4000);
        }

        // ── Format uptime ms → HH:MM:SS ──────────────────────────
        function formatUptime(ms) {
          const s   = Math.floor(ms / 1000);
          const h   = Math.floor(s / 3600);
          const m   = Math.floor((s % 3600) / 60);
          const sec = s % 60;
          return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
        }

        // ── Dot colour based on last-seen seconds ─────────────────
        function dotClass(lastSeenS) {
          if (lastSeenS < 5)  return 'dot-green';
          if (lastSeenS < 15) return 'dot-yellow';
          return 'dot-red';
        }

        // ── Reflect which model is live on the two model cards ────
        //    Only one model (Submarine or HVAC) runs at a time, driven
        //    by Operation Mode — this just makes that visually obvious.
        function updateModelCards(isSubmarine) {
          const subCard   = document.getElementById('model-submarine');
          const hvacCard  = document.getElementById('model-hvac');
          const subBadge  = document.getElementById('badge-submarine');
          const hvacBadge = document.getElementById('badge-hvac');

          subCard.classList.toggle('model-active', isSubmarine);
          subCard.classList.toggle('model-inactive', !isSubmarine);
          hvacCard.classList.toggle('model-active', !isSubmarine);
          hvacCard.classList.toggle('model-inactive', isSubmarine);

          subBadge.textContent = isSubmarine ? 'ACTIVE' : 'INACTIVE';
          subBadge.className   = 'model-badge ' + (isSubmarine ? 'badge-active' : 'badge-inactive');
          hvacBadge.textContent = isSubmarine ? 'INACTIVE' : 'ACTIVE';
          hvacBadge.className   = 'model-badge ' + (isSubmarine ? 'badge-inactive' : 'badge-active');
        }

        // ── Mask the encryption key for display — show only the first
        //    character, dot out the rest. Never render the full key.
        function maskKey(key) {
          if (!key) return '—';
          const k = String(key);
          if (k.length <= 1) return '•'.repeat(k.length || 1);
          return k.slice(0, 1) + '•'.repeat(k.length - 1);
        }

        function formatRudder(deg) {
          if (deg === undefined || deg === null || isNaN(deg)) return '—';
          if (Math.abs(deg) < 0.05) return '0.0° (amidships)';
          return `${Math.abs(deg).toFixed(1)}° ${deg > 0 ? 'R' : 'L'}`;
        }



        // ── Map a raw (x, y) telemetry value onto the mini-map's SVG ──
        //    Fixed 0–200 display range on each axis, clamped so an
        //    out-of-range point still shows at the nearest edge.
        function minimapCoords(x, y) {
          if (x === undefined || x === null || isNaN(x) || y === undefined || y === null || isNaN(y)) return null;
          const svgMin = 10, svgMax = 210, rangeMin = 0, rangeMax = 200;
          const clamp = v => Math.max(rangeMin, Math.min(rangeMax, v));
          const toSvg = v => svgMin + (clamp(v) / (rangeMax - rangeMin)) * (svgMax - svgMin);
          // SVG y-axis grows downward; flip so higher Y plots toward the top
          return { x: toSvg(x), y: svgMin + svgMax - toSvg(y) };
        }

        // ── Plot target + live telemetry positions on the mini-map ──
        function updateTargetMinimap(d) {
          const target = minimapCoords(d.target_x, d.target_y) || { x: 110, y: 110 };
          document.getElementById('target-dot').setAttribute('cx', target.x);
          document.getElementById('target-dot').setAttribute('cy', target.y);
          document.getElementById('target-cross-h').setAttribute('y1', target.y);
          document.getElementById('target-cross-h').setAttribute('y2', target.y);
          document.getElementById('target-cross-v').setAttribute('x1', target.x);
          document.getElementById('target-cross-v').setAttribute('x2', target.x);

          const clientDot = document.getElementById('live-client-dot');
          const clientPos = d.has_client_live ? minimapCoords(d.client_live_x, d.client_live_y) : null;
          if (clientPos) {
            clientDot.setAttribute('cx', clientPos.x);
            clientDot.setAttribute('cy', clientPos.y);
            clientDot.setAttribute('opacity', '1');
          } else {
            clientDot.setAttribute('opacity', '0');
          }

          const serverDot = document.getElementById('live-server-dot');
          const serverPos = d.has_server_live ? minimapCoords(d.server_live_x, d.server_live_y) : null;
          if (serverPos) {
            serverDot.setAttribute('cx', serverPos.x);
            serverDot.setAttribute('cy', serverPos.y);
            serverDot.setAttribute('opacity', '1');
          } else {
            serverDot.setAttribute('opacity', '0');
          }
        }

        // ── Format an elapsed-ms span as a short "Xs"/"Xm" label ────
        function formatElapsed(ms) {
          const s = Math.round(ms / 1000);
          if (s < 60) return s + 's';
          return Math.round(s / 60) + 'm';
        }

        // ── Draw the HVAC live-temp vs setpoint line chart ──────────
        function renderHvacChart(samples) {
          const svg = document.getElementById('hvac-chart');
          if (!samples || samples.length < 2) {
            svg.innerHTML = '<text x="200" y="85" text-anchor="middle" font-size="12" fill="#555">Collecting data&#8230;</text>';
            return;
          }

          const W = 400, H = 160, padL = 38, padR = 10, padT = 10, padB = 22;
          const plotW = W - padL - padR, plotH = H - padT - padB;

          const times = samples.map(s => s.t);
          const minT = times[0], maxT = times[times.length - 1];
          const span = Math.max(maxT - minT, 1);

          const rooms   = samples.map(s => s.room);
          const targets = samples.map(s => s.target);
          const allV = rooms.concat(targets);
          let minV = Math.min(...allV), maxV = Math.max(...allV);
          if (minV === maxV) { minV -= 1; maxV += 1; }
          const pad = (maxV - minV) * 0.15 || 1;
          minV -= pad; maxV += pad;
          const vSpan = maxV - minV;

          const xAt = t => padL + ((t - minT) / span) * plotW;
          const yAt = v => padT + (1 - (v - minV) / vSpan) * plotH;

          const roomPts   = samples.map(s => `${xAt(s.t).toFixed(1)},${yAt(s.room).toFixed(1)}`).join(' ');
          const targetPts = samples.map(s => `${xAt(s.t).toFixed(1)},${yAt(s.target).toFixed(1)}`).join(' ');
          const gridYs = [0, 0.5, 1].map(f => (padT + f * plotH).toFixed(1));

          svg.innerHTML = `
            ${gridYs.map(gy => `<line x1="${padL}" y1="${gy}" x2="${W - padR}" y2="${gy}" stroke="#16213e" stroke-width="1" />`).join('')}
            <line x1="${padL}" y1="${padT}" x2="${padL}" y2="${H - padB}" stroke="#0f3460" stroke-width="1.5" />
            <line x1="${padL}" y1="${H - padB}" x2="${W - padR}" y2="${H - padB}" stroke="#0f3460" stroke-width="1.5" />
            <polyline points="${targetPts}" fill="none" stroke="#4fd1ff" stroke-width="2" stroke-dasharray="4,3" />
            <polyline points="${roomPts}" fill="none" stroke="#e94560" stroke-width="2" />
            <text x="${padL - 4}" y="${(padT + 4).toFixed(1)}" text-anchor="end" font-size="9" fill="#666">${maxV.toFixed(1)}&#176;</text>
            <text x="${padL - 4}" y="${H - padB}" text-anchor="end" font-size="9" fill="#666">${minV.toFixed(1)}&#176;</text>
            <text x="${padL}" y="${H - 4}" text-anchor="start" font-size="9" fill="#555">-${formatElapsed(span)}</text>
            <text x="${W - padR}" y="${H - 4}" text-anchor="end" font-size="9" fill="#555">now</text>
          `;
        }

        // ── Fetch HVAC temperature history and redraw the chart ─────
        async function fetchHvacHistory() {
          try {
            const resp = await fetch('/hvac_history');
            if (!resp.ok) return;
            const data = await resp.json();
            renderHvacChart(data.samples || []);
          } catch (e) {
            console.warn('History fetch failed:', e);
          }
        }

        // ── Fetch status and update both panels ───────────────────
        async function refreshStatus() {
          try {
            const resp = await fetch('/status');
            if (!resp.ok) return;
            const d = await resp.json();

            // Stat boxes
            document.getElementById('stat-clients').textContent =
              (d.connected_clients ?? '—') + ' / 3';
            document.getElementById('stat-uptime').textContent =
              d.uptime_ms !== undefined ? formatUptime(d.uptime_ms) : '—';
            document.getElementById('stat-client-pts').textContent =
              d.client_point_count ?? '—';
            document.getElementById('stat-server-pts').textContent =
              d.server_point_count ?? '—';

            // Status rows
            const encEl = document.getElementById('stat-enc');
            encEl.textContent    = d.encryption ? 'ON' : 'OFF';
            encEl.className      = 'status-val ' + (d.encryption ? 'green' : 'red');
            const keyEl = document.getElementById('stat-enc-key');
            keyEl.textContent    = d.encryption ? maskKey(d.encryption_key) : '—';
            const filterEl = document.getElementById('stat-filter');           // ← add this block
            filterEl.textContent = d.filter_correction ? 'ON' : 'OFF';
            filterEl.className   = 'status-val ' + (d.filter_correction ? 'green' : 'red');
            const modeEl = document.getElementById('stat-mode');
            const modeBtnEl = document.getElementById('mode-toggle-btn');
            modeEl.textContent  = d.submarine_mode ? 'SUBMARINE' : 'HVAC';
            modeEl.className    = 'status-val ' + (d.submarine_mode ? 'green' : 'red');
            modeBtnEl.textContent = d.submarine_mode ? '→ HVAC' : '→ SUBMARINE';

            document.getElementById('stat-target').textContent =
              `(${d.target_x ?? '—'}, ${d.target_y ?? '—'})`;
            updateTargetMinimap(d);

            document.getElementById('stat-speed').textContent =
              d.has_live_speed ? d.live_speed.toFixed(1) + ' kn' : '—';
            document.getElementById('stat-rudder').textContent =
              d.has_live_rudder ? formatRudder(d.live_rudder) : '—';


            // HVAC setpoint readout (test tool)
            document.getElementById('stat-hvac-target').textContent =
              d.target_temp !== undefined ? d.target_temp.toFixed(1) + '°F' : '—';

            // Live HVAC telemetry, relayed in from HVAC_Server's /hvac_status posts
            document.getElementById('stat-room-temp').textContent =
              d.current_temp !== undefined ? d.current_temp.toFixed(1) + '°F' : '—';
            const heaterEl = document.getElementById('stat-heater');
            heaterEl.textContent = d.heater_on ? 'ON' : 'OFF';
            heaterEl.className   = 'status-val ' + (d.heater_on ? 'green' : 'red');

            // Which model is live — only one runs at a time
            updateModelCards(!!d.submarine_mode);

            // Device table
            const tbody = document.getElementById('device-tbody');
            if (!d.devices || d.devices.length === 0) {
              tbody.innerHTML =
                '<tr><td colspan="4" class="no-devices">No devices seen yet</td></tr>';
            } else {
              tbody.innerHTML = d.devices.map(dev => {
                const cls = dotClass(dev.last_seen_s);
                const age = dev.last_seen_s < 60
                  ? dev.last_seen_s + 's ago'
                  : Math.floor(dev.last_seen_s / 60) + 'm ago';
                const status = dev.last_seen_s < 5 ? 'Active'
                            : dev.last_seen_s < 15 ? 'Slow'
                            : 'Stale';
                return `<tr>
                  <td>${dev.ip}</td>
                  <td><span class="dot ${cls}"></span>${status}</td>
                  <td>${age}</td>
                  <td>${dev.point_count}</td>
                </tr>`;
              }).join('');
            }
          } catch(e) {
            console.warn('Status fetch failed:', e);
          }
        }

        // ── Save config ───────────────────────────────────────────
        async function saveConfig() {
          const ssid     = document.getElementById('ssid').value.trim();
          const password = document.getElementById('password').value;
          const flask_ip = document.getElementById('flask_ip').value.trim();

          if (!ssid) { showToast('SSID cannot be empty.'); return; }

          const resp = await fetch('/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ssid, password, flask_ip })
          });

          if (resp.ok) {
            showToast('Saved! Reconnecting...');
            setTimeout(() => location.reload(), 4000);
          } else {
            showToast('Error saving config.');
          }
        }

        // ── Clear telemetry ───────────────────────────────────────
        async function clearData() {
          await fetch('/clear', { method: 'POST' });
          showToast('Telemetry data cleared.');
          refreshStatus();
        }

        async function toggleMode() {
          const modeEl = document.getElementById('stat-mode');
          const currentlySubmarine = modeEl.textContent.trim() === 'SUBMARINE';
          const newMode = !currentlySubmarine;

          const resp = await fetch('/set_mode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ submarine_mode: newMode })
          });

          if (resp.ok) {
            showToast('Mode set to: ' + (newMode ? 'SUBMARINE' : 'HVAC'));
            refreshStatus();
          } else {
            showToast('Failed to set mode.');
          }
        }

        // ── Submarine targeting ──────────────────────────────────────
        async function setSubmarineTarget() {
          const rawX = document.getElementById('sub_target_x').value;
          const rawY = document.getElementById('sub_target_y').value;
          const x = parseFloat(rawX);
          const y = parseFloat(rawY);
          if (rawX === '' || rawY === '' || isNaN(x) || isNaN(y)) {
            showToast('Enter valid X and Y values.');
            return;
          }

          const resp = await fetch('/set_target', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target_x: x, target_y: y })
          });

          if (resp.ok) {
            showToast(`Target sent: (${x}, ${y})`);
            refreshStatus();
          } else {
            showToast('Failed to set target.');
          }
        }

        // ── HVAC setpoint (test tool) ──────────────────────────────
        async function setHvacTarget() {
          const raw = document.getElementById('hvac_target').value;
          const val = parseFloat(raw);
          if (raw === '' || isNaN(val)) {
            showToast('Enter a valid temperature.');
            return;
          }

          const resp = await fetch('/set_hvac_target', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target_temp: val })
          });

          if (resp.ok) {
            showToast('Setpoint sent: ' + val.toFixed(1) + '°F');
            refreshStatus();
          } else {
            showToast('Failed to set HVAC target.');
          }
        }

        // ── Reboot ────────────────────────────────────────────────
        async function rebootDevice() {
          await fetch('/reboot', { method: 'POST' });
          showToast('Rebooting System...');
        }

        // ── Start auto-refresh ────────────────────────────────────
        refreshStatus();
        fetchHvacHistory();
        setInterval(() => {
          refreshStatus();
          fetchHvacHistory();
        }, 5000);
      </script>
    </body>
    </html>
    )rawhtml";
      return html;
  }

void setupRoutes() {

  // ── GET /  →  Config page ──────────────────────────────────
  server.on("/", HTTP_GET, [](AsyncWebServerRequest* req) {
    req->send(200, "text/html", buildConfigPage());
  });

  // ── GET /config  →  Return current config as JSON ──────────
  //   Called by Master/Server devices at boot to fetch credentials,
  //   and polled by HVAC_Server.ino each cycle to pick up the live
  //   setpoint (target_temp) and the AP's current operation mode.
  server.on("/config", HTTP_GET, [](AsyncWebServerRequest* req) {
    StaticJsonDocument<256> doc;
    doc["ssid"]         = AP_SSID;       // ← always AP-Config
    doc["password"]     = AP_PASSWORD;   // ← always admin1234
    doc["flask_ip"]     = "192.168.4.1"; // ← AP IP, no Flask needed
    doc["ap_router_ip"] = "192.168.4.1"; // ← same, always static
    doc["target_temp"]    = g_target_temp;    // ← live HVAC setpoint
    doc["submarine_mode"] = g_submarine_mode; // ← so HVAC devices know if they should run
    String out;
    serializeJson(doc, out);
    req->send(200, "application/json", out);
  });

  // ── POST /config  →  Save credentials ──────────────────────
  server.on("/config", HTTP_POST,
    [](AsyncWebServerRequest* req) {},
    nullptr,
    [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
      StaticJsonDocument<256> doc;
      DeserializationError err = deserializeJson(doc, data, len);
      if (err) {
        req->send(400, "application/json", "{\"error\":\"bad json\"}");
        return;
      }

      String newSsid  = doc["ssid"]     | "";
      String newPass  = doc["password"] | "";
      String newFlask = doc["flask_ip"] | "";

      if (newSsid.length() == 0 || newFlask.length() == 0) {
        req->send(400, "application/json", "{\"error\":\"missing fields\"}");
        return;
      }

      g_ssid     = newSsid;
      g_password = newPass;
      g_flask_ip = newFlask;
      savePreferences(g_ssid, g_password, g_flask_ip);

      req->send(200, "application/json", "{\"status\":\"saved\"}");
      delay(500);
      //connectSTA();
    }
  );

  // ── POST /reboot  →  Reboot device ──────────────────────────
  server.on("/reboot", HTTP_POST, [](AsyncWebServerRequest* req) {
    req->send(200, "application/json", "{\"status\":\"rebooting\"}");
    delay(500);
    ESP.restart();
  });

  // ── GET /status  →  JSON health check ──────────────────────
  server.on("/status", HTTP_GET, [](AsyncWebServerRequest* req) {
  StaticJsonDocument<2048> doc;
  doc["ap_ssid"]           = AP_SSID;
  doc["ap_ip"]             = WiFi.softAPIP().toString();
  doc["sta_ssid"]          = g_ssid;
  doc["sta_connected"]     = (WiFi.status() == WL_CONNECTED);
  doc["sta_ip"]            = WiFi.localIP().toString();
  doc["flask_ip"]          = g_flask_ip;
  doc["target_x"]          = g_target_x;
  doc["target_y"]          = g_target_y;
  doc["encryption"]        = g_encryption_status;
  doc["encryption_key"]    = g_encryption_key;
  doc["uptime_ms"]         = millis();
  doc["client_point_count"] = g_client_arr.size();
  doc["server_point_count"] = g_server_arr.size();
  doc["connected_clients"] = WiFi.softAPgetStationNum();
  doc["filter_correction"] = g_filter_correction;
  doc["submarine_mode"] = g_submarine_mode;
  doc["target_temp"]    = g_target_temp;
  doc["current_temp"]   = g_current_room_temp;
  doc["heater_on"]      = g_heater_on;

  // Live submarine telemetry position, per source, for the mini-map
  doc["has_client_live"] = g_has_client_live;
  doc["client_live_x"]   = g_client_live_x;
  doc["client_live_y"]   = g_client_live_y;
  doc["has_server_live"] = g_has_server_live;
  doc["server_live_x"]   = g_server_live_x;
  doc["server_live_y"]   = g_server_live_y;
  doc["has_live_speed"]  = g_has_live_speed;
  doc["live_speed"]      = g_live_speed;
  doc["has_live_rudder"] = g_has_live_rudder;
  doc["live_rudder"]     = g_live_rudder;



  // device list
  JsonArray devices = doc.createNestedArray("devices");
  uint32_t now = millis();
  for (auto& kv : g_devices) {
    JsonObject d = devices.createNestedObject();
    d["ip"]          = kv.second.ip;
    d["last_seen_s"] = (now - kv.second.lastSeenMs) / 1000;
    d["point_count"] = kv.second.pointCount;
  }

  String out;
  serializeJson(doc, out);
  req->send(200, "application/json", out);
});

  // ── GET /hvac_history  →  Recent room-temp vs setpoint samples ─
  //   Used by the System Parameters tab to draw the HVAC line chart.
  //   Returns samples oldest-first; "ms" is device uptime in ms,
  //   not wall-clock time, since the AP has no RTC.
  server.on("/hvac_history", HTTP_GET, [](AsyncWebServerRequest* req) {
    DynamicJsonDocument doc(2048);
    JsonArray samples = doc.createNestedArray("samples");
    int start = (g_hvac_history_head - g_hvac_history_count + HVAC_HISTORY_LEN) % HVAC_HISTORY_LEN;
    for (int i = 0; i < g_hvac_history_count; i++) {
      int idx = (start + i) % HVAC_HISTORY_LEN;
      JsonObject s = samples.createNestedObject();
      s["t"]      = g_hvac_history[idx].ms;
      s["room"]   = g_hvac_history[idx].room;
      s["target"] = g_hvac_history[idx].target;
    }
    String out;
    serializeJson(doc, out);
    req->send(200, "application/json", out);
  });

  // ── POST /data  →  Accumulate points, return control state ─
  //   Body: { "source": "client"|"server", "x":..., "y":..., ... }
  server.on("/data", HTTP_POST,
    [](AsyncWebServerRequest* req) {},
    nullptr,
    [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
      DynamicJsonDocument incoming(512);
      DeserializationError err = deserializeJson(incoming, data, len);
      if (err) {
        req->send(400, "application/json", "{\"error\":\"bad json\"}");
        return;
      }

      incoming["received_at"] = String(millis() / 1000);

      String src = incoming["source"] | "unknown";

      // ── Track device last-seen ─────────────────────────────────
      String clientIP = req->client()->remoteIP().toString();
      g_devices[clientIP].ip         = clientIP;
      g_devices[clientIP].lastSeenMs = millis();
      if (src == "client") {
        if (g_client_arr.size() >= MAX_POINTS) g_client_arr.remove(0);
        g_client_arr.add(incoming.as<JsonObject>());
        g_devices[clientIP].pointCount = g_client_arr.size();
      } else if (src == "server") {
        if (g_server_arr.size() >= MAX_POINTS) g_server_arr.remove(0);
        g_server_arr.add(incoming.as<JsonObject>());
        g_devices[clientIP].pointCount = g_server_arr.size();
      }

      // ── Track live (x, y) position per source for the mini-map ──
      if (incoming.containsKey("x") && incoming.containsKey("y")) {
        float px = incoming["x"];
        float py = incoming["y"];
        if (src == "client") {
          g_client_live_x = px;
          g_client_live_y = py;
          g_has_client_live = true;
        } else if (src == "server") {
          g_server_live_x = px;
          g_server_live_y = py;
          g_has_server_live = true;
        }
      }

      // ── Track live speed / rudder from whichever source posts them ──
      if (incoming.containsKey("speed")) {
        g_live_speed     = incoming["speed"];
        g_has_live_speed = true;
      }
      if (incoming.containsKey("rudder")) {
        g_live_rudder     = incoming["rudder"];
        g_has_live_rudder = true;
      }



      // Return control state
      StaticJsonDocument<128> resp;
      resp["encryption_status"] = g_encryption_status;
      resp["encryption_key"]    = g_encryption_key;
      resp["target_x"]          = g_target_x;
      resp["target_y"]          = g_target_y;
      resp["filter_correction"]  = g_filter_correction;
      resp["submarine_mode"] = g_submarine_mode;

      String out;
      serializeJson(resp, out);
      req->send(200, "application/json", out);
    }
  );

  // ── GET /api/data  →  Serve accumulated points to Defender ─
  server.on("/api/data", HTTP_GET, [](AsyncWebServerRequest* req) {
    DynamicJsonDocument resp(8192);
    resp["encryption_status"] = g_encryption_status;
    resp["encryption_key"]    = g_encryption_key;
    resp["target_x"]          = g_target_x;
    resp["target_y"]          = g_target_y;
    resp["client_points"]     = g_client_arr;
    resp["server_points"]     = g_server_arr;
    resp["submarine_mode"] = g_submarine_mode;
    resp["target_temp"]    = g_target_temp;
    resp["current_temp"]   = g_current_room_temp;
    resp["heater_on"]      = g_heater_on;

    String out;
    serializeJson(resp, out);
    req->send(200, "application/json", out);
  });

  // ── POST /set_encryption  →  Defender toggles encryption ───
  server.on("/set_encryption", HTTP_POST,
    [](AsyncWebServerRequest* req) {},
    nullptr,
    [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
      StaticJsonDocument<128> doc;
      DeserializationError err = deserializeJson(doc, data, len);
      if (err) {
        req->send(400, "application/json", "{\"error\":\"bad json\"}");
        return;
      }
      g_encryption_status = doc["encryption_status"] | false;
      g_encryption_key    = doc["encryption_key"]    | "1234";
      Serial.printf("[AP] Encryption set: %s  key=%s\n",
                    g_encryption_status ? "ON" : "OFF",
                    g_encryption_key.c_str());
      req->send(200, "application/json", "{\"status\":\"ok\"}");
    }
  );

  // ── POST /set_filter_correction  →  Defender toggles filter correction ─
  server.on("/set_filter_correction", HTTP_POST,
    [](AsyncWebServerRequest* req) {},
    nullptr,
    [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
      StaticJsonDocument<64> doc;
      DeserializationError err = deserializeJson(doc, data, len);
      if (err) {
        req->send(400, "application/json", "{\"error\":\"bad json\"}");
        return;
      }
      g_filter_correction = doc["filter_correction"] | false;
      Serial.printf("[AP] filterCorrection set: %s\n",
                    g_filter_correction ? "ON" : "OFF");
      req->send(200, "application/json", "{\"status\":\"ok\"}");
    }
  );

  // ── POST /set_target  →  Defender sets target position ─────
  server.on("/set_target", HTTP_POST,
    [](AsyncWebServerRequest* req) {},
    nullptr,
    [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
      StaticJsonDocument<128> doc;
      DeserializationError err = deserializeJson(doc, data, len);
      if (err) {
        req->send(400, "application/json", "{\"error\":\"bad json\"}");
        return;
      }
      g_target_x = doc["target_x"] | 100.0f;
      g_target_y = doc["target_y"] | 100.0f;
      Serial.printf("[AP] Target set: (%.1f, %.1f)\n",
                    g_target_x, g_target_y);
      req->send(200, "application/json", "{\"status\":\"ok\"}");
    }
  );

  server.on("/set_mode", HTTP_POST,
      [](AsyncWebServerRequest* req) {},
      nullptr,
      [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
        StaticJsonDocument<64> doc;
        DeserializationError err = deserializeJson(doc, data, len);
        if (err || !doc.containsKey("submarine_mode")) {
          req->send(400, "application/json", "{\"error\":\"bad json\"}");
          return;
        }
        g_submarine_mode = doc["submarine_mode"].as<bool>();
        Serial.printf("[AP] Mode set: %s\n",
                      g_submarine_mode ? "SUBMARINE" : "HVAC");
        req->send(200, "application/json", "{\"status\":\"ok\"}");
    }
  );

  // ── POST /set_hvac_target  →  Manually push a setpoint ──────
  //   TEMPORARY TEST TOOL: lets you punch in a target_temp from the
  //   AP's config page to verify HVAC_Client/HVAC_Server respond
  //   correctly. Production setpoint control will live in defender.py —
  //   remove this card + endpoint once that's wired up.
  server.on("/set_hvac_target", HTTP_POST,
    [](AsyncWebServerRequest* req) {},
    nullptr,
    [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
      StaticJsonDocument<128> doc;
      DeserializationError err = deserializeJson(doc, data, len);
      if (!err && doc.containsKey("target_temp")) {
        g_target_temp = doc["target_temp"];
        Serial.printf("[AP] New HVAC target received: %.2f°F\n", g_target_temp);
        recordHvacSample(g_current_room_temp, g_target_temp);
        req->send(200, "application/json", "{\"status\":\"ok\"}");
      } else {
        req->send(400, "application/json", "{\"error\":\"invalid json data\"}");
      }
    }
  );

  // ── POST /hvac_status  →  HVAC_Server.ino reports its live readings ─
  //   Body: { "current_temp": <float>, "heater_on": <bool> }
  //   The AP has no sensor of its own here — it's just relaying whatever
  //   the Server last measured/decided, so Defender can poll it via /api/data.
  server.on("/hvac_status", HTTP_POST,
    [](AsyncWebServerRequest* req) {},
    nullptr,
    [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
      StaticJsonDocument<128> doc;
      DeserializationError err = deserializeJson(doc, data, len);
      if (err) {
        req->send(400, "application/json", "{\"error\":\"bad json\"}");
        return;
      }
      if (doc.containsKey("current_temp")) {
        g_current_room_temp = doc["current_temp"];
      }
      if (doc.containsKey("heater_on")) {
        g_heater_on = doc["heater_on"].as<bool>();
      }
      recordHvacSample(g_current_room_temp, g_target_temp);
      req->send(200, "application/json", "{\"status\":\"ok\"}");
    }
  );

  server.on("/clear", HTTP_POST, [](AsyncWebServerRequest* req) {
      g_client_doc.clear();
      g_server_doc.clear();
      g_client_arr = g_client_doc.to<JsonArray>();
      g_server_arr = g_server_doc.to<JsonArray>();
      g_devices.clear();
      Serial.println("[AP] Telemetry data cleared.");
      req->send(200, "application/json", "{\"status\":\"cleared\"}");
  });

  // ── 404 catch-all ───────────────────────────────────────────
  server.onNotFound([](AsyncWebServerRequest* req) {
    req->send(404, "text/plain", "Not found");
  });
}