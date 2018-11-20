import socket
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
    #def getPortNumberForIterativeRequest(self,data):


    #this function will take in the request from the local server and return
    #the full return message needed to the "run" method, so that the run method
    # doesn't have to do any calculation.
    def iterativeRequest(self, data):
        print "Recieved an iterative request for :", data
        #this code block just splits the request for me
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        print "Domain name to search for: ", cleanedrequest[1]
        domain = cleanedrequest[1].split(".")
        finaldomain = domain[2]
        print "domain server to query: ", finaldomain
        if finaldomain.strip() == 'org'
            port = 5354
        elif finaldomain.strip == 'gov'
            port = 5355
        elif finaldomain.strip == 'com'
            port = 5356

    #this function will take in a request and return what it gets back from the
    #com, org, or dat server.
    def recursiveRequest(self, data):
        print "Recieved a recursive request for :", data
    #this is the main running function of the server, will call its helpers
    # to send back the proper response to the local server and the client.
    def run(self):
        while True :
            data = conn.recv(2048)
            print "Server received data:", data
            # at this point we know the request is valid, so all we need to check
            # is whether or not it is recursive or iterative
            IR = self.checkIterativeOrRecursive(data)
            print "IR returned: ", IR
            if IR == 1:
                #call the iterative function(easier)
                self.iterativeRequest(data)
            if IR == 0:
                #call the Recursive function
                self.recursiveRequest(data)


            MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE == 'exit':
                break
            conn.send(MESSAGE)  # echo

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
    print "Multithreaded Python server : Waiting for connections from TCP clients..."
    (conn, (ip,port)) = tcpServer.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
