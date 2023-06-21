# Drone-Speech
Here wii be code from my university project, where i control dji tello by communication through sockets and give command to him by recognizing the command from our speech. 

## Recognizing commands
For recognizing commands i use Reccurent Neural Network with lstm "elements", this network was trained on "Speech Command Dataset" where 65,000 one-second long utterances of 30 short words, by thousands of different people. But in case i train it only on ["yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go"] to improve recognition accuracy. 

## Sending commands 
For sending commands i have window from PySide6 library, where you need to press space button to start recording that have constatnt long(2s), then this recording wil recognize by network and if it find right command in this recording it will send it to tello drone.

## Commands 
yes - take off
no - land 

up - move up for 20cm
down - move down for 20cm

left - move left for 50cm
right - move right for 50cm 

