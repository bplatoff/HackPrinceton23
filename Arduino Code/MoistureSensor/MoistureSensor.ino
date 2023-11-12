// Light Switch
int sensorpin = A2; // Analog input pin that the sensor is attached to
int sensorValue = 0;// value read from the port
int cal_value = 0;
int iteration_num = 0;
int sample_value = 0;

void setup() {
  //pinMode(ledPin,OUTPUT);
  pinMode(sensorpin, INPUT);
  Serial.begin(9600);
  cal_value = analogRead(sensorpin);
  Serial.print("Cal Value: ");
  Serial.println(cal_value);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(sensorpin);
  sample_value = sample_value + sensorValue;
  if (iteration_num == 30){
    Serial.print("Average Val: ");
    int ave_val = sample_value/30;
    Serial.println(ave_val);
    sample_value = 0;
    iteration_num = 0;
  }else{
    iteration_num = iteration_num + 1;
  }
  delay(100);
  
}
