#include <Servo.h>
#include <Adafruit_LiquidCrystal.h>
Adafruit_LiquidCrystal lcd_1(0);
Servo S1,S2;
long duration,duration1;
float distance,distance1;
float num=60;
void setup()
{
  pinMode(12,OUTPUT);
  pinMode(13,INPUT);
  pinMode(9,INPUT);
  pinMode(6,OUTPUT);
  pinMode(2,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  S1.attach(10);
  S2.attach(11);
  lcd_1.begin(16,2);
  //lcd_1.print("Hello Human");
  S1.write(90);
  S2.write(90);
  Serial.begin(9600);
}
void loop()
{
  
  digitalWrite(6,LOW);  //ULTRASONIC 1 begin
  delay(2);
  digitalWrite(6,HIGH);
  delay(10);
  digitalWrite(6,LOW);
  duration=pulseIn(9,HIGH);
  distance=duration*0.034/2;  //ULTRASONIC 1 end
  
  digitalWrite(12,LOW);  //ULTRASONIC 2 begin
  delay(2);
  digitalWrite(12,HIGH);
  delay(10);
  digitalWrite(12,LOW);
  duration1=pulseIn(13,HIGH);
  distance1=duration1*0.034/2; //ULTRASONIC 2 end
  
  if(distance>60 && distance1<=250)
  {
    lcd_1.clear();
    lcd_1.print("DUSTBIN");
    delay(1000);
  }

  if(distance1<=250)
  {
  if(distance<=num)
  {
    lcd_1.clear();
    lcd_1.setCursor(0,0);
    lcd_1.print("Please drop the");
    lcd_1.setCursor(0,1);
    lcd_1.print("trash");
    S1.write(0);
    S2.write(0);
    delay(3000);
  }
  else
  {
    S1.write(90);
    S2.write(90);
    delay(1000);
  } 
  }
  else
  {
    if(distance>num || distance<=num)
    {
    S1.write(90);
    S2.write(90);
    lcd_1.clear();
    lcd_1.setCursor(0,0);
    lcd_1.print("Trash full");
    lcd_1.setCursor(0,1);
    lcd_1.print("Bot on move");
    delay(3000);
    }
}
  if(distance1>250)
  {
    digitalWrite(2,HIGH);
    digitalWrite(4,LOW);
    digitalWrite(7,HIGH);
    digitalWrite(8,LOW);
  
  }
  else
  {
    digitalWrite(2,LOW);
    digitalWrite(4,LOW);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
  }
    
}
