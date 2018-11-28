# Python TCP Client A
import socket

host = socket.gethostname()
port = 5352
BUFFER_SIZE = 2000
MESSAGE = raw_input("tcpClientA: Enter input filename/ Enter q to quit:")

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

def writeToMappingFile(url, ip):
    print"Here is the request to put in the map file:", url, ", ", ip
    request = url + ", " + ip + " \n"
    mapfile = open("mapping.log", "a")
    mapfile.write(request)

while MESSAGE != 'q':
    file = open(MESSAGE)
    for line in file:
        tcpClientA.send(line)
        data = tcpClientA.recv(BUFFER_SIZE)
        #here we parse for the for ip address
        responseone = data.replace("<", "")
        responsetwo = responseone.replace(">", "")
        cleanedresponse = responsetwo.split(",")
        #Here we parse for the original URL we requested
        urlone = line.replace("<", "")
        urltwo = urlone.replace(">", "")
        cleanedurl = urltwo.split(",")

        if cleanedresponse[0] == "0x00":
            ip = cleanedresponse[2]
            url = cleanedurl[1]
            #writeToMappingFile(url, ip)

    MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter q to quit:")

tcpClientA.close()
