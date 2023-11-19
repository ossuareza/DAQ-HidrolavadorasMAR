double v_pressure_1 = 0;
double v_pressure_2 = 0;

double measurements_counter = 1;

bool reading_roto = false;
bool reading_triplex = false;

void setup() {
  Serial.begin(115200);
  Serial.println("Arduino ready");
}

void loop() {



  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "R") {                   // Rotodinámicas
      reading_roto = true;
      reading_triplex = false;
    }
    else if (data == "T") {              //Triplex
      reading_triplex = true;
      reading_roto = false;
    }

    v_pressure_1 = v_pressure_1 / measurements_counter;
    v_pressure_2 = v_pressure_2 / measurements_counter;
    
    Serial.println(v_pressure_1);
    Serial.println(v_pressure_2);

    measurements_counter = 0;
    v_pressure_1 = 0;
    v_pressure_2 = 0;
  }

  if (reading_roto) {
    v_pressure_1 += analogRead(A0);
    v_pressure_2 += analogRead(A1);
    measurements_counter += 1;
  }
  else if (reading_triplex) {
    v_pressure_1 += analogRead(A2);
    v_pressure_2 += analogRead(A3);
    measurements_counter += 1;
  }

}

//    Serial.print("You sent me: ");
//    v_pressure_1 = analogRead(A0);
//    Serial.println(analogRead(A0) * 5.0 / 1023.0);
//    Serial.println(analogRead(A1) * 5.0 / 1023.0);
//    Serial.println(analogRead(A2) * 5.0 / 1023.0);
//    Serial.println(analogRead(A3) * 5.0 / 1023.0);
//    Serial.println("Siguiente");
//    Serial.println(v_pressure_2);
//    Serial.println(data);
//    delay(1000);
