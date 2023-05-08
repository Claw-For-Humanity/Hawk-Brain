void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString();  // Read one byte from serial
    int data_int = data.toInt();
    Serial.write(data_int);
  }
}
