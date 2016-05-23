import socket
import json
import datetime
import os

baseDir = "/tmp/UmonsITListener/"
targetDir = baseDir+"CompiledPDFs/"

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
            print "Detected changes in", repository, "("+jsdoc["repository"]["git_url"]+")"
            #launch the update routine
            #first check if repo has already been cloned
            dirName = baseDir+repository
            if not (os.path.exists(dirName) and os.path.isdir(dirName)):
                clone(jsdoc["repository"]["git_url"], dirName)
            pull(repository, dirName)
            compileAndMove(dirName, targetDir)
            commitAndPush(targetDir)

def clone(url, dirName):
    print "Cloning", url, "in", dirName

def pull(repo, dirName):
    print "Pulling", repo, "in", dirName

def compileAndMove(compileDir, targetDir):
    print "Compiling", compileDir
    move(compileDir, targetDir)

def move(compileDir, targetDir):
    print "Copying PDFs in", compileDir, "to", targetDir

def commitAndPush(target):
    print "Commiting", target, "with message",
    message = "Auto-compiled on " + datetime.datetime.now().isoformat()
    print message
    print "Pushing", target


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
