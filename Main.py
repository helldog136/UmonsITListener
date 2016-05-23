import socket
import json
import os

baseDir = "/tmp/UmonsITListener/"

def mainLoop(serversocket):
    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(500000)
        if len(buf) > 0:
            #isolate JSON from message
            isJson = False
            js = ""
            for line in buf:
                if line[0]=="{":
                    isJson = True
                if isJson:
                    js += line
            #extract repo name
            jsdoc = json.JSONDecoder().decode(js)
            repository = jsdoc["repository"]["name"]
            #launch the update routine
            #first check if repo has already been cloned
            dirName = baseDir+repository
            if not (os.path.exists(dirName) and os.path.isdir(dirName)):
                clone(jsdoc["repository"]["git_url"], dirName)
            pull(repository, dirName)

def clone(url, dirName):
    print "Cloning ", url, " in ", dirName

def pull(repo, dirName):
    print "Pulling ", repo, " in ", dirName


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
    serversocket.close()
