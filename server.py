import threading
import socket

host = '127.0.0.1'
port = 4444

port = int(input("Port: "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

class Client():
    def __init__(self, clientvar, username, addr):
        self.clientvar = clientvar
        self.username = username
        self.addr = addr


clients = []


def broadcast(message, senderClient = None):
    print(message.decode('ascii'))
    if(senderClient):
        message = (f"{senderClient.username}: {message.decode('ascii')}").encode('ascii')
    for thisClient in clients:
        thisClient.clientvar.send(message)

def handle(thisClient):
    while(True):
        try:
            message = thisClient.clientvar.recv(1024)
            broadcast(message, thisClient)
        except:
            thisClient.clientvar.close()
            print(f"{thisClient.username} disconnected with ip {thisClient.addr}")
            clients.remove(thisClient)
            break

def receive():
    while True:
        print("Listening...")
        clientvar, address = server.accept()
        print(f"connection from {str(address)}.")

        clientvar.send("username:".encode('ascii'))
        username = clientvar.recv(1024).decode('ascii')
        thisClient =  Client(clientvar,username,address) 
        clients.append(thisClient)

        broadcast(f"Welcome {thisClient.username}.".encode('ascii'))

        thread = threading.Thread(target=handle, args={thisClient,})
        thread.start()


receive()
