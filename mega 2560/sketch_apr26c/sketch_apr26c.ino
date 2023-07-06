#include <SoftwareSerial.h>
#include <Servo.h>
#include <math.h>

Servo base;
Servo shoulder;
Servo wrist;

float L1 = 6.5;
float L2 = 11.5;
float L3 = 8.5;

bool firstTheta1Received = false;  // Flag to track the first theta1 received

void setup() {
  Serial.begin(115200);
  Serial3.begin(115200);

  base.attach(5);       // theta1
  shoulder.attach(6);   // theta2
  wrist.attach(7);      // theta3

  shoulder.write(130);  
  base.write(0);
  wrist.write(0);

}

void loop() {

  if (Serial3.available()) {
    int z_coor = 0;

    int x_coor = Serial3.parseInt();
    Serial.print("Received X: ");
    Serial.println(x_coor);

    int y_coor = Serial3.parseInt();
    Serial.print("Received y: ");
    Serial.println(y_coor);

    if (x_coor != 0 && x_coor != 2 && x_coor != -2 && x_coor != 4 && x_coor != 10 && x_coor != 15 && x_coor != 22 && x_coor != 29 && x_coor != 168 && x_coor != 109 && x_coor != 190 && x_coor != 192 && y_coor != 0 && y_coor != -2 && y_coor != 2 && y_coor != 4 && y_coor != 8 && y_coor != 10 && y_coor != 22 && y_coor != 168 && y_coor != 190 && y_coor != 192) {

      float theta1_rad = atan2(static_cast<float>(y_coor), static_cast<float>(x_coor));
      float theta1 = degrees(theta1_rad) / 0.8;

      float r = sqrt(pow(static_cast<float>(x_coor), 2) + pow(static_cast<float>(y_coor), 2));
      float k = sqrt(pow(L1, 2) + pow(r, 2));  // Pz=0-L1

      float numerator1 = pow(k, 2) - pow(L2, 2) - pow(L3, 2);
      float denominator1 = 2 * L2 * L3;

      float theta3_rad = acos(numerator1 / denominator1);
      float theta3 = degrees(theta3_rad);

      float numerator2 = L3 * sin(theta3_rad);
      float denominator2 = L2 + (L3 * cos(theta3_rad));
      float alpha = atan2(numerator2, denominator2);
      float beta = atan2(L1, r);

      float theta2_rad = (beta - alpha);
      float theta2 = degrees(theta2_rad);

      Serial.print("theta 1: ");
      Serial.println(theta1);

      delay(2000);
      base.write(theta1); 
      delay(1000);

      if (!firstTheta1Received) {
      shoulder.write(27);
      delay(1000);
      firstTheta1Received = true;  // Set the flag to true after the first theta1 is received
      }

    }

  } else {
    // No more theta1 values to be received, return to 130 degrees
    shoulder.write(130);
    delay(1000);
    
    firstTheta1Received = false;  // Reset the flag for the next set of theta1 values
  }
}
