#include <Servo.h>

Servo base, shoulder, elbow, gripper; //Objekte 

//definieren von pin
const int BASE_PIN = 8;
const int SHOULDER_PIN = 2;
const int ELBOW_PIN = 7;
const int GRIPPER_PIN = 4;

int pos[4] = {90, 90, 90, 30}; //Aktuelle Position
int posA[4], posB[4]; //Speicherplätze für a und b

void setup() { //Setup bei start von Programm aufgerufen
  Serial.begin(9600);
  base.attach(BASE_PIN); //Wichtig, weil arduino sonst keine signale senden kann
  shoulder.attach(SHOULDER_PIN);
  elbow.attach(ELBOW_PIN);
  gripper.attach(GRIPPER_PIN);
  moveTo(pos); //Startposition
  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); //auslesen Serial input wenn vorhanden, bis zeilenumbruch

    if (input.startsWith("MOVE")) {
      sscanf(input.c_str(), "MOVE %d %d %d %d", &pos[0], &pos[1], &pos[2], &pos[3]);
      moveTo(pos); //Bei eingabe von MOVE gefolgt von 4 Werte bewegt sich arm auf neue Position
    }
    else if (input.startsWith("SAVEA")) {
      memcpy(posA, pos, sizeof(pos));
      Serial.println("SAVED A"); //Bei eingabe von SAVEA wird aktuelle pos in posA gespeichert
    }
    else if (input.startsWith("SAVEB")) {
      memcpy(posB, pos, sizeof(pos));
      Serial.println("SAVED B"); // Selbes mit B
    }
    else if (input.startsWith("AUTO")) {
      runAuto(); //Startet Auto funktion. Automatisches Ablegen von a nach b
    }
  }
}

void moveTo(int p[4]) {
  base.write(p[0]);
  shoulder.write(p[1]);
  elbow.write(p[2]);
  gripper.write(p[3]);
} //bewegt auf gegebene Werte

void runAuto() {
  moveTo(posA); delay(500);
  gripper.write(90); delay(500);   // Greifen
  moveTo(posB); delay(500);
  gripper.write(30); delay(500);   // Ablegen
  moveTo(pos); // Zurück zur Startposition
}//Automatisches anfahren von a, greifen, fahren zu b, ablegen, zurückfahren zu start
