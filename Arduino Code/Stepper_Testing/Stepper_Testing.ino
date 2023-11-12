int pwm1=9;
int pwm2=10;
int ctr_a =9;
int ctr_b =8;
int ctr_c =11;
int ctr_d =10;
int sd =6;
int i=0;
int t=1500;

void setup()
{
    //pinMode(sd,OUTPUT);
    //pinMode(pwm1,OUTPUT);
    //pinMode(pwm2,OUTPUT);
    pinMode(ctr_a,OUTPUT);
    pinMode(ctr_b,OUTPUT);
    pinMode(ctr_c,OUTPUT);
    pinMode(ctr_d,OUTPUT);
    Serial.begin(9600);
    delay(1);
    //digitalWrite(sd,HIGH);
    //digitalWrite(pwm1,HIGH);
    //digitalWrite(pwm2,HIGH);
//    digitalWrite(ctr_a,LOW);
//    digitalWrite(ctr_b,LOW);
//    digitalWrite(ctr_c,LOW);
//    digitalWrite(ctr_d,LOW);
        
}


void loop ()
{
//   for(i=1500;i>=1;i--)
//   {
//       digitalWrite(ctr_a,HIGH);//A
//       digitalWrite(ctr_b,LOW);
//       digitalWrite(ctr_c,LOW);
//       digitalWrite(ctr_d,LOW);
//       delayMicroseconds(t);
//       digitalWrite(ctr_a,HIGH);
//       digitalWrite(ctr_b,HIGH);//AB
//       digitalWrite(ctr_c,LOW);
//       digitalWrite(ctr_d,LOW);
//       delayMicroseconds(t);
//       digitalWrite(ctr_a,LOW);
//       digitalWrite(ctr_b,HIGH);//B
//       digitalWrite(ctr_c,LOW);
//       digitalWrite(ctr_d,LOW);
//       delayMicroseconds(t);
//       digitalWrite(ctr_a,LOW);
//       digitalWrite(ctr_b,HIGH);
//       digitalWrite(ctr_c,HIGH);//BC
//        digitalWrite(ctr_d,LOW);
//       delayMicroseconds(t);
//       digitalWrite(ctr_a,LOW);
//       digitalWrite(ctr_b,LOW);
//       digitalWrite(ctr_c,HIGH);//C
//       digitalWrite(ctr_d,LOW);
//       delayMicroseconds(t);
//       digitalWrite(ctr_a,LOW);
//       digitalWrite(ctr_b,LOW);
//       digitalWrite(ctr_c,HIGH);//CD
//       digitalWrite(ctr_d,HIGH);
//       delayMicroseconds(t);
//        digitalWrite(ctr_a,LOW);
//       digitalWrite(ctr_b,LOW);
//       digitalWrite(ctr_c,LOW);//D
//       digitalWrite(ctr_d,HIGH);
//       delayMicroseconds(t);
//        digitalWrite(ctr_a,HIGH);
//       digitalWrite(ctr_b,LOW);
//       digitalWrite(ctr_c,LOW);//DA
//       digitalWrite(ctr_d,HIGH);
//       delayMicroseconds(t);
//       
//   }
//       digitalWrite(ctr_a,LOW);
//       digitalWrite(ctr_b,LOW);
//       digitalWrite(ctr_c,LOW);
//       digitalWrite(ctr_d,LOW);
//   
//   
//   
     Serial.println("Clockwise");
     for(i=255;i>=1;i--)
   {
       digitalWrite(ctr_d,HIGH);//D
       delayMicroseconds(t);
       digitalWrite(ctr_c,HIGH);//DC
       delayMicroseconds(t);
       digitalWrite(ctr_d,LOW);//C
       delayMicroseconds(t);
       digitalWrite(ctr_b,HIGH);//CB
       delayMicroseconds(t);
       digitalWrite(ctr_c,LOW);//B
       delayMicroseconds(t);
       digitalWrite(ctr_a,HIGH);//BA
       delayMicroseconds(t);
       digitalWrite(ctr_b,LOW);//A
       delayMicroseconds(t);
       digitalWrite(ctr_d,HIGH);//AD
       delayMicroseconds(t);
       digitalWrite(ctr_a,LOW);
       digitalWrite(ctr_d,LOW);
   }
   delay(2000);

   Serial.println("Counterclockwise");
   for(i=255;i>=1;i--)
   {
       digitalWrite(ctr_a,LOW);//A
       digitalWrite(ctr_b,HIGH);
       digitalWrite(ctr_c,HIGH);
       digitalWrite(ctr_d,HIGH);
       delayMicroseconds(t);
       digitalWrite(ctr_a,LOW);
       digitalWrite(ctr_b,LOW);//AB
       digitalWrite(ctr_c,HIGH);
       digitalWrite(ctr_d,HIGH);
       delayMicroseconds(t);
       digitalWrite(ctr_a,HIGH);
       digitalWrite(ctr_b,LOW);//B
       digitalWrite(ctr_c,HIGH);
       digitalWrite(ctr_d,HIGH);
       delayMicroseconds(t);
       digitalWrite(ctr_a,HIGH);
       digitalWrite(ctr_b,LOW);
       digitalWrite(ctr_c,LOW);//BC
        digitalWrite(ctr_d,HIGH);
       delayMicroseconds(t);
       digitalWrite(ctr_a,HIGH);
       digitalWrite(ctr_b,HIGH);
       digitalWrite(ctr_c,LOW);//C
       digitalWrite(ctr_d,HIGH);
       delayMicroseconds(t);
       digitalWrite(ctr_a,HIGH);
       digitalWrite(ctr_b,HIGH);
       digitalWrite(ctr_c,LOW);//CD
       digitalWrite(ctr_d,LOW);
       delayMicroseconds(t);
        digitalWrite(ctr_a,HIGH);
       digitalWrite(ctr_b,HIGH);
       digitalWrite(ctr_c,HIGH);//D
       digitalWrite(ctr_d,LOW);
       delayMicroseconds(t);
       digitalWrite(ctr_a,LOW);
       digitalWrite(ctr_b,HIGH);
       digitalWrite(ctr_c,HIGH);//DA
       digitalWrite(ctr_d,LOW);
       delayMicroseconds(t);
       
   }
       digitalWrite(ctr_a,HIGH);
       digitalWrite(ctr_b,HIGH);
       digitalWrite(ctr_c,HIGH);
       digitalWrite(ctr_d,HIGH);
        delay(2000);
   
//      Serial.println("Phase 3");
//     for(i=500;i>=1;i--)
//   {
//       digitalWrite(ctr_d,HIGH);//D
//       delay(t);
//       digitalWrite(ctr_c,HIGH);//DC
//       delay(t);
//       digitalWrite(ctr_d,LOW);//C
//       delay(t);
//       digitalWrite(ctr_b,HIGH);//CB
//       delay(t);
//       digitalWrite(ctr_c,LOW);//B
//       delay(t);
//       digitalWrite(ctr_a,HIGH);//BA
//       delay(t);
//       digitalWrite(ctr_b,LOW);//A
//       delay(t);
//       digitalWrite(ctr_d,HIGH);//AD
//       delay(t);
//       digitalWrite(ctr_a,LOW);
//       digitalWrite(ctr_d,LOW);
//   }
   

}
