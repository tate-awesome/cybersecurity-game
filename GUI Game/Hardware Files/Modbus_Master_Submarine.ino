// Modbus Master (ESP32 main)

#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

const char* ssid = "JairoWifi";
const char* password = "12345678";

#define RUDDER_REG 100
#define SPEED_REG 101
#define X_REG 102
#define Y_REG 103
#define HEADING_REG 104

uint16_t set_cb(TRegister* reg, uint16_t speed);
uint16_t rudder_cb(TRegister* reg, uint16_t rudder);

ModbusIP mb;

uint16_t speed = 0.0;
float x = 2.0;
float y = 2.0;
float heading = 0.75;
uint16_t rudder = 0.0;
float rudder_2 = 0.0;
float speed_2 = 0.0;
float dt = 0.05;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("Combined Code: Modbus Master + PID Controller");

  // ============ WIFI Setup and Init ============
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Print your local IP address:
  Serial.print("TCP Server IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Please update the serverAddress in ESP32 #1 code");

  // ========= MODBUS ========
  // Init modbus server
  mb.server();

  // Add the registers to listen to
  mb.addHreg(0, 0);
  mb.addHreg(RUDDER_REG, 0);
  mb.addHreg(SPEED_REG, 0);
  mb.addHreg(X_REG, 0);
  mb.addHreg(Y_REG,0);
  mb.addHreg(HEADING_REG,0);

  // Whenever the register offset is changed, invoke the callback
  mb.onSetHreg(SPEED_REG, set_cb);
  mb.onSetHreg(RUDDER_REG, rudder_cb);
}

void loop() {
  mb.task();
  delay(10);
}

uint16_t set_cb(TRegister* reg, uint16_t data) 
{
  Serial.println("SET callback");
  speed = ((float)data); // Cast the recieved 16 bit data into float
  speed_2 = ((float)speed / 10000.0); 
  // rudder = mb.Hreg(RUDDER_REG);
  Serial.print("\t");
  Serial.println(speed_2);

  // Calculate the current heading and position
  x += (speed_2 * cos(heading) * dt);
  Serial.println(speed_2 * sin(heading)* dt);
  y = y + (speed_2 * sin(heading) * dt);
  heading = heading + (0.6/(0.1/tan(rudder_2) )* dt);

  Serial.print("Position is ");
  Serial.print(x);
  Serial.print("\t");
  Serial.print(y);
  Serial.print("\t");
  Serial.print("Heading is ");
  Serial.println(heading);

  // Scale up floats to fit in uint16_t
  float xT = (x * 256);
  float yT = (y * 256);
  float headingT = (heading * 256);

  //Send 'Podsition' value to the Modbus slave
  Serial.print("Send Vals: ");
  Serial.print(xT);
  Serial.print("\t");
  Serial.print(yT);
  Serial.print("\t");
  Serial.println(headingT);

  // Write the positon and heading to the registers
  mb.Hreg(X_REG, round(xT));
  // mb.Hreg(X_REG, 5);
  mb.Hreg(Y_REG, round(yT));
  // mb.Hreg(Y_REG, 4);
  mb.Hreg(HEADING_REG, round(headingT));
  // mb.Hreg(HEADING_REG, 3);
  //delay(dt * 100);
  return xT;
  // return yT;
  // return headingT;
}

uint16_t rudder_cb(TRegister* reg, uint16_t data) {
  //get rudder value from controller
  Serial.println("RUDDER CB");
  rudder = ((float)data);
  rudder_2 = ((float)rudder / 5000.0-5);
  Serial.println(rudder_2);
  return rudder_2;
}