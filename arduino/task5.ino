/*
    The purpose of the program is to create a functionality using ARDUINO UNO R3 to check air temperature, humidity and lighting. 
    Depending on the values detected by the sensors, the program will inform the user by the brightness and colour of the diodes. 
    Also, if certain values are critical, the buzzer will turn on.
*/

#include <LiquidCrystal.h> //Header file for LCD from https://www.arduino.cc/EN/Reference/LiquidCrystal
#include <Keypad.h> //Header file for Keypad from https://github.com/Chris--A/Keypad
#include <SHT1X.h> //Header file for Humidity sensor from https://github.com/sparkfun/SHT15_Breakout/

// Defining the Keymap:
const byte KEYMAP_ROW_NUMBER = 4;
const byte KEYMAP_COL_NUMBER = 3;
char keys[KEYMAP_ROW_NUMBER][KEYMAP_COL_NUMBER] = {
    { '7', '8', '9' },
    { '4', '5', '6' },
    { '1', '2', '3' },
    { '*', '0', '#' }
};
byte keymapRowPins[KEYMAP_ROW_NUMBER] = { 0, 1, 2, 3 }; // Keymap ROW0, ROW1, ROW2 and ROW3 pins.
byte keymapColPins[KEYMAP_COL_NUMBER] = { 4, 5, 6 }; // Keymap COL0, COL1 and COL2 pins.
Keypad kpd = Keypad(makeKeymap(keys), keymapRowPins, keymapColPins, KEYMAP_ROW_NUMBER, KEYMAP_COL_NUMBER); //  Creating the Keypad
char key; // Keymap value

// Defining the LCD
const int RS = 8, EN = 9, D4 = 10, D5 = 11, D6 = 12, D7 = 13; //Pins to which the LCD is connected
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);

// Defining the humidity sensor
const int SENSOR_DATA = A5, SENSOR_SCK = A4; //Pins to which the humidity sensor is connected
SHT1x sht15(SENSOR_DATA, SENSOR_SCK); // Creating the humidity sensor
float tempC = 0, tempF = 0, humidity = 0; // Sensor values

// Defining the light sensor pin
const int LIGHT_SENSOR_PIN = A3;

// Defining the sounder pin
const int SOUNDER_PIN = 3;

// Defining the start button pin
const int START_BUTTON = 7;

// Defining the 8-Bit shift register
const int RCLK = A2, SER = A1, SRCLK = A0; //Pins to which the 8-Bit shift register is connected
const int registerPinNumber = 8; // 8-bit
boolean shiftRegisterData[registerPinNumber]; // Creating a register array

// Defining the led order
const int LED_RED = 0, LED_YELLOW = 1, LED_GREEN = 2, LED_BLUE = 4;

void setup()
{
    Serial.begin(9600);
    // Defining pins for the shift register
    pinMode(SER, OUTPUT);
    pinMode(RCLK, OUTPUT);
    pinMode(SRCLK, OUTPUT);
    ClearBuffer(); // Clearing the shift register buffer
    lcd.begin(16, 2); // Starting a LCD
    welcomeMessage(); // Displaying the welcome message
}

void loop()
{
    menuMessage(); // Displaying a menu message
    key = kpd.getKey(); // Storing pressed keypad key value in a char
    if (key != NO_KEY) {
        DetectButtons();
    }
}

void welcomeMessage()
{
    /*
    The function for displaying a welcome message on LCD.
    */
    lcd.print("Press a button"); //Display an intro message
    lcd.setCursor(0, 1); // Set the cursor to column 0, line 1
    lcd.print("to start"); //Display an intro message
    readStartButton();
}

void menuMessage()
{
    /*
    The function for displaying a menu on LCD.
    */
    lcd.clear();
    lcd.setCursor(0, 0); // Set the cursor to column 0, line 1
    lcd.print("Press 1-5 to"); //Display an intro message
    lcd.setCursor(0, 1); // Set the cursor to column 0, line 1
    lcd.print("display a metric"); //Display an intro message
    delay(100);
}

void readStartButton()
{
    /*
    The function that checks when the start button is pressed.
    */
    int buttonState = 0;
    while (buttonState != 1) {
        buttonState = digitalRead(START_BUTTON); // reading a start button
        delay(1);
    }
}
void readSH1XSensor()
{
    /*
    The function that reads the humidity sensor values: a temperature  *C, *F and a humidity.
    */
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Reading humidity");
    lcd.setCursor(0, 1);
    lcd.print("sensor value");
    // Read values from the sensor
    tempC = sht15.readTemperatureC();
    tempF = sht15.readTemperatureF();
    humidity = sht15.readHumidity();
    checkTemprature(tempC);
}

void checkTemprature(int tempC)
{
    /*
    The function that checks the temperature value and lights a led depends on it. 
    If the temperature value is critical, the buzzer is on.
    */
    if ((tempC > 0) && (tempC < 20)) {
        ledDigitalWrite(LED_YELLOW);
    }
    else {
        float volume = abs(tempC / 40);
        if (tempC > 20) {
            ledDigitalWrite(LED_GREEN);
        }
        else {
            ledDigitalWrite(LED_RED);
        }
        buzzerAnalogWrite(volume);
    }
}

void readLightSensor()
{
    /*
    The function that reads light sensor value and displaying if it is dark, dim, light, bright or very bright.
    It illuminates the blue led and its brightness depends on the lighting value. 
    */
    int analogValue = analogRead(LIGHT_SENSOR_PIN); // reading a sensor value
    lcd.clear(); // clearing a led
    lcd.setCursor(0, 0);
    lcd.print(String("Light sensor = ") + String(analogValue)); //
    Serial.print(analogValue); // displaying a read value
    lcd.setCursor(0, 1);
    if (analogValue < 10) {
        lcd.print(" - Dark");
    }
    else if (analogValue < 200) {
        lcd.print(" - Dim");
    }
    else if (analogValue < 500) {
        lcd.print(" - Light");
    }
    else if (analogValue < 800) {
        lcd.print(" - Bright");
    }
    else {
        lcd.print(" - Very bright");
    }
    ledAnalogWrite(LED_BLUE, analogValue / 1000); // illuminating the blue led
    delay(500);
}

void buzzerAnalogWrite(int volume)
{
    /*
    The function that turns on the buzzer at a certain volume.
    */
    shiftRegisterData[SOUNDER_PIN] = volume; // setting a certain value to the buzzer pin
    UpdateData(); // Updating shift registry data
    delay(300);
    ClearBuffer(); // clearing the shift registry
}
void DetectButtons()
{
    /*
    The function that displays a certain metric depends on the pressed key on keymap.
    */
    lcd.clear(); // Clearing a lcd
    lcd.setCursor(0, 0);
    switch (key) {
    case '1':
        readSH1XSensor(); // reading sh1x sensor
        lcd.print(key);
        lcd.setCursor(0, 1);
        lcd.print(String("Temp, *C:") + String(tempC)); // printing temperature in Celsius
        break;
    case '2':
        readSH1XSensor(); // reading sh1x sensor
        lcd.print(key);
        lcd.setCursor(0, 1);
        lcd.print(String("Temp, *F:") + tempF); // printing temperature in Fahrenheit
        break;
    case '3':
        readSH1XSensor(); // reading sh1x sensor
        lcd.print(key);
        lcd.setCursor(0, 1);
        lcd.print(String("Humidity:") + humidity); // printing humidity
        break;
    case '4':
        lcd.print(key);
        readLightSensor(); // printing humidity
        break;
    case '5':
        lcd.print(key);
        buzzerAnalogWrite(HIGH);  // checking the buzzer
        break;
    case '*':
        lcd.clear();
        break;
    }

    delay(200);
}

void ClearBuffer()
{
    /*
    The function that clear a shift registry buffer.
    */
    for (int i = registerPinNumber - 1; i >= 0; i--) {
        shiftRegisterData[i] = LOW;
    }
    UpdateData();
}

void UpdateData()
{
    /*
    The function that update shift registry buffer values.
    */
    digitalWrite(RCLK, LOW);
    for (int i = registerPinNumber - 1; i >= 0; i--) {
        digitalWrite(SRCLK, LOW); // stoping a shift-register clock
        digitalWrite(SER, shiftRegisterData[i]); // setting serial input pin to the buffer value
        digitalWrite(SRCLK, HIGH); // starting a shift-register clock
    }
    digitalWrite(RCLK, HIGH); // starting a storage-register clock
}

void ledDigitalWrite(int ledNumber)
{
    /*
    The function that lights up a led with the digital value.
    */
    shiftRegisterData[ledNumber] = HIGH;
    UpdateData(); // Updating shift registry data
    delay(300);
    ClearBuffer(); // clearing the shift registry
}

void ledAnalogWrite(int ledNumber, int value)
{
    /*
    The function that lights up a led with the analogue value.
    */
    shiftRegisterData[ledNumber] = value;
    UpdateData(); // Updating shift registry data
    delay(300);
    ClearBuffer(); // clearing the shift registry
}
