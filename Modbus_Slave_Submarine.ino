// Modbus Slave (Client) -- ESP32 (w/o velocio)

#include <ezButton.h>
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

#define BUTTON_PIN 20
#define Xpos_pin 2
#define Ypos_pin 42
#define heading_pin 1
#define DIGITAL_PIN_7 12
#define DIGITAL_PIN_8 13
#define DIGITAL_PIN_9 11
#define DIGITAL_PIN_10 10
#define DIGITAL_PIN_11 9
#define DIGITAL_PIN_12 46

#define DIGITAL_PIN_1 3
#define DIGITAL_PIN_2 8
#define DIGITAL_PIN_3 18
#define DIGITAL_PIN_4 17
#define DIGITAL_PIN_5 16
#define DIGITAL_PIN_6 15

#define RUDDER_REG 100
#define SPEED_REG 101
#define X_REG 102
#define Y_REG 103
#define HEADING_REG 104

//const char* ssid = "GL-SFT1200-ab1";
//const char* password = "goodlife";
const char* ssid = "JairoWifi";
const char* password = "12345678";
ezButton button(BUTTON_PIN);
IPAddress remote(192, 168, 137, 77);

ModbusIP mb;

float x = 0.0, y = 0.0, theta = 0.0;
float dt = 1;
float L = 0.1;
// float target_x = -20, target_y = -10;
float target_x = 5, target_y = 5;

void setup()
{
  Serial.begin(115200);
  button.setDebounceTime(50);

  Serial.println("ESP32: Modbus Slave + A BUTTON/SWITCH");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  mb.client();
  mb.addHreg(RUDDER_REG,0);
  mb.addHreg(SPEED_REG,0);
  mb.addHreg(X_REG,0);
  mb.addHreg(Y_REG,0);
  mb.addHreg(HEADING_REG,0);
}

static uint16_t recvx = 0.0;
static uint16_t recvy = 0.0;
static uint16_t recvheading = 0.0;
uint16_t speed = 0;
uint16_t rudder = 0;
uint16_t valueToSend = 0;

void loop()
{
  button.loop();

  if (mb.isConnected(remote))
  {      
    uint16_t pos[3];                                              // Check if connection to Modbus Slave is established
    // Initiate Read Hreg from Modbus Server
    uint16_t trans = mb.readHreg(remote, X_REG, pos, 3);
  
    while (mb.isTransaction(trans))
    { // Check if transaction is active
      mb.task();
      
      delay(10);
    }
    Serial.println("Received sensor data");
    Serial.print(pos[0]);
    Serial.print("\t");
    Serial.print(pos[1]);
    Serial.print("\t");
    Serial.println(pos[2]);

    theta = pos[2] / 256.0;
    x = pos[0] / 256.0;
    y = pos[1] / 256.0;
    
    Serial.println("Sensor Data");
    Serial.print(x);
    Serial.print("\t");
    Serial.print(y);
    Serial.print("\t");
    Serial.println(theta);

    float head_x = x + 2 * cos(theta);
    float head_y = y + 2 * sin(theta);
        
    float rho = 0.1 * (atan2(target_y - y, target_x - x) - theta);
    float v = 0.5 * sqrt(abs(target_x - head_x) + abs(target_y - head_y));

    if (abs(target_x - head_x) + abs(target_y - head_y) <= 0.5) {
        v = 0;
    }

    Serial.println("Control Command (ValuesToSend):");
    Serial.println("Speed \t");
    Serial.println(v);
    Serial.println("Rudder angle \t");
    Serial.println(rho);

    trans = mb.writeHreg(remote, RUDDER_REG, (rho+5) * 5000); // Initiate Read Hreg from Modbus Server
 // Initiate Read Hreg from Modbus Server
    while (mb.isTransaction(trans))
    { // Check if transaction is active
      // Serial.println("Transmitting ...");
      mb.task();
      delay(10);
    }

    trans = mb.writeHreg(remote, SPEED_REG, v * 10000); // Initiate Read Hreg from Modbus Server
 // Initiate Read Hreg from Modbus Server
    while (mb.isTransaction(trans))
    { // Check if transaction is active
      // Serial.println("Transmitting ...");
      mb.task();
      delay(10);
    }
  }
  else
  {
     mb.connect(remote,502); // Try to connect if no connection
   }

  delay(100);
}