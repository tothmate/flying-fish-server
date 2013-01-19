
/*
 * Protocol:
 * accepted characters: [LlRrUuDdSs]
 *   (left/right/up/down/reset)
 * any direction is sent to the fish until the opposite
 * direction or reset is received
 */


#define LEFT_PIN  2
#define RIGHT_PIN 4
#define UP_PIN    8
#define DOWN_PIN  6

int horizontal = 0; // 0-None, 1-left, 2-right
int vertical = 0; // 0-None, 1-up, 2-down

void setup() {
  Serial.begin(9600);
  pinMode(LEFT_PIN, OUTPUT);
  pinMode(RIGHT_PIN, OUTPUT);
  pinMode(UP_PIN, OUTPUT);
  pinMode(DOWN_PIN, OUTPUT);
}

void loop() {
  if(Serial.available() > 0) {
    char in = Serial.read();
    
    switch (in) {
      case 'S': case 's':
        horizontal=0;
        vertical=0;
        Serial.println("reset controls to 0");
        break;
      case 'L': case 'l':
        horizontal = (horizontal==1) ? 0 : 1;
        Serial.println("got command left");
        break;
      case 'R': case 'r':
        horizontal = (horizontal==2) ? 0 : 2;
        Serial.println("got command right");
        break;
      case 'U': case 'u':
        vertical = (vertical==1) ? 0 : 1;
        Serial.println("got command up");
        break;
      case 'D': case 'd':
        vertical = (vertical==2) ? 0 : 2;
        Serial.println("got command down");
        break;
    }
    
    if(horizontal == 1) 
      setLeft(); 
    else if(horizontal == 2)
      setRight();
    else
      resetHorizontal();

    if(vertical == 1)
      setUp();
    else if(vertical == 2)
      setDown();
    else
      resetVertical();

    
  }
  delay(10);
}


void setLeft() {
  digitalWrite(RIGHT_PIN, LOW);
  digitalWrite(LEFT_PIN, HIGH);
}

void setRight() {
  digitalWrite(LEFT_PIN, LOW);
  digitalWrite(RIGHT_PIN, HIGH);
}

void resetHorizontal() {
  digitalWrite(RIGHT_PIN, LOW);
  digitalWrite(LEFT_PIN, LOW);
}

void setUp() {
  digitalWrite(DOWN_PIN, LOW);
  digitalWrite(UP_PIN, HIGH);
}

void setDown() {
  digitalWrite(UP_PIN, LOW);
  digitalWrite(DOWN_PIN, HIGH);
}

void resetVertical() {
  digitalWrite(UP_PIN, LOW);
  digitalWrite(DOWN_PIN, LOW);
}
