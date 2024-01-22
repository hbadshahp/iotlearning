// ESP ultrasonic with MQTT
#include "SR04.h"
#include "PubSubClient.h"
#include "WiFi.h"

#define TRIG_PIN 2
#define ECHO_PIN 4
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a;

// WiFi
const char* ssid = "raspi-iiot";                
const char* wifi_password = "hussain2024";

// MQTT
const char* mqtt_server = "10.3.141.1"; 
const char* distance_topic = "distance";
const char* mqtt_username = "npdAtom"; // MQTT username
const char* mqtt_password = "npd@Atom"; // MQTT password
const char* clientID = "Distance_measurement"; // MQTT client ID

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;

// 1883 is the listener port for the Broker
PubSubClient client(mqtt_server, 1883, wifiClient);

// Custom function to connect to the MQTT broker via WiFi
void connect_MQTT(){
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection is confirmed
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging – Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed…");
  }
}

void setup() {
   Serial.begin(9600);
   delay(1000);
}

void loop() {
   connect_MQTT();
   Serial.setTimeout(2000);

   a=sr04.Distance()*10+30;

   Serial.print(a);
   Serial.println("mm");
   //delay(1000);

   // MQTT can only transmit strings
   String as="Hieght: "+String(a)+"mm";

    // PUBLISH to the MQTT Broker (topic = Temperature)
   if (client.publish(distance_topic, String(a).c_str())) {
    Serial.println("Distance sent!");
  }
   else {
    Serial.println("Distance failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10); // This delay ensures that client.publish doesn’t clash with the client.connect call
    client.publish(distance_topic, String(a).c_str());
  }


  client.disconnect();  // disconnect from the MQTT broker
  delay(1000*10);       // print new values after 1 Minute
}
