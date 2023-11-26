#include<ESP8266WiFi.h>
int port=5055;
int fireval=0;
WiFiServer server(port);
const char *ssid="santhoshesp";
const char *password="hello123";
void setup(){
  pinMode(LED_BUILTIN,OUTPUT);
  Serial.begin(9600);
  Serial.println();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid,password);
  Serial.println("connecting to wifi");
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
    delay(500);
  }
  Serial.println("");
  Serial.print("connected to ");
  Serial.println(ssid);
  Serial.print("IP address:");
  Serial.println(WiFi.localIP());
  server.begin();
  Serial.print("open telnet and connect to IP");
  Serial.print(WiFi.localIP());
  Serial.print(" on port ");
  Serial.println(port);
}

void loop(){
  WiFiClient client=server.available();
  if(client){
    if(client.connected()){
      Serial.println("client connected");
    }
    while(client.connected()){
      while(client.available()>0){
        fireval =int(client.read());
        while(1){
          if(fireval==0){
            digitalWrite(LED_BUILTIN,LOW);
          }else{
            digitalWrite(LED_BUILTIN,HIGH);
          }
        }
      }
      while(Serial.available()>0){
        client.write(Serial.read());
      }
    }
    client.stop();
    Serial.println("client disconnected");
  }
}