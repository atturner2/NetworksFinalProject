import socket
import os
import signal
from threading import Thread
from SocketServer import ThreadingMixIn

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New server socket thread started for " + ip + ":" + str(port)
    #This function takes in the original client message and checks to see
    #which type of request it is.
    def checkIterativeOrRecursive(self, data):
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        IR = cleanedrequest[2]
        # returns 1 for Iterative
        # returns 0 for Recursive
        if IR.strip() == 'i' or IR.strip() == 'I':
            return 1
        elif IR.strip() == 'R' or IR.strip() == 'r':
            return 0


    # this function will take in com, dat, or org and return
    #the appropriate port number, for that given Iterative request.
    def getPortNumber(self, data):
        if data.strip().lower() == "org":
            return 5354
        if data.strip().lower() == "gov":
            return 5358
        if data.strip().lower() == "com":
            return 5356
        else:
            return 1

    def getDomainFromURL(self, data):
        #print "original data: ", data
        temp = data.split(".")
        #print "temp3: ", temp[2]
        domain = temp[2]
        return domain




    #this function will take in the request from the local server and return
    #the full return message needed to the "run" method, so that the run method
    # doesn't have to do any calculation.
    def iterativeRequest(self, data):
        port = 1
        print "Recieved an iterative request for :", data
        #this code block just splits the request for me
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        #print "Domain name to search for: ", cleanedrequest[1]
        domain = cleanedrequest[1].split(".")
        finaldomain = domain[2]
        #print "domain server to query: ", finaldomain
        port = self.getPortNumber(finaldomain)
        #print "final domain: ", finaldomain
        #print "final port number: ", port
        message = "<0x01, " + cleanedrequest[0] + ", "+ str(port) + ">"
        return message

    #this is the same as saveDomainForIterativeRequest in the local server,
    #it does the exact same thing, the only difference is for the name.
    def saveDomainForRecursiveRequest(self, data):
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        return cleanedrequest[1]

    #this function will take in a request and return what it gets back from the
    #com, org, or dat server.
    def recursiveRequest(self, data):
        print "Recieved a recursive request for :", data
        url = self.saveDomainForRecursiveRequest(data)
        #print "url: ", url
        domain = self.getDomainFromURL(url)
        #print "domain: ", domain
        port = self.getPortNumber(domain)
        #print "port number: ", port

        message = url
        host = socket.gethostname()
        BUFFER_SIZE = 2000
        print "Root server trying to connect on port: ", port


        RecursiveRequestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        RecursiveRequestSocket.connect((host, port))
        RecursiveRequestSocket.send(message)
        data = RecursiveRequestSocket.recv(BUFFER_SIZE)
        print "Here is data back from com, or or goc server to the root server: ", data
        return data

    def die(self):
        print"Dying!"
        os.kill(os.getpid(), signal.SIGKILL)

    #this is the main running function of the server, will call its helpers
    # to send back the proper response to the local server and the client.
    def run(self):
        #while True :
            data = conn.recv(2048)
            print "Server received data:", data
            if data == "q":
                self.die()
            # at this point we know the request is valid, so all we need to check
            # is whether or not it is recursive or iterative
            IR = self.checkIterativeOrRecursive(data)
            print "IR returned: ", IR
            if IR == 1:
                #call the iterative function(easier)
                message = self.iterativeRequest(data)
                print "Root Server sending message from Iterative Request: ", message
            if IR == 0:
                #call the Recursive function
                message = self.recursiveRequest(data)
                print "Root Server sending message from Recursive Request: ", message



            #MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            #if MESSAGE == 'exit':
                #break
            conn.send(message)  # echo

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 5353
BUFFER_SIZE = 20  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(4)
    print "Multithreaded Python root server : Waiting for connections from TCP clients..."
    (conn, (ip,port)) = tcpServer.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
