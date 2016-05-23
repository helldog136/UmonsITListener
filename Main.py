import socket
import json
import datetime
import os
import git

baseDir = "/tmp/UmonsITListener"
targetDir = baseDir+"/CompiledPDFs/"
pdfRepoUrl= "https://github.com/UMonsIT/CompiledPDFs.git"

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
            repoUrl = jsdoc["repository"]["git_url"]
            print "Detected changes in", repository, "("+repoUrl+")"
            #launch the update routine
            #first check if repo has already been cloned
            dirName = baseDir+repository
            if not (os.path.exists(dirName) and os.path.isdir(dirName)):
                clone(repoUrl, dirName)
            pull(repository, dirName)

            if not (os.path.exists(targetDir) and os.path.isdir(targetDir)):
                clone(pdfRepoUrl, baseDir)
            compileAndMove(dirName, repository, targetDir)
            commitAndPush(targetDir)

def clone(url, dirName):
    print "Cloning", url, "in", dirName
    repo = git.Repo.clone_from(url, dirName)
    print "Done cloning..."

def pull(repo, dirName):
    print "Pulling", repo, "in", dirName
    git.Repo(dirName).remote().pull()

def compileAndMove(compileDir, repoName, targetDir):
    print "Compiling", repoName, "in", compileDir
    # TODO
    move(compileDir, repoName, targetDir)

def move(compileDir, repoName, targetDir):
    print "Copying PDFs in", compileDir, "to", targetDir+repoName
    #TODO

def commitAndPush(target):
    message = "Auto-compiled on " + datetime.datetime.now().isoformat()
    print "Commiting", target, "with message", message
    git.Repo(target).commit(message)
    print "Pushing", target
    git.Repo(target).remote().push()


if __name__ == "__main__":
    port = 4242
    print "Starting server on port ", port, "..."
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', port))
    serversocket.listen(5)  # become a server socket, maximum 5 connections
    try:
        while True :
            mainLoop(serversocket)
    finally:
        serversocket.close()
