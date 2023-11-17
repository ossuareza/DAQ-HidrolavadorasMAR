double v_pressure_1 = -1;
double v_pressure_2 = -1;

void setup() {
  Serial.begin(115200);
}

void loop() {

  v_pressure_1 = -1;
  v_pressure_2 = -1;

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "R") {                   // Rotodinámicas
      v_pressure_1 = 1; //analogRead(A0);
      v_pressure_2 = 2; //analogRead(A1);
    }
    else if (data == "T"){               //Triplex
      v_pressure_1 = analogRead(A2);
      v_pressure_2 = analogRead(A3);
    }
  
//    Serial.print("You sent me: ");
    Serial.println(v_pressure_1);
    Serial.println(v_pressure_2);
//    Serial.println(data);
//    delay(1000);
  }
  
}
