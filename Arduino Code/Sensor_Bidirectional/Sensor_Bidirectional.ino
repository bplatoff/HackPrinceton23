#include "Wire.h"
#include "DHT.h"
#define DHTTYPE DHT20   // DHT 20

DHT dht(DHTTYPE);         //   DHT10 DHT20 don't need to define Pin

#if defined(ARDUINO_ARCH_AVR)
#define debug  Serial

#elif defined(ARDUINO_ARCH_SAMD) ||  defined(ARDUINO_ARCH_SAM)
#define debug  SerialUSB
#else
#define debug  Serial
#endif

int pwm1 = 9;
int pwm2 = 10;
int ctr_a = 9;
int ctr_b = 8;
int ctr_c = 11;
int ctr_d = 10;
int moisture_pin = A2;
int light_pin = A6;
//int temp_pin = 3;
int sd = 6;
int i = 0;
int t = 1500;
int light_value = 0;
int moisture_value = 0;
int rot_type = 0;
int loop_iteration = 0;

void setup()
{
  //pinMode(sd,OUTPUT);
  //pinMode(pwm1,OUTPUT);
  //pinMode(pwm2,OUTPUT);
  pinMode(ctr_a, OUTPUT);
  pinMode(ctr_b, OUTPUT);
  pinMode(ctr_c, OUTPUT);
  pinMode(ctr_d, OUTPUT);
  pinMode(moisture_pin, INPUT);
  pinMode(light_pin, INPUT);
  //pinMode(temp_pin, INPUT);
  Serial.begin(9600);
  delay(1);
  //digitalWrite(sd,HIGH);
  //digitalWrite(pwm1,HIGH);
  //digitalWrite(pwm2,HIGH);
  //    digitalWrite(ctr_a,LOW);
  //    digitalWrite(ctr_b,LOW);
  //    digitalWrite(ctr_c,LOW);
  //    digitalWrite(ctr_d,LOW);
  //debug.begin(9600);
  //debug.println("DHTxx test!");
  Wire.begin();
  dht.begin();

}


void loop ()
{
  //5 times a second we will check for incoming turn commands
  //every 2 seconds we will send telemetry data
  //if a turn command is sent data will be shared
  if (loop_iteration == 10) {
    //need to send telemetry
    float temp_hum_val[2] = {0};

    if (!dht.readTempAndHumidity(temp_hum_val)) {
      Serial.print("Humidity: ");
      Serial.print(temp_hum_val[0]);
      Serial.println(" %");
      Serial.print("Temperature: ");
      Serial.print(temp_hum_val[1]);
      Serial.println(" *C");
    } else {
      Serial.println("Failed to get temprature and humidity value.");
    }

    light_value = analogRead(light_pin);
    Serial.print("Light Value: ");
    Serial.println(light_value);
    moisture_value = analogRead(moisture_pin);
    Serial.print("Moisture Value: ");
    Serial.println(moisture_value);
    Serial.println();
    loop_iteration = 0;
  } else {
    loop_iteration = loop_iteration + 1;
  }

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "turn") {
      if (rot_type == 0) {
        for (i = 255; i >= 1; i--)
        {
          digitalWrite(ctr_d, HIGH); //D
          delayMicroseconds(t);
          digitalWrite(ctr_c, HIGH); //DC
          delayMicroseconds(t);
          digitalWrite(ctr_d, LOW); //C
          delayMicroseconds(t);
          digitalWrite(ctr_b, HIGH); //CB
          delayMicroseconds(t);
          digitalWrite(ctr_c, LOW); //B
          delayMicroseconds(t);
          digitalWrite(ctr_a, HIGH); //BA
          delayMicroseconds(t);
          digitalWrite(ctr_b, LOW); //A
          delayMicroseconds(t);
          digitalWrite(ctr_d, HIGH); //AD
          delayMicroseconds(t);
          digitalWrite(ctr_a, LOW);
          digitalWrite(ctr_d, LOW);
        }
        rot_type = 1;
      } else {
        for (i = 255; i >= 1; i--)
        {
          digitalWrite(ctr_a, LOW); //A
          digitalWrite(ctr_b, HIGH);
          digitalWrite(ctr_c, HIGH);
          digitalWrite(ctr_d, HIGH);
          delayMicroseconds(t);
          digitalWrite(ctr_a, LOW);
          digitalWrite(ctr_b, LOW); //AB
          digitalWrite(ctr_c, HIGH);
          digitalWrite(ctr_d, HIGH);
          delayMicroseconds(t);
          digitalWrite(ctr_a, HIGH);
          digitalWrite(ctr_b, LOW); //B
          digitalWrite(ctr_c, HIGH);
          digitalWrite(ctr_d, HIGH);
          delayMicroseconds(t);
          digitalWrite(ctr_a, HIGH);
          digitalWrite(ctr_b, LOW);
          digitalWrite(ctr_c, LOW); //BC
          digitalWrite(ctr_d, HIGH);
          delayMicroseconds(t);
          digitalWrite(ctr_a, HIGH);
          digitalWrite(ctr_b, HIGH);
          digitalWrite(ctr_c, LOW); //C
          digitalWrite(ctr_d, HIGH);
          delayMicroseconds(t);
          digitalWrite(ctr_a, HIGH);
          digitalWrite(ctr_b, HIGH);
          digitalWrite(ctr_c, LOW); //CD
          digitalWrite(ctr_d, LOW);
          delayMicroseconds(t);
          digitalWrite(ctr_a, HIGH);
          digitalWrite(ctr_b, HIGH);
          digitalWrite(ctr_c, HIGH); //D
          digitalWrite(ctr_d, LOW);
          delayMicroseconds(t);
          digitalWrite(ctr_a, LOW);
          digitalWrite(ctr_b, HIGH);
          digitalWrite(ctr_c, HIGH); //DA
          digitalWrite(ctr_d, LOW);
          delayMicroseconds(t);

        }
        digitalWrite(ctr_a, HIGH);
        digitalWrite(ctr_b, HIGH);
        digitalWrite(ctr_c, HIGH);
        digitalWrite(ctr_d, HIGH);
        rot_type = 0;
      }
      Serial.println("turn_complete");
      float temp_hum_val[2] = {0};

      if (!dht.readTempAndHumidity(temp_hum_val)) {
        Serial.print("Humidity: ");
        Serial.print(temp_hum_val[0]);
        Serial.println(" %");
        Serial.print("Temperature: ");
        Serial.print(temp_hum_val[1]);
        Serial.println(" *C");
      } else {
        Serial.println("Failed to get temprature and humidity value.");
      }

      light_value = analogRead(light_pin);
      Serial.print("Light Value: ");
      Serial.println(light_value);
      moisture_value = analogRead(moisture_pin);
      Serial.print("Moisture Value: ");
      Serial.println(moisture_value);
      Serial.println();
      loop_iteration = 0;
    }
  }


  delay(200);

}
