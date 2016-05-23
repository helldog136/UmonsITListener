import socket

def mainLoop(serversocket):
    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(500000)
        if len(buf) > 0:
            print "got something"
            print buf


if __name__ == "__main__":
    port = 4242
    print "Starting server on port ", port, "..."
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', port))
    serversocket.listen(5)  # become a server socket, maximum 5 connections
    while True :
        try:
            mainLoop(serversocket)
        finally:
            serversocket.close()
