// assign pin num
int right_pin = 6;
int left_pin = 7;
int forward_pin = 10;
int reverse_pin = 9;
int previous_command = 0;
bool valid_command = true;

// duration for output
int time = 50;
// initial command
int command = 0;

void setup() {
  pinMode(right_pin, OUTPUT);
  pinMode(left_pin, OUTPUT);
  pinMode(forward_pin, OUTPUT);
  pinMode(reverse_pin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  //receive command
  if (Serial.available() > 0){
    command = Serial.read();
  }
  else{
    reset();
  }
   send_command(command,time);
}

void right(int time){
  digitalWrite(right_pin, LOW);
  delay(time);
}

void left(int time){
  digitalWrite(left_pin, LOW);
  delay(time);
}

void forward(int time){
  digitalWrite(forward_pin, LOW);
  delay(time);
}

void reverse(int time){
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void forward_right(int time){
  digitalWrite(forward_pin, LOW);
  digitalWrite(right_pin, LOW);
  delay(time);
}

void reverse_right(int time){
  digitalWrite(reverse_pin, LOW);
  digitalWrite(right_pin, LOW);
  delay(time);
}

void forward_left(int time){
  digitalWrite(forward_pin, LOW);
  digitalWrite(left_pin, LOW);
  delay(time);
}

void reverse_left(int time){
  digitalWrite(reverse_pin, LOW);
  digitalWrite(left_pin, LOW);
  delay(time);
}

void reset(){
  digitalWrite(right_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
}


void print_command(int intcommand)
{
  if(previous_command != intcommand)
  {
    if(!valid_command)
    {
      Serial.print("Invalid command: ");
    }
    Serial.println(intcommand);
  }
  
}


int ascii_to_num(int ascii)
{
//  return ascii - 48;
  return ascii;
}

void send_command(int command, int time){

  // keep track of the commands and output if it has been updated
  int intcommand = ascii_to_num(command);
  print_command(intcommand);
  previous_command = intcommand;


  // send the command to the vehicle
  switch (intcommand){

     //reset command
     case 0: reset(); break;

     // single command
     case 1: forward(time); valid_command=true; break;
     case 2: reverse(time); valid_command=true; break;
     case 3: right(time); valid_command=true; break;
     case 4: left(time); valid_command=true; break;

     //combination command
     case 6: forward_right(time); valid_command=true; break;
     case 7: forward_left(time); valid_command=true; break;
     case 8: reverse_right(time); valid_command=true; break;
     case 9: reverse_left(time); valid_command=true; break;

     default: valid_command=false; print_command(intcommand);

    }
}
