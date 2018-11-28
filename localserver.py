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

    #this function handles the special missing case when "www." is not included
    #in the url. it makes a new request to send in.
    def specialMissingWWWCase(self, data):
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        ID = cleanedrequest[0]
        hostname = cleanedrequest[1]
        IR = cleanedrequest[2]
        print "OldId: ", ID
        print "hostname: ", hostname
        print "IR: ", IR
        newhostname = "www." + hostname.strip()
        print "new host name: ", newhostname
        newmessage = "<" + ID + ", " + newhostname + "," + IR + ">"
        print newmessage
        return newmessage


    #this function validates the url field in the original query.
    def validateURL(self, data):
        print "validating URL"
        #1 for valid, #0 for invalid, 2 for missing www case
        isValid = 1
        requestone = data.replace("<", "")
        requesttwo = requestone.replace(">", "")
        cleanedrequest = requesttwo.split(",")
        hostname = cleanedrequest[1]
        print "hostname: ", hostname
        hostname_to_split = hostname.split(".")
        length = len(hostname_to_split)
        print"Length: ", length
        if length == 1:
            isValid = 0
        #now we check or the missing www case
        elif length == 2:
            if (hostname_to_split[1] == "org") or (hostname_to_split[1] == "com") or (hostname_to_split[1] == "gov"):
                print "missing www case true, message needs to be reformatted. Special Case Only."
                isValid = 2
            else:
                print "length is short but format is invalid. Mark Invalid."
                isValid = 0
        elif length == 3:
            if not ((hostname_to_split[2].strip().lower() == "org") or (hostname_to_split[2].strip().lower() == "com") or (hostname_to_split[2].strip().lower() == "gov")):
                print hostname_to_split[2]
                print "extension invalid, even though length is correct."
                isValid = 0
        else:
            isValid = 0
        return isValid
    #this function takes in the original client message and checks
    #to make sure the client id field is of valid format.
    def validateClientID(self, data):
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
        print "Length of hostname: ", len(hostname.split("."))
        #now we check for invalidity. we will first check the ClientID
        clientID.strip()
        print "Stripped ClientID: ", clientID
        if clientID != 'PC1' and clientID != 'PC2':
            isValid = 0
        #now we check the hostname for validity
        if len(hostname) == 1:
            isValid = 0
        #if len(hostname) == 2:
        if (IR.strip() != 'I') and (IR.strip() != 'R'):
            isValid = 0
            print "WE know its invalid!!"
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
    #domain server.  It takes in the whole query and returns just the domain.
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
        if int(port.strip()) = 1:
            print "Port is 1, invalid format"
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
            isValid1 = self.validateClientID(data)

            isValid2 = self.validateURL(data)

            if isValid1 == 0 or isValid2 == 0:
                conn.send("Invalid Request Format")
            elif isValid2 == 2:
                #call the message modifier for the specific www case
                data = self.specialMissingWWWCase(data)

                #check iterative or recursive
            IR = self.checkIterativeOrRecursive(data)
            if IR == 1 and isValid1 != 0 and isValid2 != 0:
                #request is Iterative, call iterative function
                message = self.iterativeRequestPartOne(data)
                conn.send(message)
            elif IR == 0 and isValid1 != 0 and isValid2 != 0:
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
