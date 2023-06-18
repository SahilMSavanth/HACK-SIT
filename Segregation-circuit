#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>
Adafruit_LiquidCrystal lcd_1(0);
Servo S;
float moisture=0;
int position=0;
void setup()
{
  pinMode(A0,INPUT);
  pinMode(2,OUTPUT);
  lcd_1.begin(16,2);
  S.attach(3);
  S.write(90);
  Serial.begin(9600);
}

void loop()
{
 digitalWrite(2,HIGH);
 delay(10);
 moisture=analogRead(A0);
 digitalWrite(2,LOW);
 Serial.println(moisture);
 if(moisture<=5.00)
 {
   S.write(90);
   lcd_1.print("Segregating....."); 
 }
  
 else if(moisture<=359.00 && moisture>5.00)
 {
   lcd_1.print("Dry waste");
   S.write(170);
   delay(1000);
   S.write(90);
   delay(1000);
 }
  else
  {
    lcd_1.print("Wet waste");
    S.write(20);
    delay(1000);
    S.write(90);
    delay(1000);
  }
  lcd_1.clear();
}
