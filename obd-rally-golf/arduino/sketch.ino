#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int counter = 0;  // Counter to track button presses
unsigned long lastUpdate = 0;  // Timestamp of the last counter update
const long debounceTime = 500;  // Debounce time in milliseconds
int lastCounter = 0;  // Keep track of the last counter to update LCD only on change

bool prevPressed = false;
bool nextPressed = false;

String displayName;  // Variable to store the name displayed on the LCD

void setup() {
  lcd.begin(16, 2);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(13, OUTPUT);

  Serial.begin(9600); // Start serial communication at 9600 baud rate
  lcd.clear();
  lcd.print("RaceMonitorXPro");
}

void loop() {
  int isPrevPressed = analogRead(A0) == 1023; // Check if the "PREV" button is pressed
  int isNextPressed = analogRead(A1) == 1023; // Check if the "NEXT" button is pressed

  unsigned long currentTime = millis();

  // Handle "PREV" button with debouncing
  if (isPrevPressed && !prevPressed && (currentTime - lastUpdate > debounceTime)) {
    Serial.println("PREV");
    prevPressed = true; // Mark as pressed
    lastUpdate = currentTime; // Update last press time
  }
  if (!isPrevPressed && prevPressed) {
    prevPressed = false; // Reset state if button is released
  }

  // Handle "NEXT" button with debouncing
  if (isNextPressed && !nextPressed && (currentTime - lastUpdate > debounceTime)) {
    Serial.println("NEXT");
    nextPressed = true; // Mark as pressed
    lastUpdate = currentTime; // Update last press time
  }
  if (!isNextPressed && nextPressed) {
    nextPressed = false; // Reset state if button is released
  }

  // Read serial input for system statuses and name
  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n'); // Read the incoming status message
    if (incomingData.length() >= 4) { // Check if the data is longer than just the status
      String status = incomingData.substring(0, 4); // First 3 characters are status
      displayName = incomingData.substring(4); // Rest is the display name

      digitalWrite(8, status.charAt(0) == '1' ? HIGH : LOW); // Set GPS state
      digitalWrite(9, status.charAt(1) == '1' ? HIGH : LOW); // Set OBD state
      digitalWrite(10, status.charAt(2) == '1' ? HIGH : LOW); // Set CONSUMER state
      digitalWrite(13, status.charAt(3) == '1' ? HIGH : LOW); // Set CONSUMER state

      lcd.setCursor(0, 1); // Move cursor to the beginning of the second line
      lcd.print("                "); // Clear the second line
      lcd.setCursor(0, 1); // Reset cursor position after clearing
      lcd.print(displayName); // Display the name on the second line
    }
  }
}
