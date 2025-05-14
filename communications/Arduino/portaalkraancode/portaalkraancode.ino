// extra stappen voor YNeutral te bereiken.

#include "BITL.h"
#include <math.h>

BITL kraan("kraan", 9600);
String data = "";  // Variable to store received data
String lastData = "";

#define grabPin 2

#define inputPinX 13
#define enPinX 7
#define stepPinX 5
#define dirPinX 3

#define inputPinY 12
#define enPinY 10
#define stepPinY 6
#define dirPinY 11

#define motorDelay 750
#define stepPerDist 6400  // voor 360° draaien

#define diameterWheel 79.5
#define standardDist 85
#define nillDist 267.5

#define YNeutral 4
#define diameterSpool 14
#define heightContainer 42

#define YSteps 2000
#define YNeutralExtraSteps 500

#define grabPauzeMS 1000

int currentX = -2;
int currentY = 0;

int GoToX;
int GoToY;
int cordCount = 0;

int cordX1 = 1;
int cordY1 = 0;

int cordX2 = 2;
int cordY2 = 0;

bool grabber = false;
bool prevGrabberState = false;

enum leftRight { LEFT, RIGHT };
leftRight directionLR;

enum upDown { UP, DOWN };
upDown directionUD;

enum Steps { PUTDOWN, INTERMEDIATE, HORZ, LOAD, CHECK };
Steps stappenplan = CHECK;
Steps previousStappenplan = CHECK;

void setup() {
  Serial.begin(9600);

  pinMode(inputPinX, INPUT);
  pinMode(stepPinX, OUTPUT);
  pinMode(dirPinX, OUTPUT);
  pinMode(enPinX, OUTPUT);

  pinMode(inputPinY, INPUT);
  pinMode(stepPinY, OUTPUT);
  pinMode(dirPinY, OUTPUT);
  pinMode(enPinY, OUTPUT);

  digitalWrite(enPinX, LOW);
  digitalWrite(enPinY, LOW);
}

void loop() {
  stepByStep();
}

// stappenplan
// ---------------------------------------------------------------------------------------------

void stepByStep() {
  doWePauze();
  switch (stappenplan) {
    case INTERMEDIATE: moveYToIntermediate(); break;
    case HORZ: moveXToTarget(GoToX); break;
    case PUTDOWN: moveYToTarget(GoToY); break;
    case LOAD: makeGrabberGrab(); break;
    case CHECK: calcNextMove(); break;
  }
}

void doWePauze() {
  if (stappenplan != previousStappenplan) {
    Serial.println("! pauze !");
    delay(1000);
    previousStappenplan = stappenplan;
  }
}

void moveYToIntermediate() {
  if (currentY == YNeutral) {
    stappenplan = HORZ;
  } else {
    makeMotorYMove(false);  // false is naar boven want kan niet anders
  }
}

void moveXToTarget(int targetX) {
  if (currentX == targetX) {
    stappenplan = PUTDOWN;
  } else if (currentX < targetX) {
    makeMotorXMove(true);  // naar links
  } else {
    makeMotorXMove(false);  // naar rechts
  }
}

void moveYToTarget(int targetY) {
  if (currentY == targetY) {
    Serial.println("aangekomen!!!!!");
    stappenplan = LOAD;
    cordCount++;
    delay(200);
  } else {
    makeMotorYMove(true);  // naar beneden want kan niet anders
  }
}

void makeGrabberGrab() {
  if (cordCount == 2) {
    grabber = true;
  } else {
    grabber = false;
  }
  digitalWrite(grabPin, grabber);
  stappenplan = CHECK;
}

void calcNextMove() {
  switch (cordCount) {
    case 1:
      GoToX = cordX1;
      GoToY = cordY1;
      stappenplan = INTERMEDIATE;
      Serial.print("cordCount = ");
      Serial.println(cordCount);
      break;
    case 2:
      GoToX = cordX2;
      GoToY = cordY2;
      stappenplan = INTERMEDIATE;
      Serial.print("cordCount = ");
      Serial.println(cordCount);
      break;
    default:
      Serial.print("cordCount = ");
      Serial.println(cordCount);
      delay(500);
      Serial.println("stop");
      Serial.println("waiting for new cord");
      recieveCord();
      delay(500);
      cordCount = 1;
      break;
  }
}

// Om motor X te bewegen
// -------------------------------------------------------------------------------

void makeMotorXMove(bool leftRight) {
  directionLR = leftRight ? RIGHT : LEFT;
  digitalWrite(dirPinX, directionLR);
  setStepsX(calcDistanceX());
}

int calcDistanceX() {
  if (currentX == 0) return nillDist - standardDist;
  else return standardDist;
}

void setStepsX(int mmDistance) {
  unsigned long stappen = calcStappenX(mmDistance);
  if (digitalRead(inputPinX)) {
    Serial.println("High");
    digitalWrite(enPinX, LOW);
    motorX(stappen);
    updatePositionX();
  } else {
    Serial.println("low");
    digitalWrite(enPinX, HIGH);
  }
}

unsigned long calcStappenX(int mmDistance) {
  float omtrek = M_PI * diameterWheel;
  float Q = mmDistance / omtrek;
  float stappen = stepPerDist * Q;
  Serial.print("stappen = ");
  Serial.println(stappen);
  return round(stappen);
}

void motorX(unsigned long steps) {
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(motorDelay);
    digitalWrite(stepPinX, LOW);
    delayMicroseconds(motorDelay);
  }
}

void updatePositionX() {
  switch (directionLR) {
    case RIGHT: currentX++; break;
    case LEFT: currentX--; break;
  }
  Serial.print("X = ");
  Serial.println(currentX);
}

// om motor Y te bewegen
// --------------------------------------------------------------------------------------------------

void makeMotorYMove(bool upDown) {
  directionUD = upDown ? DOWN : UP;
  digitalWrite(dirPinY, !directionUD);
  setStepsY(heightContainer);
}

void setStepsY(int mmDistance) {
  unsigned long stappen = calcStappenY(mmDistance);
  if (digitalRead(inputPinY)) {
    Serial.println("High");
    digitalWrite(enPinY, LOW);
    motorY(stappen);
    updatePositionY();
  } else {
    Serial.println("low");
    digitalWrite(enPinY, HIGH);
  }
}

unsigned long calcStappenY(int mmDistance) {
  float omtrek = M_PI * diameterSpool;
  float Q = mmDistance / omtrek;
  float stappen = stepPerDist * Q;
  Serial.print("stappen = ");
  Serial.println(stappen);
  return round(stappen);
}

void motorY(unsigned long steps) {
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepPinY, HIGH);
    delayMicroseconds(motorDelay);
    digitalWrite(stepPinY, LOW);
    delayMicroseconds(motorDelay);
  }
}

void updatePositionY() {
  switch (directionUD) {
    case UP: currentY++; break;
    case DOWN: currentY--; break;
  }
  Serial.print("Y = ");
  Serial.println(currentY);
}

// alles met de grijper
// ------------------------------------------------------------------------------------------------------------------

void grabDelay() {
  if (grabber != prevGrabberState) {
    Serial.println("grabbing");
    delay(grabPauzeMS);
    prevGrabberState = grabber;
  }
}

// communicatie
// ---------------------------------------------------------------------------------------------------------------

void recieveCord() {
  String newData = kraan.receive();
  Serial.println('Reading Data');
  if (newData != "" && newData != lastData) {
    data = newData;
    editdata();
    lastData = newData;
  }
}

void editdata() {
  int a, b, c, d;

  // Replace commas with spaces in case comma-separated input is used
  data.trim();  // Remove whitespace, newline

  if (sscanf(data.c_str(), "%d %d %d %d", &a, &b, &c, &d) == 4) {
    cordX1 = a;
    cordY1 = b;
    cordX2 = c;
    cordY2 = d;
  } else {
    Serial.println("Parsing failed — invalid input format:");
    Serial.println(data);
  }
  debugRecievedData(data);
}


void debugRecievedData(String debugData) {
  Serial.println("check recieved data");
  Serial.println();
  Serial.println(data);
  Serial.println(cordX1);
  Serial.println(cordY1);
  Serial.println(cordX2);
  Serial.println(cordY2);
}
