///////////////////////////////////////////////////////////
//   CLAW FOR HUMANITY v2.2, THSS Robotics Team © 2023   //
///////////////////////////////////////////////////////////
//                       Commands:                       //
// 1,2 - ON, OFF Solenoid #1 | 3,4 - ON, OFF Solenoid #2 //
// 5,6 - ON, OFF Solenoid #3 | 7,8 - ON, OFF Solenoid #4 //
//          9,10 - ON, OFF The Master Solenoid           //
//               11,12 - ON, OFF The Drive               //
//                  13 - EMERGENCY STOP                  //
//                 14 - System SELF-TEST                 //
//                  15 - All pistons OFF                 //
//                  16 - All pistons ON                  //
///////////////////////////////////////////////////////////

#define drve 2
#define mstr 3
#define cyl4 4
#define cyl3 5
#define cyl2 6
#define cyl1 7
#define buzz 8

String str;

void setup() {
  pinMode(cyl1, OUTPUT);
  pinMode(cyl2, OUTPUT);
  pinMode(cyl3, OUTPUT);
  pinMode(cyl4, OUTPUT);
  pinMode(mstr, OUTPUT);
  pinMode(drve, OUTPUT);
  pinMode(buzz, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(10);
  Serial.println("*** Ready to receive ***");

  digitalWrite(cyl1, LOW);
  digitalWrite(cyl2, LOW);
  digitalWrite(cyl3, LOW);
  digitalWrite(cyl4, LOW);
  digitalWrite(mstr, LOW);
  digitalWrite(drve, HIGH);

  tone(8, 400);
  delay(150);
  noTone(8);
  delay(90);

  tone(8, 400);
  delay(150);  // включаем на пьезодинамик 600 Гц
  noTone(8);   // отключаем пьезодинамик на пин 11
  delay(40);   // ждем 1 секунду

  tone(8, 600);
  delay(255);
  noTone(8);
  delay(2000);
}


void loop() {

  if (Serial.available() > 0) {

    str = Serial.readString();
    Serial.println(str);
    str.trim();

    /////////////////////////////////////////
    if (str == "1") {
      digitalWrite(cyl1, HIGH);
      Serial.println("* Turning on Solenoid #1 *");
      select();
    }  //Solenoid #1
    if (str == "2") {
      digitalWrite(cyl1, LOW);
      Serial.println("* Turning off Solenoid #1 *");
      select();
    }
    /////////////////////////////////////////
    if (str == "3") {
      digitalWrite(cyl2, HIGH);
      Serial.println("* Turning on Solenoid #2 *");
      select();
    }  //Solenoid #2
    if (str == "4") {
      digitalWrite(cyl2, LOW);
      Serial.println("* Turning off Solenoid #2 *");
      select();
    }
    /////////////////////////////////////////
    if (str == "5") {
      digitalWrite(cyl3, HIGH);
      Serial.println("* Turning on Solenoid #3 *");
      select();
    }  //Solenoid #3
    if (str == "6") {
      digitalWrite(cyl3, LOW);
      Serial.println("* Turning off Solenoid #3 *");
      select();
    }
    /////////////////////////////////////////
    if (str == "7") {
      digitalWrite(cyl4, HIGH);
      Serial.println("* Turning on Solenoid #4 *");
      select();
    }  //Solenoid #4
    if (str == "8") {
      digitalWrite(cyl4, LOW);
      Serial.println("* Turning off Solenoid #4 *");
      select();
    }
    /////////////////////////////////////////
    if (str == "9") {
      digitalWrite(mstr, HIGH);
      Serial.println("* Turning on the Master Solenoid *");
      select();
    }  //Master Solenoid
    if (str == "10") {
      digitalWrite(mstr, LOW);
      Serial.println("* Turning off the Master Solenoid *");
      select();
    }
    /////////////////////////////////////////
    if (str == "11") {
      digitalWrite(drve, LOW);
      Serial.println("* Turning on the Drive *");
      select();
    }  //Drive
    if (str == "12") {
      digitalWrite(drve, HIGH);
      Serial.println("* Turning off the Drive *");
      select();
    }
    /////////////////////////////////////////
    //EMERGENCY STOP
    if (str == "13") {
      digitalWrite(mstr, LOW);
      digitalWrite(drve, HIGH);
      emerStop();
      Serial.println("** EMERGENCY STOP ** Turning off the Master Solenoid & Drive");
    }
    /////////////////////////////////////////
    if (str == "14") {  //SYSTEM SELF_TEST
      selfTest();
    }
    /////////////////////////////////////////
    if (str == "15") {  //ALL PISTONS OFF
      digitalWrite(cyl1, LOW);
      digitalWrite(cyl2, LOW);
      digitalWrite(cyl3, LOW);
      digitalWrite(cyl4, LOW);
      select();
      Serial.println("** All Pistons OFF **");
    }
    /////////////////////////////////////////
    if (str == "16") {  //ALL PISTONS ON
      digitalWrite(cyl1, HIGH);
      digitalWrite(cyl2, HIGH);
      digitalWrite(cyl3, HIGH);
      digitalWrite(cyl4, HIGH);
      select();
      Serial.println("** All Pistons ON **");
    }
  }
}

void select() {
  tone(8, 600);
  delay(100);  // включаем на пьезодинамик 600 Гц
  noTone(8);
}

void emerStop() {
  tone(8, 600);
  delay(1000);  
  noTone(8);
  delay(1000);
  tone(8, 600);
  delay(1000);  
  noTone(8);
  delay(1000);
  tone(8, 600);
  delay(1000);  
  noTone(8);
  delay(1000);
}

void selfTest() {
  Serial.println("** SELF_TEST ** Starting the system Self-Test...");

  tone(8, 600);
  delay(1000);  
  noTone(8);
  delay(1000);

  Serial.println("** SELF_TEST ** Turning off all Solenoids, Drive, Master Solenoid...");
  digitalWrite(cyl1, LOW);
  digitalWrite(cyl2, LOW);
  digitalWrite(cyl3, LOW);
  digitalWrite(cyl4, LOW);
  digitalWrite(mstr, LOW);
  digitalWrite(drve, HIGH);

  tone(8, 600);
  delay(1000);  
  noTone(8);
  delay(1000);
  
  Serial.println("** SELF_TEST ** Checking Solenoids...");
  delay(2000);
  digitalWrite(cyl1, HIGH);
  delay(1500);
  digitalWrite(cyl1, LOW);
  delay(2000);
  digitalWrite(cyl2, HIGH);
  delay(1500);
  digitalWrite(cyl2, LOW);
  delay(2000);
  digitalWrite(cyl3, HIGH);
  delay(1500);
  digitalWrite(cyl3, LOW);
  delay(2000);
  digitalWrite(cyl4, HIGH);
  delay(1500);
  digitalWrite(cyl4, LOW);

  delay(3000);
  Serial.println("** SELF_TEST ** Checking the Master Solenoid...");
  delay(2000);
  digitalWrite(mstr, HIGH);
  delay(1000);
  digitalWrite(mstr, LOW);

  delay(3000);
  Serial.println("** SELF_TEST ** Checking the Drive...");
  delay(2000);
  digitalWrite(drve, LOW);
  delay(5000);
  digitalWrite(drve, HIGH);

  tone(8, 600);
  delay(2000);
  noTone(8);
  Serial.println("** SELF_TEST ** System Self-Test completed!");
  setup();
}