import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#ip = input("Enter server IP address you want to connect: ")

client.bind(("192.168.0.4", random.randint(50000, 60000)))

name = input("Enter username: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024) 
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.0.4", 40000))

while True:
    message = input("Enter message: ")
    if message == "exit":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("192.168.0.4", 40000))