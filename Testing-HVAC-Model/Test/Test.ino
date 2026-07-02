void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.printf("Flash size: %d MB\n", ESP.getFlashChipSize() / (1024*1024));
  Serial.printf("PSRAM size: %d MB\n", ESP.getPsramSize() / (1024*1024));
  Serial.printf("Free heap: %d bytes\n", ESP.getFreeHeap());
}

void loop() {
  
}