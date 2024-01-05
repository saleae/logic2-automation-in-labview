#include <SPI.h>

// Define pin connections
const int ssPin = 10; // SS (Slave Select) pin

void setup() {
  pinMode(ssPin, OUTPUT); // Set the SS pin as an output
  digitalWrite(ssPin, HIGH); // Set the SS pin to HIGH to disable the slave device
  Serial.begin(115200);     // Initialize serial communication at 115200 bps
  SPI.setClockDivider(SPI_CLOCK_DIV8);   
  SPI.begin();            // Initialize the SPI library

}

//MOSI 11
//MISO 12
//SPI Clock 13
//CS  10

void loop() {

 digitalWrite(ssPin, LOW); // Set the SS pin to LOW to enable the slave device
  // Loop to send data values from 0 to 128
  for (byte data_value = 0; data_value <= 128; data_value++) {

    //SPI.transfer(0x00);           // Send a write command (first bit indicates registry address 0x00)
    SPI.transfer(data_value);     // Send the actual data value


  }
  digitalWrite(ssPin, HIGH); // Set the SS pin to HIGH to disable the slave device

    delay(100); // Delay 100ms between sends

}
