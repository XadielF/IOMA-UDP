from cryptography.fernet import Fernet
import socket
import threading
import queue

messages = queue.Queue()
clients = []

#generating a key for encryption
key =  Fernet.generate_key()

#Instance the Fernet class with the key
fernet = Fernet(key)

#Creating UDP Socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("192.168.0.4", 40000))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            #PRINT WITHOUT ENCRYPTION
            #print(message.decode())

            #PRINT WITH ENCRYPTION
            print(fernet.encrypt(message).decode())
            
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined the server!".encode(), client)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()