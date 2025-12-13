#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

const int ldrPin = 34;
const int potPin = 32;

const int headlightLED = 4;
const int leftIndLED = 16;
const int rightIndLED = 17;

const int buttonPin = 15;
const int hazardPin = 18;

#define DHTPIN 27
#define DHTTYPE DHT22
DHT dht(DHTPIN,DHTTYPE);

LiquidCrystal_I2C LCD = LiquidCrystal_I2C(0x27, 16, 2);

const int pwmChannel=0;
const int pwmFreq=5000;
const int pwmRes=8;

int ldrValue = 0;
int potValue = 0;
int brightness = 0;
int buttonState = 0;
int hazardState = 0;

unsigned long lastDhtRead=0;
const unsigned long DHT_INTERVAL=2000;

float lastTemp=0.0;
float lastHum=0.0;

void setup() {
  pinMode(headlightLED, OUTPUT);
  pinMode(leftIndLED, OUTPUT);
  pinMode(rightIndLED, OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(potPin, INPUT);
  pinMode(buttonPin, INPUT_PULLUP); 
  pinMode(hazardPin, INPUT_PULLUP); 
  Serial.begin(115200);

  ledcAttach(pwmChannel,pwmFreq,pwmRes);

  dht.begin();
  LCD.init();
  LCD.backlight();

  LCD.setCursor(0,0);
  LCD.print("Headlight System");
  LCD.setCursor(0,1);
  delay(1000);
  LCD.clear();
}
void loop() {
  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) {
    ledcWrite(pwmChannel,255);
    LCD.setCursor(0,0);
    LCD.print("Mode: MANUAL HIGH");
    analogWrite(headlightLED, 255); 
    Serial.println("Mode: MANUAL (High Beam)");
  } else {
    ldrValue = analogRead(ldrPin);    
    brightness = map(ldrValue, 32, 4063, 255, 10);
    brightness = constrain(brightness, 10, 255);
    ledcWrite(pwmChannel, brightness);

    LCD.setCursor(0, 0);
    LCD.print("Mode: AUTO        ");
    Serial.print("Mode: AUTO | LDR: ");
    Serial.print(ldrValue);
    Serial.print(" | Brightness: ");
    Serial.println(brightness);
  }

  hazardState = digitalRead(hazardPin);

  if (hazardState == HIGH) {
    digitalWrite(leftIndLED, HIGH);
    digitalWrite(rightIndLED, HIGH); 
    delay(200); 
    digitalWrite(leftIndLED, LOW);
    digitalWrite(rightIndLED, LOW);
    delay(200);
    LCD.setCursor(0,1);
    LCD.print("HAZARD ACTIVE   ");
    Serial.println("Warning! HAZARD");
  } else {
    potValue = analogRead(potPin);
    
    if (potValue < 1000) {
      digitalWrite(rightIndLED, LOW);
      digitalWrite(leftIndLED, HIGH);
      delay(300);
      digitalWrite(leftIndLED, LOW);
      delay(300);
      LCD.setCursor(0,1);
      LCD.print("Signal: LEFT    ");
      Serial.println("Signal: LEFT");
    } else if (potValue > 3000) {
      digitalWrite(leftIndLED, LOW);  
      digitalWrite(rightIndLED, HIGH);
      delay(300);
      digitalWrite(rightIndLED, LOW);
      delay(300);
      LCD.setCursor(0,1);
      LCD.print("Signal: RIGHT    ");
      Serial.println("Signal: RIGHT");
    }
    else {
      digitalWrite(leftIndLED, LOW);
      digitalWrite(rightIndLED, LOW);
      delay(50);
    }
  }
  unsigned long now=millis();
  if (now-lastDhtRead >= DHT_INTERVAL){
    lastDhtRead=now;
    float h=dht.readHumidity();
    float t=dht.readTemperature();

    if (!isnan(h)&&!isnan(t)){
      lastHum=h;
      lastTemp=t;
      Serial.print("DHT -> Temp: ");
      Serial.print(t);
      Serial.print(" *C  Hum: ");
      Serial.print(h);
      Serial.println(" %");
    } else {
      Serial.println("DHT read failed");
    }
    LCD.setCursor(0, 1);
    LCD.print("T:");
    LCD.print(lastTemp, 1);
    LCD.print((char)223); // degree symbol on many LCD fonts
    LCD.print("C ");
    LCD.print("H:");
    LCD.print(lastHum, 0);
    LCD.print("%   ");
    }
    delay(10);
  }

