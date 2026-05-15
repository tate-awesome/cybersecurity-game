#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "GL-SFT1200-ab1";
const char* password = "goodlife";

// MQTT
const char* mqtt_server = "192.168.0.1";
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// State received from MQTT
float mqtt_x = 0.0f;
float mqtt_y = 0.0f;
float mqtt_theta = 0.0f;
bool dataReceived = false;

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  char msg[32];
  memcpy(msg, payload, length);
  msg[length] = '\0';
  
  if (strcmp(topic, "vessel/state/x") == 0) {
    mqtt_x = atof(msg);
    Serial.printf("[DEFENDER] Received X: %.3f\n", mqtt_x);
    dataReceived = true;
  } else if (strcmp(topic, "vessel/state/y") == 0) {
    mqtt_y = atof(msg);
    Serial.printf("[DEFENDER] Received Y: %.3f\n", mqtt_y);
    dataReceived = true;
  } else if (strcmp(topic, "vessel/state/theta") == 0) {
    mqtt_theta = atof(msg);
    Serial.printf("[DEFENDER] Received Theta: %.4f rad\n", mqtt_theta);
    dataReceived = true;
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);
  
  Serial.println("\n[DEFENDER] Booting...");
  
  // WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("[DEFENDER] Connecting to WiFi");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(300);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\n[DEFENDER] WiFi FAILED!");
    while(1) delay(1000);
  }
  
  Serial.printf("\n[DEFENDER] WiFi Connected - IP: %s\n", WiFi.localIP().toString().c_str());
  
  // MQTT with unique client ID
  mqttClient.setServer(mqtt_server, 1883);
  mqttClient.setCallback(mqttCallback);
  mqttClient.setKeepAlive(60);
  
  // Generate unique client ID
  String clientId = "Defender-";
  clientId += String((uint32_t)ESP.getEfuseMac(), HEX);
  
  Serial.printf("[DEFENDER] Connecting to MQTT broker: %s\n", mqtt_server);
  Serial.printf("[DEFENDER] Client ID: %s\n", clientId.c_str());
  
  if (mqttClient.connect(clientId.c_str())) {
    Serial.println("[DEFENDER] MQTT Connected!");
    
    mqttClient.subscribe("vessel/state/x");
    mqttClient.subscribe("vessel/state/y");
    mqttClient.subscribe("vessel/state/theta");
    
    Serial.println("[DEFENDER] Subscribed to topics:");
    Serial.println("  - vessel/state/x");
    Serial.println("  - vessel/state/y");
    Serial.println("  - vessel/state/theta");
  } else {
    Serial.printf("[DEFENDER] MQTT Connection FAILED! State: %d\n", mqttClient.state());
  }
  
  Serial.println("[DEFENDER] Ready - Waiting for messages...\n");
}

void loop() {
  // Reconnect if needed
  if (!mqttClient.connected()) {
    static uint32_t lastReconnect = 0;
    if (millis() - lastReconnect > 5000) {
      lastReconnect = millis();
      
      String clientId = "Defender-";
      clientId += String((uint32_t)ESP.getEfuseMac(), HEX);
      
      Serial.println("[DEFENDER] MQTT disconnected, reconnecting...");
      Serial.printf("[DEFENDER] Client ID: %s, Broker: %s\n", clientId.c_str(), mqtt_server);
      
      if (mqttClient.connect(clientId.c_str())) {
        mqttClient.subscribe("vessel/state/x");
        mqttClient.subscribe("vessel/state/y");
        mqttClient.subscribe("vessel/state/theta");
        Serial.println("[DEFENDER] Reconnected to MQTT");
      } else {
        Serial.printf("[DEFENDER] Reconnect failed! State: %d\n", mqttClient.state());
      }
    }
  }
  
  mqttClient.loop();
  
  // Print current state every 2 seconds
  static uint32_t lastPrint = 0;
  if (millis() - lastPrint > 2000) {
    lastPrint = millis();
    
    if (mqttClient.connected()) {
      Serial.println("─────────────────────────────────");
      Serial.printf("[DEFENDER] MQTT Status: Connected\n");
      Serial.printf("[DEFENDER] Data received: %s\n", dataReceived ? "Yes" : "No");
      Serial.printf("[DEFENDER] Current State:\n");
      Serial.printf("  X:     %.3f m\n", mqtt_x);
      Serial.printf("  Y:     %.3f m\n", mqtt_y);
      Serial.printf("  Theta: %.4f rad (%.1f°)\n", mqtt_theta, mqtt_theta * 57.2958);
      Serial.println("─────────────────────────────────");
    } else {
      Serial.println("[DEFENDER] MQTT Status: DISCONNECTED");
    }
  }
  
  delay(10);
}