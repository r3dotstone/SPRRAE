#include <ME480FSM.h> //include ME480 FSM Timer Counter library
// Include the Wire library for I2C
#include <Wire.h>

// LED on pin 13
const int ledPin = 13;
const int calpin = 40;

FSMEncoder1 encode1;

int phasepin = 8;
int enable = 9;
bool phase; //false = cw true = ccw
int counts;
int setspeed, direct, out;
float pos, t, t_old, pos_old, omega, dp, dt, goal;
float goal_new, goal_old;
bool cal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  phase = true;
  direct = 1;
  Wire.begin(0x8);

  // Call receiveEvent when data received
  Wire.onReceive(receiveEvent);

  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  goal_old = 0;
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    digitalWrite(ledPin, c);
    out = c;
  }
}

void loop() {
  cal = true;
  counts = encode1.getCounts();
  pos = 2 * PI * counts / 12000;
  goal_new = 2 * PI * out / 360;
  t = micros();
  cal = true;

  if (cal == true) {
    if (goal_new > 0) {
      direct = 1;
      phase = true;
    } else if (goal_new < 0) {
      direct = -1;
      phase = false;
    }
    digitalWrite(phasepin, phase);
    if (((pos < goal_new) && (direct == 1)) || ((pos > goal_new) && (direct == -1))) {
      if (abs(pos - goal_new) > 0.75) {
        analogWrite(enable, 120);
      } else {
        analogWrite(enable, 90);
      }
    } else {
      out = 0;
      counts = encode1.getCountsAndReset();
      analogWrite(enable, 0);
      delay(100);
    }
  }



  if (cal == false) {
    if (goal_new > goal_old) {
      direct = 1;
      phase = true;
    } else if (goal_new < goal_old) {
      direct = -1;
      phase = false;
    }
    digitalWrite(phasepin, phase);
    if (((pos < goal_new) && (direct == 1)) || ((pos > goal_new) && (direct == -1))) {
      if (abs(pos - goal_new) > 0.75) {
        analogWrite(enable, 120);
      } else {
        analogWrite(enable, 90);
      }
    } else {
      analogWrite(enable, 0);
      goal_old = goal_new;
      delay(100);
    }
  }

  delay(50);

  dp = (pos - pos_old);
  dt = (t - t_old) / 1000000.0;

  omega =  dp / dt;
  pos_old = pos;
  t_old = t;


  Serial.print(pos);
  Serial.print('\t');
  Serial.print(goal_new);
  Serial.print('\t');
  Serial.print(direct);
  Serial.print('\t');
  Serial.println(out);
}






//#include <ME480FSM.h> //include ME480 FSM Timer Counter library
//// Include the Wire library for I2C
//#include <Wire.h>
//
//// LED on pin 13
//const int ledPin = 13;
//const int calpin = 40;
//
//FSMEncoder1 encode1;
//
//int phasepin = 8;
//int enable = 9;
//bool phase; //false = cw true = ccw
//int counts;
//int setspeed, direct, out;
//float pos, t, t_old, pos_old, omega, dp, dt, goal;
//float goal_new, goal_old;
//bool cal;
//
//void setup() {
//  // put your setup code here, to run once:
//  Serial.begin(9600);
//  phase = true;
//  direct = 1;
//  Wire.begin(0x8);
//
//  // Call receiveEvent when data received
//  Wire.onReceive(receiveEvent);
//
//  // Setup pin 13 as output and turn LED off
//  pinMode(ledPin, OUTPUT);
//  digitalWrite(ledPin, LOW);
//  goal_old = 0;
//}
//
//// Function that executes whenever data is received from master
//void receiveEvent(int howMany) {
//  while (Wire.available()) { // loop through all but the last
//    char c = Wire.read(); // receive byte as a character
//    digitalWrite(ledPin, c);
//    out = c;
//  }
//}
//
//void loop() {
//  cal = digitalRead(calpin);
//  counts = encode1.getCounts();
//  pos = 2 * PI * counts / 12000;
//  goal_new = 2 * PI * out / 360;
//  t = micros();
//
//  if (cal == true) {
//    if (goal_new > 0) {
//      direct = 1;
//      phase = true;
//    } else if (goal_new < 0) {
//      direct = -1;
//      phase = false;
//    }
//    digitalWrite(phasepin, phase);
//    if (((pos < goal_new) && (direct == 1)) || ((pos > goal_new) && (direct == -1))) {
//      if (abs(pos - goal_new) > 0.75) {
//        analogWrite(enable, 120);
//      } else {
//        analogWrite(enable, 60);
//      }
//    } else {
//      out = 0;
//      counts = encode1.getCountsAndReset();
//      analogWrite(enable, 0);
//      delay(100);
//    }
//  }
//
//
//
//  if (cal == false) {
//    if (goal_new > goal_old) {
//      direct = 1;
//      phase = true;
//    } else if (goal_new < goal_old) {
//      direct = -1;
//      phase = false;
//    }
//    digitalWrite(phasepin, phase);
//    if (((pos < goal_new) && (direct == 1)) || ((pos > goal_new) && (direct == -1))) {
//      if (abs(pos - goal_new) > 0.75) {
//        analogWrite(enable, 120);
//      } else {
//        analogWrite(enable, 60);
//      }
//    } else {
//      analogWrite(enable, 0);
//      goal_old = goal_new;
//      delay(100);
//    }
//  }
//
//  delay(50);
//
//  dp = (pos - pos_old);
//  dt = (t - t_old) / 1000000.0;
//
//  omega =  dp / dt;
//  pos_old = pos;
//  t_old = t;
//
//
//  Serial.print(pos);
//  Serial.print('\t');
//  Serial.print(goal_new);
//  Serial.print('\t');
//  Serial.print(direct);
//  Serial.print('\t');
//  Serial.println(out);
//}
