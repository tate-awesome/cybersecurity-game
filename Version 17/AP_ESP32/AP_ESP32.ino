#include <Arduino.h>
#include <WiFi.h>
#include <Preferences.h>          // NVS (non-volatile) storage
#include <ESPAsyncWebServer.h>    // Async web server
#include <HTTPClient.h>           // Forward requests to Flask
#include <ArduinoJson.h>          // JSON relay parsing

// ─── Soft-AP credentials (permanent, never change) ───────────
const char* AP_SSID     = "ESP32-Config";
const char* AP_PASSWORD = "admin1234";
const IPAddress AP_IP   (192, 168, 4, 1);
const IPAddress AP_GW   (192, 168, 4, 1);
const IPAddress AP_SUBNET(255, 255, 255, 0);

// ─── NVS key names ────────────────────────────────────────────
#define NVS_NAMESPACE   "netcfg"
#define NVS_KEY_SSID    "ssid"
#define NVS_KEY_PASS    "password"
#define NVS_KEY_FLASK   "flask_ip"

// ─── Globals ──────────────────────────────────────────────────
Preferences   prefs;
AsyncWebServer server(80);

String g_ssid     = "";
String g_password = "";
String g_flask_ip = "192.168.8.167";


String g_client_payload = "{}";
String g_server_payload = "{}";

#define MAX_POINTS 20 

StaticJsonDocument<8192> g_client_doc;  // stores array of points
StaticJsonDocument<8192> g_server_doc;
JsonArray g_client_arr = g_client_doc.to<JsonArray>();
JsonArray g_server_arr = g_server_doc.to<JsonArray>();

bool g_encryption_status = false;
String g_encryption_key  = "1234";
float g_target_x = 100.0;
float g_target_y = 100.0;

// ─── Forward declarations ─────────────────────────────────────
void loadPreferences();
void savePreferences(const String& ssid, const String& pass, const String& flask_ip);
void startAP();
void connectSTA();
void setupRoutes();
String buildConfigPage();
void forwardToFlask(const String& endpoint, const String& body);

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n[AP-ESP32] Booting...");

  loadPreferences();
  startAP();

  if (g_ssid.length() > 0) {
    connectSTA();
  } else {
    Serial.println("[AP-ESP32] No router SSID saved — skipping STA connect.");
  }

  g_client_arr = g_client_doc.to<JsonArray>();
  g_server_arr = g_server_doc.to<JsonArray>();

  setupRoutes();
  server.begin();
  Serial.println("[AP-ESP32] Web server started on http://192.168.4.1");
}

void loop() {
  // Re-attempt STA connection if it drops
  static uint32_t lastCheckMs = 0;
  if (g_ssid.length() > 0 && millis() - lastCheckMs > 10000) {
    lastCheckMs = millis();
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("[AP-ESP32] STA disconnected — reconnecting...");
      connectSTA();
    }
  }
}

void loadPreferences() {
  prefs.begin(NVS_NAMESPACE, true);   // read-only
  g_ssid     = prefs.getString(NVS_KEY_SSID,  "");
  g_password = prefs.getString(NVS_KEY_PASS,  "");
  g_flask_ip = prefs.getString(NVS_KEY_FLASK, "192.168.8.167");
  prefs.end();

  Serial.printf("[AP-ESP32] Loaded NVS — SSID: '%s'  Flask: '%s'\n",g_ssid.c_str(), g_flask_ip.c_str());
}

void savePreferences(const String& ssid, const String& pass, const String& flask_ip) {
  prefs.begin(NVS_NAMESPACE, false);  // read-write
  prefs.putString(NVS_KEY_SSID,  ssid);
  prefs.putString(NVS_KEY_PASS,  pass);
  prefs.putString(NVS_KEY_FLASK, flask_ip);
  prefs.end();
  Serial.println("[AP-ESP32] Preferences saved to NVS.");
}

void startAP() {
  WiFi.mode(WIFI_AP_STA);   // AP + STA simultaneously
  WiFi.softAPConfig(AP_IP, AP_GW, AP_SUBNET);
  WiFi.softAP(AP_SSID, AP_PASSWORD);
  Serial.printf("[AP-ESP32] Soft-AP started: SSID='%s'  IP=%s\n",AP_SSID, WiFi.softAPIP().toString().c_str());
}

void connectSTA() {
  Serial.printf("[AP-ESP32] Connecting to router SSID='%s'...\n", g_ssid.c_str());
  WiFi.begin(g_ssid.c_str(), g_password.c_str());

  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 10000) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("[AP-ESP32] Router connected — IP: %s\n",
                  WiFi.localIP().toString().c_str());
    
    prefs.begin(NVS_NAMESPACE, false);
    prefs.putString("ap_router_ip", WiFi.localIP().toString());
    prefs.end();
  } else {
    Serial.println("[AP-ESP32] Router connection FAILED (will retry in 10s).");
  }
}

void forwardToFlask(const String& endpoint, const String& body) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[AP-ESP32] Cannot forward — not connected to router.");
    return;
  }

  String url = "http://" + g_flask_ip + ":5000" + endpoint;
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(body);
  Serial.printf("[AP-ESP32] Forwarded to Flask %s  →  HTTP %d\n",
                url.c_str(), code);
  http.end();
}


// ============================================================
//  HTML Config Page
// ============================================================
String buildConfigPage() {
  String staStatus = (WiFi.status() == WL_CONNECTED)
    ? ("&#10003; Connected to <b>" + g_ssid + "</b> (" + WiFi.localIP().toString() + ")")
    : "&#10007; Not connected to router";

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
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .card {
      background: #16213e;
      border: 1px solid #0f3460;
      border-radius: 12px;
      padding: 32px;
      width: 100%;
      max-width: 480px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }

    .header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 1px solid #0f3460;
    }

    .header-icon {
      font-size: 28px;
    }

    h1 {
      font-size: 1.25rem;
      color: #e94560;
      letter-spacing: 0.5px;
    }

    h1 span {
      display: block;
      font-size: 0.75rem;
      color: #888;
      font-weight: normal;
      margin-top: 2px;
      letter-spacing: 0;
    }

    .status-bar {
      background: #0f3460;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.82rem;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .status-bar .label { color: #888; }

    .section-title {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #e94560;
      margin-bottom: 14px;
      margin-top: 24px;
    }

    .form-group {
      margin-bottom: 16px;
    }

    label {
      display: block;
      font-size: 0.82rem;
      color: #aaa;
      margin-bottom: 6px;
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 10px 14px;
      background: #0a0a1a;
      border: 1px solid #0f3460;
      border-radius: 8px;
      color: #e0e0e0;
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s;
    }

    input[type="text"]:focus,
    input[type="password"]:focus {
      border-color: #e94560;
    }

    input[type="text"]::placeholder,
    input[type="password"]::placeholder {
      color: #444;
    }

    .btn {
      width: 100%;
      padding: 12px;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      margin-top: 8px;
      transition: opacity 0.2s, transform 0.1s;
    }

    .btn:active { transform: scale(0.98); }

    .btn-primary {
      background: #e94560;
      color: #fff;
      margin-top: 24px;
    }

    .btn-primary:hover { opacity: 0.9; }

    .btn-secondary {
      background: #0f3460;
      color: #e0e0e0;
      margin-top: 10px;
    }

    .btn-secondary:hover { opacity: 0.85; }

    .toast {
      display: none;
      background: #0f3460;
      border-left: 3px solid #e94560;
      border-radius: 6px;
      padding: 10px 14px;
      font-size: 0.85rem;
      margin-top: 16px;
    }

    .divider {
      border: none;
      border-top: 1px solid #0f3460;
      margin: 24px 0 0;
    }

    .footer {
      font-size: 0.75rem;
      color: #555;
      text-align: center;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="card">

    <div class="header">
      <div class="header-icon">&#128268;</div>
      <h1>ESP32 Network Config
        <span>Access Point / Relay Node</span>
      </h1>
    </div>

    <div class="status-bar">
      <span class="label">Router Status:</span>
      <span>)rawhtml" + staStatus + R"rawhtml(</span>
    </div>

    <!-- ── Router Credentials ── -->
    <div class="section-title">Router Credentials</div>

    <div class="form-group">
      <label for="ssid">Network SSID</label>
      <input type="text" id="ssid" name="ssid"
             placeholder="e.g. MyLabRouter"
             value=")rawhtml" + g_ssid + R"rawhtml(">
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" name="password"
             placeholder="Router password">
    </div>

    <!-- ── Flask Server ── -->
    <div class="section-title">Flask Server</div>

    <div class="form-group">
      <label for="flask_ip">Flask Server IP</label>
      <input type="text" id="flask_ip" name="flask_ip"
             placeholder="e.g. 192.168.8.167"
             value=")rawhtml" + g_flask_ip + R"rawhtml(">
    </div>

    <button class="btn btn-primary" onclick="saveConfig()">
      &#128190; Save &amp; Reconnect
    </button>

    <button class="btn btn-secondary" onclick="rebootDevice()">
      &#128260; Reboot ESP32
    </button>

    <div class="toast" id="toast"></div>

    <hr class="divider">
    <div class="footer">
      AP IP: 192.168.4.1 &nbsp;|&nbsp; Soft-AP: ESP32-Config
    </div>

  </div>

  <script>
    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 4000);
    }

    async function saveConfig() {
      const ssid     = document.getElementById('ssid').value.trim();
      const password = document.getElementById('password').value;
      const flask_ip = document.getElementById('flask_ip').value.trim();

      if (!ssid) { showToast('SSID cannot be empty.'); return; }
      if (!flask_ip) { showToast('Flask IP cannot be empty.'); return; }

      const resp = await fetch('/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ssid, password, flask_ip })
      });

      if (resp.ok) {
        showToast('Saved! Reconnecting to router...');
        setTimeout(() => location.reload(), 4000);
      } else {
        showToast('Error saving config.');
      }
    }

    async function rebootDevice() {
      await fetch('/reboot', { method: 'POST' });
      showToast('Rebooting ESP32...');
    }
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
    doc["ssid"]         = g_ssid;
    doc["password"]     = g_password;
    doc["flask_ip"]     = g_flask_ip;
    doc["ap_router_ip"] = WiFi.localIP().toString();
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
      connectSTA();
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
    StaticJsonDocument<256> doc;
    doc["ap_ssid"]       = AP_SSID;
    doc["ap_ip"]         = WiFi.softAPIP().toString();
    doc["sta_ssid"]      = g_ssid;
    doc["sta_connected"] = (WiFi.status() == WL_CONNECTED);
    doc["sta_ip"]        = WiFi.localIP().toString();
    doc["flask_ip"]      = g_flask_ip;
    doc["target_x"]      = g_target_x;
    doc["target_y"]      = g_target_y;
    doc["encryption"]    = g_encryption_status;
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

      // Tag with AP-side timestamp (seconds since boot)
      incoming["received_at"] = String(millis() / 1000);

      String src = incoming["source"] | "unknown";

      if (src == "client") {
        if (g_client_arr.size() >= MAX_POINTS) g_client_arr.remove(0);
        g_client_arr.add(incoming.as<JsonObject>());
      } else if (src == "server") {
        if (g_server_arr.size() >= MAX_POINTS) g_server_arr.remove(0);
        g_server_arr.add(incoming.as<JsonObject>());
      }

      // Return control state back to the posting ESP32
      // (replaces what Flask used to return)
      StaticJsonDocument<128> resp;
      resp["encryption_status"] = g_encryption_status;
      resp["encryption_key"]    = g_encryption_key;
      resp["target_x"]          = g_target_x;
      resp["target_y"]          = g_target_y;

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
      Serial.printf("[AP-ESP32] Encryption set: %s  key=%s\n",
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
      Serial.printf("[AP-ESP32] Target set: (%.1f, %.1f)\n",
                    g_target_x, g_target_y);
      req->send(200, "application/json", "{\"status\":\"ok\"}");
    }
  );

  // ── 404 catch-all ───────────────────────────────────────────
  server.onNotFound([](AsyncWebServerRequest* req) {
    req->send(404, "text/plain", "Not found");
  });
}