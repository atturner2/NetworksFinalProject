# Python TCP Client A
import socket

host = socket.gethostname()
port = 5352
BUFFER_SIZE = 2000
MESSAGE = raw_input("tcpClientA: Enter input filename/ Enter q to quit:")

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))


while MESSAGE != 'q':
    file = open(MESSAGE)
    for line in file:
        print line



        tcpClientA.send(line)
        data = tcpClientA.recv(BUFFER_SIZE)
        print " Client2 received data:", data

    MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter q to quit:")

tcpClientA.close()
