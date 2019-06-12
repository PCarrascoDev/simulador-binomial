import sys
import random
import string
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import IncrementalBar


def randomString():
    """Generador de strings aleatorios"""
    stringLength = random.randint(1, 100)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def failRate(probPercent=7):
    """Calcular la probabilidad de fallo para el envío de cada paquete"""
    decimalProb = probPercent / 100

    #Retorna True en una probabilidad = (probPercent / 100), de lo contrario False
    return (random.random() < decimalProb) 

class Message():
    """Clase Message, contiene un string aleatorio en self.data"""
    def __init__(self):
        self.data = randomString()
    def getData(self):
        return self.data

class DataPacket():
    """Clase DataPacket; cada paquete de datos contiene n mensajes.
        *Por defecto n = 1"""
    def __init__(self):
        self.messages = []
    
    def appendMessage(self, message):
        #Añadir un mensaje a la lista
        self.messages.append(message)

    def getMessages(self):
        #Retornar los mensajes
        return self.messages

class Receiver():
    """Clase Receiver: encargado de recibir los paquetes de datos con mensajes."""
    def __init__(self):
        self.receivedPackets = []
    
    def receivePacket(self, packet):
        #Recibir 1 paquete de datos
        self.receivedPackets.append(packet)

    def countMessages(self):
        #Contar los mensajes en todos los paquetes de datos recibidos.
        msgCounter = 0
        for packet in self.receivedPackets:
            for message in packet.getMessages():
                msgCounter = msgCounter + 1

        return msgCounter

class WebServer():
    """Clase WebServer: encargada de enviar los paquetes de datos al Receiver"""
    def __init__(self, messagesByPacket=1, messagesNum=200):
        #Primero se generan 200 mensajes aleatorios
        self.messages = [Message() for x in range(messagesNum)]
        self.packets = []

        #Luego se crean paquetes de datos para enviar los mensajes, dependiendo la cantidad de mensajes.
        packetNum = 0
        while(len(self.messages) > 0):
            self.packets.append(DataPacket())
            
            #Si se supera la cantidad de mensajes por paquete, se crea otro paquete para llenar
            for x in range(messagesByPacket):
                if (len(self.messages) > 0):
                    #Se añade el mensaje al paquete, y se saca de la lista de mensajes, siempre y cuando la lista no esté vacía
                    self.packets[packetNum].appendMessage(self.messages.pop())

            #Si aún quedan mensajes, se siguen contando paquetes.
            if (len(self.messages) > 0):
                packetNum = packetNum + 1
    

    def sendPackets(self, receiver=Receiver()):
        #Esta función envía los paquetes a un receiver
        for packet in self.packets:
            #El envío de cada paquete es dependiente de la probabilidad de failRate()
            if(failRate() is not True):
                receiver.receivePacket(packet)

class Simulation():
    """Clase Simulation: se encarga de ejecutar la simulación n veces y luego plottearla en un histograma."""

    def __init__(self, repetitions=10000, messagesByPacket=1, messagesNum=200):
        self.Xvalues = []
        self.repetitions = repetitions
        bar = IncrementalBar('Simulando...', max = repetitions, suffix='%(percent)d%%')
        for x in range(repetitions):
            webServer = WebServer(messagesByPacket)
            receiver = Receiver()
            webServer.sendPackets(receiver)
            self.Xvalues.append(messagesNum - receiver.countMessages())

            bar.next()
        bar.finish()

    def plotSim(self):
        n, bins, patches = plt.hist(self.Xvalues, bins=range(min(self.Xvalues), max(self.Xvalues) + 1, 1), facecolor='blue', alpha=0.5)
        plt.xticks(bins)
        plt.grid()
        plt.xlabel("X (Mensajes no enviados correctamente)")
        plt.ylabel("Frecuencia")
        plt.show()
    
if __name__ == "__main__":
    sim = Simulation()
    sim.plotSim()

