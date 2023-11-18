double v_pressure_1 = -1;
double v_pressure_2 = -1;

void setup() {
  Serial.begin(115200);
}

void loop() {

  v_pressure_1 = -1;
  v_pressure_2 = -1;
//Serial.available() > 0
  if (true) {
    String data = Serial.readStringUntil('\n');
    if (data == "R") {                   // Rotodinámicas
      v_pressure_1 = analogRead(A0);
      v_pressure_2 = analogRead(A3);
    }
    else if (data == "T"){               //Triplex
      v_pressure_1 = analogRead(A6);
      v_pressure_2 = analogRead(A9);
    }
  
//    Serial.print("You sent me: ");
    v_pressure_1 = analogRead(A0);
    Serial.println(v_pressure_1);
//    Serial.println(v_pressure_2);
//    Serial.println(data);
//    delay(1000);
  }
  
}
