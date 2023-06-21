import sys
import socket
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time
import torch
from rty import Rec
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from com import model_api, predict_end

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.n = 43  # initialize file counter
        self.recording = None
        self.start_time = None
        self.fs = 16000  # sampling frequency
        self.flag = False
        self.model = model_api()

        # Initialize Tello drone control using sockets
        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.tello_port)) 

        self.send_command("command")  # Initialize SDK mode

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
            return

        self.recording = sd.rec(2 * self.fs, samplerate=self.fs, channels=1, dtype='int16', mapping=[1])

        print("Recording...")
        filename = "Ter.wav"  # use current file counter in filename   
        self.n += 1  # increment file counter

        sd.wait()
        print("Done recording")

        wav.write(filename, self.fs, self.recording.astype(np.int16))  # convert to int16 before saving
        prediction = predict_end("Ter.wav", self.model)
        print(prediction)
        self.control_tello(prediction)
        # print(Rec(filename))

    def send_command(self, command):
        self.socket.sendto(command.encode('utf-8'), self.tello_address)

    def control_tello(self, command):
        if command == "yes":
            self.send_command("takeoff")
            print(self.socket.recvfrom(1024))
        elif command == "no":
            self.send_command("land")
            print(self.socket.recvfrom(1024))
        elif command == "right":
            
            self.send_command("right 20")
            print(self.socket.recvfrom(1024))
        elif command == "left":
               
                self.send_command("left 20")
                print(self.socket.recvfrom(1024))
        elif command == "go" or command == "on":
                # self.send_command("flip b")
                # print(self.socket.recvfrom(1024))
                print("go command")
        elif command == "up":
            self.send_command("up 40")
            print(self.socket.recvfrom(1024))
        
        elif command == "down":
            self.send_command("down 20")
            print(self.socket.recvfrom(1024))


        # Add more commands here as needed 
        else:
            print(f"Unknown command: {command}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

main()
