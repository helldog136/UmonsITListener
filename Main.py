import socket

def mainLoop(serversocket):
    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(64)
        if len(buf) > 0:
            print buf


if __name__ == "__main__":
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 4242))
    serversocket.listen(5)  # become a server socket, maximum 5 connections
    while True :
        mainLoop(serversocket)