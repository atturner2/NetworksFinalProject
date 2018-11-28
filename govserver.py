import socket
import os
import signal
from threading import Thread
from SocketServer import ThreadingMixIn
# -*- coding: utf-8 -*-

#this is the default local DNS server.  It now receives the request from the client
#and sends it to the root DNS server.
# Multithreaded Python server : TCP Server Socket Thread Pool
#<1, www.google.gov, I>
class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New server socket thread started for " + ip + ":" + str(port)

    def die(self):
        print"Dying!"
        os.kill(os.getpid(), signal.SIGKILL)

    #this file takes in the domain and returns the proper message
    def openAndReadDatFile(self, data):
        file = open('datfiles/gov.dat')
        print "IN the open file function"
        message = "<OxFF, gov, 'Host Not Found'>"
        for line in file:
             temp = line.split()
             domain = temp[0]
             lowereddata = data.lower()
             if lowereddata.strip() == domain.strip():
                 print"here in the if"
                 message = "<0x00, gov, " + temp[1] + ">"
        return message
    #Here we have the gov server. All it does is recieve requests and then check the gov
    #directories to see if they have what we need.
    def run(self):
        #while True :
        data = conn.recv(2048)
        print "Server received request:", data
        if data == "q":
            self.die()
        file = open('datfiles/gov.dat')
        message = self.openAndReadDatFile(data)
        print"response message sent: ", message
        print message
        conn.send(message)  # echo
    #this function takes in the request from the
    #client and makes sure it is valid. Returns 1 for valid and returns 0 for
    #invalid.


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 5358
BUFFER_SIZE = 20  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(4)
    print "Multithreaded Python gov server : Waiting for connections from TCP clients..."
    (conn, (ip,port)) = tcpServer.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
