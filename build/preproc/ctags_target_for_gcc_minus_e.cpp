# 1 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino"
# 2 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2
# 3 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2
# 4 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2
# 5 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2
# 6 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2
# 7 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2
# 8 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2
# 9 "/home/martin/Desktop/cybersecurity-game/Version 17/AP_ESP32/AP_ESP32.ino" 2

// ─── Soft-AP credentials (permanent, never change) ───────────
const char* AP_SSID = "ESP32-Config";
const char* AP_PASSWORD = "admin1234";
const IPAddress AP_IP (192, 168, 4, 1);
const IPAddress AP_GW (192, 168, 4, 1);
const IPAddress AP_SUBNET(255, 255, 255, 0);

DNSServer dnsServer;
const byte DNS_PORT = 53;

// ─── NVS key names ────────────────────────────────────────────





// ─── Globals ──────────────────────────────────────────────────
Preferences prefs;
AsyncWebServer server(80);

String g_ssid = "";
String g_password = "";
String g_flask_ip = "192.168.8.167";


String g_client_payload = "{}";
String g_server_payload = "{}";



struct DeviceInfo {
  String ip;
  uint32_t lastSeenMs;
  int pointCount;
};
std::map<String, DeviceInfo> g_devices;

StaticJsonDocument<8192> g_client_doc; // stores array of points
StaticJsonDocument<8192> g_server_doc;
JsonArray g_client_arr = g_client_doc.to<JsonArray>();
JsonArray g_server_arr = g_server_doc.to<JsonArray>();

bool g_encryption_status = false;
String g_encryption_key = "1234";
float g_target_x = 100.0;
float g_target_y = 100.0;

// ─── Forward declarations ─────────────────────────────────────
void loadPreferences();
void savePreferences(const String& ssid, const String& pass, const String& flask_ip);
void startAP();
//void connectSTA();
void setupRoutes();
String buildConfigPage();
void forwardToFlask(const String& endpoint, const String& body);

void setup() {
  Serial0.begin(115200);
  delay(500);
  Serial0.println("\n[AP-ESP32] Booting...");

  loadPreferences();
  startAP();

  g_client_arr = g_client_doc.to<JsonArray>();
  g_server_arr = g_server_doc.to<JsonArray>();

  setupRoutes();
  server.begin();
  Serial0.println("[AP-ESP32] Web server started on http://192.168.4.1");
}

void loop() {
  // // Re-attempt STA connection if it drops
  // static uint32_t lastCheckMs = 0;
  // if (g_ssid.length() > 0 && millis() - lastCheckMs > 10000) {
  //   lastCheckMs = millis();
  //   if (WiFi.status() != WL_CONNECTED) {
  //     Serial.println("[AP-ESP32] STA disconnected — reconnecting...");
  //     connectSTA();
  //   }
  // }
  dnsServer.processNextRequest();
  delay(10);
}

void loadPreferences() {
  prefs.begin("netcfg", true); // read-only
  g_ssid = prefs.getString("ssid", "");
  g_password = prefs.getString("password", "");
  g_flask_ip = prefs.getString("flask_ip", "192.168.8.167");
  prefs.end();

  Serial0.printf("[AP-ESP32] Loaded NVS — SSID: '%s'  Flask: '%s'\n",g_ssid.c_str(), g_flask_ip.c_str());
}

void savePreferences(const String& ssid, const String& pass, const String& flask_ip) {
  prefs.begin("netcfg", false); // read-write
  prefs.putString("ssid", ssid);
  prefs.putString("password", pass);
  prefs.putString("flask_ip", flask_ip);
  prefs.end();
  Serial0.println("[AP-ESP32] Preferences saved to NVS.");
}

void startAP() {
  WiFi.mode(WIFI_MODE_AP); // ← was WIFI_AP_STA
  WiFi.softAPConfig(AP_IP, AP_GW, AP_SUBNET);
  WiFi.softAP(AP_SSID, AP_PASSWORD);
  Serial0.printf("[AP-ESP32] Soft-AP started: SSID='%s'  IP=%s\n", AP_SSID, WiFi.softAPIP().toString().c_str());

  //captive portal
  dnsServer.start(DNS_PORT, "*", AP_IP);
  Serial0.println("[AP-ESP32] Captive portal DNS started.");
}

// void connectSTA() {
//   Serial.printf("[AP-ESP32] Connecting to router SSID='%s'...\n", g_ssid.c_str());
//   WiFi.begin(g_ssid.c_str(), g_password.c_str());

//   uint32_t start = millis();
//   while (WiFi.status() != WL_CONNECTED && millis() - start < 10000) {
//     delay(500);
//     Serial.print(".");
//   }
//   Serial.println();

//   if (WiFi.status() == WL_CONNECTED) {
//     Serial.printf("[AP-ESP32] Router connected — IP: %s\n",
//                   WiFi.localIP().toString().c_str());

//     prefs.begin(NVS_NAMESPACE, false);
//     prefs.putString("ap_router_ip", WiFi.localIP().toString());
//     prefs.end();
//   } else {
//     Serial.println("[AP-ESP32] Router connection FAILED (will retry in 10s).");
//   }
// }

// void forwardToFlask(const String& endpoint, const String& body) {
//   if (WiFi.status() != WL_CONNECTED) {
//     Serial.println("[AP-ESP32] Cannot forward — not connected to router.");
//     return;
//   }

//   String url = "http://" + g_flask_ip + ":5000" + endpoint;
//   HTTPClient http;
//   http.begin(url);
//   http.addHeader("Content-Type", "application/json");
//   int code = http.POST(body);
//   Serial.printf("[AP-ESP32] Forwarded to Flask %s  →  HTTP %d\n",
//                 url.c_str(), code);
//   http.end();
// }


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
      <title>ESP32 Network Configuration</title>
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
      </style>
    </head>
    <body>
      <div class="layout">

        <!-- ── Left column: Config ── -->
        <div class="column">
          <div class="card">
            <div class="header">
              <div class="header-icon">&#128268;</div>
              <h1>ESP32 Network Config
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
              &#128260; Reboot ESP32
            </button>

            <div class="toast" id="toast"></div>

            <div class="footer" style="margin-top:20px;">
              AP IP: 192.168.4.1 &nbsp;|&nbsp; SSID: ESP32-Config
            </div>
          </div>
        </div>

        <!-- ── Right column: Status + Devices ── -->
        <div class="column">

          <!-- System Status Card -->
          <div class="card">
            <div class="section-title" style="margin-top:0;">System Status
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
                <span class="status-key">Encryption</span>
                <span class="status-val" id="stat-enc">—</span>
              </div>
              <div class="status-row">
                <span class="status-key">Target X / Y</span>
                <span class="status-val" id="stat-target">—</span>
              </div>
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

      <script>
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
            document.getElementById('stat-target').textContent =
              `(${d.target_x ?? '—'}, ${d.target_y ?? '—'})`;

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

        // ── Reboot ────────────────────────────────────────────────
        async function rebootDevice() {
          await fetch('/reboot', { method: 'POST' });
          showToast('Rebooting ESP32...');
        }

        // ── Start auto-refresh ────────────────────────────────────
        refreshStatus();
        setInterval(refreshStatus, 5000);
      </script>
    </body>
    </html>
    )rawhtml";
      return html;
  }

// void setupRoutes() {

//   // ── GET /  →  Config page ──────────────────────────────────
//   server.on("/", HTTP_GET, [](AsyncWebServerRequest* req) {
//     req->send(200, "text/html", buildConfigPage());
//   });

//   // ── POST /config  →  Save credentials ─────────────────────
//   server.on("/config", HTTP_POST,
//     [](AsyncWebServerRequest* req) {},
//     nullptr,
//     [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
//       StaticJsonDocument<256> doc;
//       DeserializationError err = deserializeJson(doc, data, len);
//       if (err) {
//         req->send(400, "application/json", "{\"error\":\"bad json\"}");
//         return;
//       }

//       String newSsid  = doc["ssid"]     | "";
//       String newPass  = doc["password"] | "";
//       String newFlask = doc["flask_ip"] | "";

//       if (newSsid.length() == 0 || newFlask.length() == 0) {
//         req->send(400, "application/json", "{\"error\":\"missing fields\"}");
//         return;
//       }

//       g_ssid     = newSsid;
//       g_password = newPass;
//       g_flask_ip = newFlask;
//       savePreferences(g_ssid, g_password, g_flask_ip);

//       req->send(200, "application/json", "{\"status\":\"saved\"}");

//       // Reconnect STA on a small delay so response can be sent first
//       delay(500);
//       connectSTA();
//     }
//   );

//   // ── POST /reboot  →  Reboot ESP32 ─────────────────────────
//   server.on("/reboot", HTTP_POST, [](AsyncWebServerRequest* req) {
//     req->send(200, "application/json", "{\"status\":\"rebooting\"}");
//     delay(500);
//     ESP.restart();
//   });

//   // ── GET /status  →  JSON health check ─────────────────────
//   server.on("/status", HTTP_GET, [](AsyncWebServerRequest* req) {
//     StaticJsonDocument<256> doc;
//     doc["ap_ssid"]        = AP_SSID;
//     doc["ap_ip"]          = WiFi.softAPIP().toString();
//     doc["sta_ssid"]       = g_ssid;
//     doc["sta_connected"]  = (WiFi.status() == WL_CONNECTED);
//     doc["sta_ip"]         = WiFi.localIP().toString();
//     doc["flask_ip"]       = g_flask_ip;

//     String out;
//     serializeJson(doc, out);
//     req->send(200, "application/json", out);
//   });

//   // ── POST /data  →  Relay payload to Flask ─────────────────
//   //   Body: { "source": "client"|"server", ...rest of payload }
//   server.on("/data", HTTP_POST,
//     [](AsyncWebServerRequest* req) {},
//     nullptr,
//     [](AsyncWebServerRequest* req, uint8_t* data, size_t len, size_t, size_t) {
//       String body = String((char*)data, len);

//       // Cache latest payload by source
//       StaticJsonDocument<512> doc;
//       if (!deserializeJson(doc, body)) {
//         String src = doc["source"] | "unknown";
//         if (src == "client") g_client_payload = body;
//         else if (src == "server") g_server_payload = body;
//       }

//       // Forward to Flask asynchronously (non-blocking would need a task;
//       // for 2s interval polling, a blocking call here is fine)
//       forwardToFlask("/data", body);

//       req->send(200, "application/json", "{\"status\":\"forwarded\"}");
//     }
//   );

//   // ── GET /data  →  Return cached payloads to Defender ──────
//   server.on("/api/data", HTTP_GET, [](AsyncWebServerRequest* req) {
//     String combined = "{\"client_points\":" + g_client_payload
//                     + ",\"server_points\":" + g_server_payload + "}";
//     req->send(200, "application/json", combined);
//   });

//   // ── GET /config  →  Return current config as JSON ─────────
//   //   Used by other ESP32s to fetch stored credentials on boot
//   server.on("/config", HTTP_GET, [](AsyncWebServerRequest* req) {
//     StaticJsonDocument<256> doc;
//     doc["ssid"]         = g_ssid;
//     doc["password"]     = g_password;
//     doc["flask_ip"]     = g_flask_ip;
//     doc["ap_router_ip"] = WiFi.localIP().toString();  // ← add this
//     String out;
//     serializeJson(doc, out);
//     req->send(200, "application/json", out);
//   });

//   // ── 404 catch-all ──────────────────────────────────────────
//   server.onNotFound([](AsyncWebServerRequest* req) {
//     req->send(404, "text/plain", "Not found");
//   });
// }

void setupRoutes() {

  // ── GET /  →  Config page ──────────────────────────────────
  server.on("/", HTTP_GET, [](AsyncWebServerRequest* req) {
    req->send(200, "text/html", buildConfigPage());
  });

  // ── GET /config  →  Return current config as JSON ──────────
  //   Called by Master/Server ESP32s at boot to fetch credentials
  server.on("/config", HTTP_GET, [](AsyncWebServerRequest* req) {
    StaticJsonDocument<256> doc;
    doc["ssid"] = AP_SSID; // ← always ESP32-Config
    doc["password"] = AP_PASSWORD; // ← always admin1234
    doc["flask_ip"] = "192.168.4.1"; // ← AP IP, no Flask needed
    doc["ap_router_ip"] = "192.168.4.1"; // ← same, always static
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

      String newSsid = doc["ssid"] | "";
      String newPass = doc["password"] | "";
      String newFlask = doc["flask_ip"] | "";

      if (newSsid.length() == 0 || newFlask.length() == 0) {
        req->send(400, "application/json", "{\"error\":\"missing fields\"}");
        return;
      }

      g_ssid = newSsid;
      g_password = newPass;
      g_flask_ip = newFlask;
      savePreferences(g_ssid, g_password, g_flask_ip);

      req->send(200, "application/json", "{\"status\":\"saved\"}");
      delay(500);
      //connectSTA();
    }
  );

  // ── POST /reboot  →  Reboot ESP32 ──────────────────────────
  server.on("/reboot", HTTP_POST, [](AsyncWebServerRequest* req) {
    req->send(200, "application/json", "{\"status\":\"rebooting\"}");
    delay(500);
    ESP.restart();
  });

  // ── GET /status  →  JSON health check ──────────────────────
  server.on("/status", HTTP_GET, [](AsyncWebServerRequest* req) {
  StaticJsonDocument<1024> doc;
  doc["ap_ssid"] = AP_SSID;
  doc["ap_ip"] = WiFi.softAPIP().toString();
  doc["sta_ssid"] = g_ssid;
  doc["sta_connected"] = (WiFi.status() == WL_CONNECTED);
  doc["sta_ip"] = WiFi.localIP().toString();
  doc["flask_ip"] = g_flask_ip;
  doc["target_x"] = g_target_x;
  doc["target_y"] = g_target_y;
  doc["encryption"] = g_encryption_status;
  doc["uptime_ms"] = millis();
  doc["client_point_count"] = g_client_arr.size();
  doc["server_point_count"] = g_server_arr.size();
  doc["connected_clients"] = WiFi.softAPgetStationNum();

  // device list
  JsonArray devices = doc.createNestedArray("devices");
  uint32_t now = millis();
  for (auto& kv : g_devices) {
    JsonObject d = devices.createNestedObject();
    d["ip"] = kv.second.ip;
    d["last_seen_s"] = (now - kv.second.lastSeenMs) / 1000;
    d["point_count"] = kv.second.pointCount;
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
      g_devices[clientIP].ip = clientIP;
      g_devices[clientIP].lastSeenMs = millis();
      if (src == "client") {
        if (g_client_arr.size() >= 20) g_client_arr.remove(0);
        g_client_arr.add(incoming.as<JsonObject>());
        g_devices[clientIP].pointCount = g_client_arr.size();
      } else if (src == "server") {
        if (g_server_arr.size() >= 20) g_server_arr.remove(0);
        g_server_arr.add(incoming.as<JsonObject>());
        g_devices[clientIP].pointCount = g_server_arr.size();
      }

      // Return control state
      StaticJsonDocument<128> resp;
      resp["encryption_status"] = g_encryption_status;
      resp["encryption_key"] = g_encryption_key;
      resp["target_x"] = g_target_x;
      resp["target_y"] = g_target_y;

      String out;
      serializeJson(resp, out);
      req->send(200, "application/json", out);
    }
  );

  // ── GET /api/data  →  Serve accumulated points to Defender ─
  server.on("/api/data", HTTP_GET, [](AsyncWebServerRequest* req) {
    DynamicJsonDocument resp(8192);
    resp["encryption_status"] = g_encryption_status;
    resp["encryption_key"] = g_encryption_key;
    resp["target_x"] = g_target_x;
    resp["target_y"] = g_target_y;
    resp["client_points"] = g_client_arr;
    resp["server_points"] = g_server_arr;

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
      g_encryption_key = doc["encryption_key"] | "1234";
      Serial0.printf("[AP-ESP32] Encryption set: %s  key=%s\n",
                    g_encryption_status ? "ON" : "OFF",
                    g_encryption_key.c_str());
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
      Serial0.printf("[AP-ESP32] Target set: (%.1f, %.1f)\n",
                    g_target_x, g_target_y);
      req->send(200, "application/json", "{\"status\":\"ok\"}");
    }
  );

  server.on("/clear", HTTP_POST, [](AsyncWebServerRequest* req) {
      g_client_doc.clear();
      g_server_doc.clear();
      g_client_arr = g_client_doc.to<JsonArray>();
      g_server_arr = g_server_doc.to<JsonArray>();
      g_devices.clear();
      Serial0.println("[AP-ESP32] Telemetry data cleared.");
      req->send(200, "application/json", "{\"status\":\"cleared\"}");
  });

  // ── 404 catch-all ───────────────────────────────────────────
  server.onNotFound([](AsyncWebServerRequest* req) {
    req->send(404, "text/plain", "Not found");
  });
}
