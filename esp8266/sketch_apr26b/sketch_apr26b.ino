#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

WiFiServer server(80);

const char* ssid = "IBudget-2.4G@unifi";
const char* password = "ibudget_366";

// const char* ssid = "Redmi Note 10";
// const char* password = "amanite1005";

const int MAX_COORDINATES = 15;

struct Coordinate {
  int x;
  int y;
};

Coordinate coordinates[MAX_COORDINATES];
int coordinateCount = 0;
bool firstPairReceived = false; // Flag to track the first pair
bool firstPairPrinted = false; // Flag to track if the first pair has been printed

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  
  server.begin();
  connectToWifi();
}

void connectToWifi() {
  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);
  
  WiFi.begin(ssid, password);
  Serial.println();
  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");
    while (client.connected()) {
      if (client.available()) {
        String data = client.readStringUntil('\n');
        Serial.println(data);

        // Split the received string into substrings using the comma as the delimiter
        int firstCommaIndex = data.indexOf(',');
        int secondCommaIndex = data.indexOf(',', firstCommaIndex + 1);
        if (firstCommaIndex != -1 && secondCommaIndex != -1){
          String X_str = data.substring(firstCommaIndex + 1, secondCommaIndex);
          String Y_str = data.substring(secondCommaIndex + 1);

          if (X_str.toInt() != 0 && Y_str.toInt() != 0) {
            int X = X_str.toInt();
            int Y = Y_str.toInt();
        
            // Send the integers over serial communication
            Serial.print("X: ");
            Serial.println(X);
            Serial.flush();
            delay(200);

            Serial.print("Y: ");
            Serial.println(Y);
            Serial.flush();
            delay(200);
          }
        }

      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }

  delay(1000);
}
