import sys
import random
import string
import numpy as np
import matplotlib.pyplot as plt

def randomString():
    """Random String Generator"""
    stringLength = random.randint(0, 100)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def failRate(probPercent=7):
    decimalProb = probPercent / 100
    return (random.random() < decimalProb)

class Message():
    def __init__(self):
        self.data = randomString()
    def getData(self):
        return self.data

class DataPacket():
    def __init__(self):
        self.messages = []
    
    def appendMessage(self, message):
        self.messages.append(message)

    def getMessages(self):
        return self.messages

class Receiver():
    def __init__(self):
        self.receivedPackets = []
    
    def receivePacket(self, packet):
        self.receivedPackets.append(packet)

    def countMessages(self):
        msgCounter = 0
        for packet in self.receivedPackets:
            for message in packet.getMessages():
                msgCounter = msgCounter + 1

        return msgCounter

class WebServer():
    def __init__(self, messagesByPacket=1):
        self.messages = [Message() for x in range(200)]
        self.packets = []
        packetNum = 0
        while(len(self.messages) > 0):

            self.packets.append(DataPacket())
            for x in range(messagesByPacket):
                if (len(self.messages) > 0):
                    self.packets[packetNum].appendMessage(self.messages.pop())
            if (len(self.messages) > 0):
                packetNum = packetNum + 1
    
    def sendPackets(self, receiver=Receiver()):
        for packet in self.packets:
            if(failRate() is not True):
                receiver.receivePacket(packet)

class Simulation():
    def __init__(self):
        self.Xvalues = []
        for x in range(1000):
            
            webServer = WebServer()
            receiver = Receiver()
            webServer.sendPackets(receiver)
            print(200 - receiver.countMessages())
            self.Xvalues.append(200 - receiver.countMessages())

    def plotSim(self):
        n, bins, patches = plt.hist(self.Xvalues, num_bins, normed=1, facecolor='blue', alpha=0.5)

if __name__ == "__main__":
    sim = Simulation()
    sim.plotSim()