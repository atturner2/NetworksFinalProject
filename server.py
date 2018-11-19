import socket
from threading import Thread
from SocketServer import ThreadingMixIn
#this is the default local DNS server.  It now receives the request from the client
#and sends it to the root DNS server.
# Multithreaded Python server : TCP Server Socket Thread Pool
#<1, www.google.com, I>
class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New server socket thread started for " + ip + ":" + str(port)

        #this function takes in the original client message and checks
        #to make sure it is of valid format.
    def validateClientMessage(self, data):
        isValid = 1
        print "recieved message to validate: ", data
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        clientID = cleanedrequest[0]
        hostname = cleanedrequest[1]
        IR = cleanedrequest[2]
        print "hostname: ", hostname
        print "IR: ", IR
        #now we check for invalidity. we will first check the ClientID
        clientID.strip()
        print "Stripped ClientID: ", clientID
        if clientID != 'PC1' and clientID != 'PC2':
            isValid = 0
        #now we check the hostname for validity
        #now we check the Iterative or Revursive for validity
        #Now we check the hostname for validity

        return isValid

        #This function takes in the original client message and checks to see
        #which type of request it is.
    def checkIterativeOrRecursive(self, data):
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        IR = cleanedrequest[2]
        print "IR: ", IR
        # returns 1 for Iterative
        # returns 0 for Recursive
        if IR == 'i' or IR == 'I':
            return 1
        else:
            return 0

    def recursiveRequest(self, data):
        print "Here is our recursive request to send to the root: ", data

    def iterativeRequest(self, data):
        print "Here is our Iterative request to send to the root: ", data

    def run(self):
        while True :
            data = conn.recv(2048)
            print "Server received data:", data
            #now we will first validate the request from the client
            #we will use our defined validate message function
            #note each function is called with the original request.
            #I didn't mind copy and pasting the same code, but with
            #this function as complicated as it is, I didn't want
            #it to look crazy with all the message parsing
            isValid = self.validateClientMessage(data)
            if isValid == 0:
                conn.send("Invalid Request Format")
            else:
                #check iterative or recursive
                IR = self.checkIterativeOrRecursive(data)
            if IR == 1:
                #request is Iterative, call iterative function
                self.iterativeRequest(data)
            if IR == 0:
                #request is Recursive, call recursive function
                self.recursiveRequest(data)





            MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter q:")
            if MESSAGE == 'q':
                break
            conn.send(MESSAGE)  # echo
    #this function takes in the request from the
    #client and makes sure it is valid. Returns 1 for valid and returns 0 for
    #invalid.


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 5352
BUFFER_SIZE = 20  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(4)
    print "Multithreaded Python server : Waiting for connections from TCP clients..."
    (conn, (ip,port)) = tcpServer.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
