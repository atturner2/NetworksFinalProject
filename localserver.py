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
        if IR.strip() == 'i' or IR.strip() == 'I':
            return 1
        else:
            return 0

    def recursiveRequest(self, data):
        print "Here is our recursive request to send to the root: ", data
        host = socket.gethostname()
        port = 5353
        BUFFER_SIZE = 2000
        MESSAGE = data

        RecursiveRequestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        RecursiveRequestSocket.connect((host, port))
        RecursiveRequestSocket.send(MESSAGE)
        data = RecursiveRequestSocket.recv(BUFFER_SIZE)
        print "Local Server Recieved received data:", data
        return data
    #this function parses for just the domain name to be queried from it's appropriate
    #domain server.
    def saveDomainForIterativeRequest(self, data):
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        return cleanedrequest[1]

    #this parses the message from the root server and returns the port number
    # which is how we identify the com, org, and gov servers.
    def grabPortNumberForIterativeRequest(self, data):
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        return cleanedrequest[2]

    #This function takes the port number returned from the Root server and queries
    #the appropriate com, org, or gov server. It takes in the domain from the first
    #function and uses that to query the appropriate server for the needed information.
    def iterativeRequestPartTwo(self, data, domain):
        print"querying bottom DNS server for iterative request with :", data
        print "domain to query with: ", domain
        port = self.grabPortNumberForIterativeRequest(data)
        print "here is the port to get the domain from: ", int(port.strip())
        message = domain

        host = socket.gethostname()
        BUFFER_SIZE = 2000


        RecursiveRequestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        RecursiveRequestSocket.connect((host, int(port.strip())))
        RecursiveRequestSocket.send(message)
        data = RecursiveRequestSocket.recv(BUFFER_SIZE)
        print "Here is Iterative request back from the server: ", data
        return data
    # this function queries the root server for the port number of the
    #appropriate domain server.  It then calls the part two function
    # which will then in turn query the domain server directly.
    def iterativeRequestPartOne(self, data):
        print "Here is our Iterative request to send to the root: ", data
        domain = self.saveDomainForIterativeRequest(data)

        host = socket.gethostname()
        port = 5353
        BUFFER_SIZE = 2000
        MESSAGE = data

        RecursiveRequestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        RecursiveRequestSocket.connect((host, port))
        RecursiveRequestSocket.send(MESSAGE)
        data = RecursiveRequestSocket.recv(BUFFER_SIZE)
        print "Local Server Recieved received data from root for iterative request:", data
        message = self.iterativeRequestPartTwo(data, domain)
        return message

    def changeURLToLowercase(self, data):
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")

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
                message = self.iterativeRequestPartOne(data)
            if IR == 0:
                #request is Recursive, call recursive function
                message = self.recursiveRequest(data)
            conn.send(message)  # echo
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
