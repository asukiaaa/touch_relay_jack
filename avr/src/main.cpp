#include <Arduino.h>
#define RELAY 4
#define TOUCH_IN 8
#define TOUCH_OUT 9
#define TOUCH_THRESHOLD 1

void setup() {
  pinMode(RELAY, OUTPUT);
  pinMode(TOUCH_IN, INPUT);
  pinMode(TOUCH_OUT, OUTPUT);
  // Serial.begin(115200);
}

int count;

void loop() {
  count = 0;
  digitalWrite(TOUCH_OUT, HIGH);
  while(digitalRead(TOUCH_IN) == LOW) ++ count;
  digitalWrite(TOUCH_OUT, LOW);
  delay(100);
  // if (count != 0) Serial.println(count);
  digitalWrite(RELAY, count >= TOUCH_THRESHOLD);
}

