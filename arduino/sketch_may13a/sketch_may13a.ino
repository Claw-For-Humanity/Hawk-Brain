int x;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  while(!Serial.available());
  x = Serial.readString().toInt();
  switch (x){
    case 1:
    {
      Serial.print('one');
      }
    case 2:
    {
      Serial.print('two');
    }
    case 3:
    {
      Serial.print('three');
    }
    default:
    {
      Serial.print('Other than 3');
    }

  }
}
