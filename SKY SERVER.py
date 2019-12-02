import socket #for networking
import threading #for synchronous execution of functions
import os #for gathering filenames/directories
import base64 #for encoding/decoding data sent across the network
import math #for calculations in convertSie function
import time
import sys
global allFiles
global printThis
allFiles = os.listdir()
hasRan = False

def infoFunc(sock):
    if hasRan == False:
        def convertSize(size_bytes):
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            x = round(size_bytes / p, 2)
            return "%s %s" % (x, size_name[i])
        
        allFiles = os.listdir() #gathers all files in root directory
        finalList = []
        for file in allFiles:
            theSize = os.path.getsize(file)
            theConvertedSize = convertSize(theSize)
            final =  file + "..." + theConvertedSize + "ZZ" + str(theSize) #used to be theConvertedSize
            finalList.append(final)
            
        printThis = "\n".join(finalList)
        print("List of files available files sent to client...")
        sock.send(str.encode("NAMES ") + str(printThis).encode())

    


def RetrFile(name, sock):
    print("Waiting for file request")
    name = name
    sock = sock
    hasRan = True
    filename = ""
    filename = sock.recv(1024)
    filename = filename.decode()
    print("Request for " + filename)
    
    if os.path.isfile(filename):
        sock.send(str.encode("EXISTS") + str(os.path.getsize(filename)).encode())
        print("file exists, waiting for response from client")
        userResponse = sock.recv(1024) 
        userResponse = userResponse.decode()
        print("recieved client response, attempting to establish Rget connection")
        if userResponse[:2] == 'OK':
            print("Rget FILE: " + filename)
            with open(filename, 'rb') as f:
                print("connection established, sending...")
                bytesToSend = f.read(3000000)
                sock.sendall(bytesToSend)
                byteCounter = 0
                while str(bytesToSend) != "b''":
                    byteCounter += 1
                    print("Packet #" + str(byteCounter), end="\r")
                    sys.stdout.flush()
                    bytesToSend = f.read(8192)
                    sock.sendall(bytesToSend)
                    
                print(filename + " successfully transfered to client")
                #
        global allFiles
        RetrFile(name, sock) # NEW LINE
        if userResponse in allFiles:
            print("Client denied transfer of " + str(filename) + ", reconnecting...")            

            RetrFile(name, sock)
    else:
        print("Client disconnected...")
        sock.send(str.encode("ERR "))
        sock.close()

def Main():
    host = '192.168.254.199'
    port = 55435
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(5)
    print("Server IP: %s\nServer Port: %s" %(host, port))
    
    while True:
        c, addr = s.accept()        
        print("client connected with IP and Port:<" + str(addr) + ">")
        infoFunc(c)
        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t.start()

    s.close()

if __name__ == '__main__':
    Main()
