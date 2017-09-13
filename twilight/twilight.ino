
/*
  Required Connections    http://www.pjrc.com/store/octo28_adaptor.html
  --------------------
    pin 2:  LED Strip #1    OctoWS2811 drives 8 LED Strips.
    pin 14: LED strip #2    All 8 are the same length.
    pin 7:  LED strip #3
    pin 8:  LED strip #4    A 100 ohm resistor should used
    pin 6:  LED strip #5    between each Teensy pin and the
    pin 20: LED strip #6    wire to the LED strip, to minimize
    pin 21: LED strip #7    high frequency ringining & noise.
    pin 5:  LED strip #8
    pin 15 & 16 - Connect together, but do not use
    pin 4 - Do not use
    pin 3 - Do not use as PWM.  Normal use is ok.
*/

#include <OctoWS2811.h>

// octo ws library assumes a NxN grid but we will only be using the first row!
const int ledsPerStrip = 100;

DMAMEM int displayMemory[ledsPerStrip*6];
int drawingMemory[ledsPerStrip*6];

const int config = WS2811_GRB | WS2811_800kHz;

OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);

void setup() {
  Serial.begin(115200);
  leds.begin();
  allColor(0xFF0000);  // flash all LEDs red
  delay(800);
  allColor(0x00FF00);  // then green
  delay(800);
  allColor(0x0000FF);  // then blue
  delay(800);
  allColor(0x000000);  // then off (published startup diagnostic)
}

void allColor(unsigned int c) {
  for (int i=0; i < ledsPerStrip; i++) {
    leds.setPixel(i, c);
  }
  leds.show();
}


//reads up to maxlen into line, returns number of characters read or -1 if none
int getline(char line*, int maxlength)
{
  int i=-1;
  for (i=0; i<maxlength; ++i) {
    char c = Serial.read();
    if (c=='\n'){
      break;
    }
    line[i]=c;
  }
  return i;
}

void loop() {
  // put your main code here, to run repeatedly:

}
