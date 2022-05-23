#include <DHT.h>

// číslo pinu Arduina, kam je připojený DATA pin senzoru DHT
#define DHTPIN 2
#define DHTTYPE DHT11
// do proměné dht uložíme údaje o již nadefinovaném senzoru 
DHT dht(DHTPIN, DHTTYPE); 

// vytvoříme proměnou pro vlhkost (humidity)
float hum;
// vytvoříme proměnou pro teplotu (temperature)
float temp;  
                                
void setup()
{
  // zapneme sériovou linku a určíme rychlost 9600 baudů
  Serial.begin(9600);  
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT); 
  pinMode(5, OUTPUT); 
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);  
  // aktivujeme komunikaci senzoru DHT                      
  dht.begin();                                
}

void loop()
{
  // načteme informaci (vlhkost) z čidla a uložíme jí do proměné hum  
  hum = dht.readHumidity();  
  // načteme informaci (teplota) z čidla a uložíme jí do proměné temp
  temp = dht.readTemperature();   

  // vypíšeme informace po sériové lince
//  Serial.print("Vlhkost: ");                
//  Serial.print(hum);
//  Serial.print(" %, Teplota: ");
//  Serial.print(temp);
//  Serial.println(" Celsius");

  String humidity = String(hum);
  String temperature = String(temp);
  String values = String(humidity + "," + temperature);

  Serial.println(values);
    
  if(hum <= 19.99)
  {
    digitalWrite(7, HIGH);
    digitalWrite(6, LOW);
    digitalWrite(5, LOW);
    digitalWrite(4, LOW);
    digitalWrite(3, LOW);
  }
  else if(hum >= 20.00 && hum <= 39.99)
  {
    digitalWrite(7, HIGH);
    digitalWrite(6, HIGH);
    digitalWrite(5, LOW);
    digitalWrite(4, LOW);
    digitalWrite(3, LOW);
  }
  else if(hum >= 40.00 && hum <= 59.99)
  {
    digitalWrite(7, HIGH);
    digitalWrite(6, HIGH);
    digitalWrite(5, HIGH);
    digitalWrite(4, LOW);
    digitalWrite(3, LOW);
  }
  else if(hum >= 60.00 && hum <= 79.99)
  {
    digitalWrite(7, HIGH);
    digitalWrite(6, HIGH);
    digitalWrite(5, HIGH);
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
  }
  else
  {
    digitalWrite(7, HIGH);
    digitalWrite(6, HIGH);
    digitalWrite(5, HIGH);
    digitalWrite(4, HIGH);
    digitalWrite(3, HIGH);
  }
  
  delay(3000);                              
}
