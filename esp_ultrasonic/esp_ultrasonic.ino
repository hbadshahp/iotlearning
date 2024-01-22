// Esp32 code

#include "SR04.h"
#define TRIG_PIN 2
#define ECHO_PIN 4
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a;

void setup() {
   Serial.begin(9600);
   delay(1000);
}

void loop() {
   a=sr04.Distance()*10+30;
   Serial.print(a);
   Serial.println("mm");
   delay(1000);
}

