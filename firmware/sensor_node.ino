// ESP32 + DHT22 + soil moisture -> kirim JSON ke gateway via HTTP
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 4
#define SOILPIN 34
DHT dht(DHTPIN, DHT22);

const char* WIFI_SSID = "SSID_KAMU";
const char* WIFI_PASS = "PASSWORD_KAMU";
const char* GATEWAY   = "http://192.168.1.10:5000/ingest";
const char* NODE_ID   = "node-01";   // pseudonym, bukan nama lokasi/orang

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  int soil = analogRead(SOILPIN);
  if (!isnan(t) && !isnan(h)) {
    String body = "{\"node\":\"" + String(NODE_ID) + "\",\"temp\":" + t +
                  ",\"hum\":" + h + ",\"soil\":" + soil + "}";
    HTTPClient http;
    http.begin(GATEWAY);
    http.addHeader("Content-Type", "application/json");
    http.POST(body);
    http.end();
  }
  delay(60000); // 1 menit
}
