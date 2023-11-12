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
  pinMode(ctr_a, OUTPUT);
  pinMode(ctr_b, OUTPUT);
  pinMode(ctr_c, OUTPUT);
  pinMode(ctr_d, OUTPUT);
  delay(1);
  
}



void loop (){
for(i=200;i>=1;i--)
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
    delay(50);
}
delay(2000);
}
