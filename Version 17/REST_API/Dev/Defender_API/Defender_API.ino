#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ─── CONFIG 
const char* WIFI_SSID     = "GL-SFT1200-ab1";
const char* WIFI_PASSWORD = "goodlife";
const char* SERVER_URL    = "http://192.168.8.167:5000/data";  // Host IP + Flask port

const int   POST_INTERVAL_MS = 5000;   // How often to POST (ms)
float       x = 42.7;

HTTPClient http;

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.printf("\nConnecting to %s", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nConnected! IP: %s\n", WiFi.localIP().toString().c_str());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    sendData();
  } else {
    Serial.println("[ERROR] WiFi disconnected – reconnecting…");
    WiFi.reconnect();
  }
  delay(POST_INTERVAL_MS);
}

void sendData() {
  // JSON payload
  StaticJsonDocument<128> doc;
  doc["timestamp"] = (uint32_t)(millis() / 1000);  // seconds since boot
  doc["x"]         = x;

  String payload;
  serializeJson(doc, payload);

  // POST request
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");

  Serial.printf("[POST] %s  →  %s\n", SERVER_URL, payload.c_str());
  int statusCode = http.POST(payload);

  if (statusCode > 0) {
    String response = http.getString();
    Serial.printf("[Response %d] %s\n", statusCode, response.c_str());

    StaticJsonDocument<128> resp;
    DeserializationError err = deserializeJson(resp, response);
    if (!err && resp.containsKey("set_x")) {
      x = resp["set_x"].as<float>();
      Serial.printf("[Command] x updated to %.2f\n", x);
    }
  } else {
    Serial.printf("[ERROR] HTTP POST failed: %s\n", http.errorToString(statusCode).c_str());
  }

  http.end();
}
