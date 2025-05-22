#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define TRIG_PIN 9
#define ECHO_PIN 8
#define LDR_PIN 7

DHT dht(DHTPIN, DHTTYPE);
RTC_DS3231 rtc;
LiquidCrystal_I2C lcd(0x27, 16, 2);

bool displayOn = false;
unsigned long lastUpdate = 0;
unsigned long lastDHTRead = 0;
float temperature = 0.0;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  lcd.init();
  lcd.backlight();  // Keep backlight always ON

  dht.begin();
  rtc.begin();
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);

  lcd.clear();
  lcd.setCursor(0, 0); 
  lcd.print("Initializing...");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Ultrasonic distance reading
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;

  // Read light level from LDR
  bool isHighLight = (digitalRead(LDR_PIN) == HIGH);

  if (!isHighLight) {
    // In low light, always keep display ON
    if (!displayOn) {
      lcd.display();
      displayOn = true;
      lcd.clear();
    }
  } else {
    // In high light, control with ultrasonic
    if (distance < 15) {
      if (!displayOn) {
        lcd.display();
        displayOn = true;
        lcd.clear();
      }
    } else {
      if (displayOn) {
        lcd.noDisplay();
        displayOn = false;
      }
    }
  }

  // Read temperature every 2 seconds
  if (millis() - lastDHTRead > 2000) {
    lastDHTRead = millis();
    float temp = dht.readTemperature();
    if (!isnan(temp)) {
      temperature = temp;
    } else {
      Serial.println("Failed to read from DHT!");
    }
  }

  // Update LCD every 1 second
  if (millis() - lastUpdate >= 1000) {
    lastUpdate = millis();

    DateTime now = rtc.now();

    // Time and Light
    lcd.setCursor(0, 0);
    if (now.hour() < 10) lcd.print("0"); lcd.print(now.hour()); lcd.print(":");
    if (now.minute() < 10) lcd.print("0"); lcd.print(now.minute()); lcd.print(":");
    if (now.second() < 10) lcd.print("0"); lcd.print(now.second());

    lcd.setCursor(11, 0);
    lcd.print(isHighLight ? "HIGH" : "LOW ");

    // Date and Temp
    lcd.setCursor(0, 1);
    if (now.day() < 10) lcd.print("0"); lcd.print(now.day()); lcd.print("/");
    if (now.month() < 10) lcd.print("0"); lcd.print(now.month()); lcd.print("/");
    lcd.print(now.year());

    lcd.setCursor(10, 1);
    lcd.print(" ");
    lcd.print(temperature, 1);
    lcd.print((char)223);
    lcd.print("C ");
  }
}
