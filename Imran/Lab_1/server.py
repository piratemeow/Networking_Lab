import socket

s = socket.socket() #by default it has ipv4 and tcp parameters. Otherwise it has to be passed

print("Socket Created\n")
format = 'utf-8'  #encoding and decoding format
server = 'localhost'  # Specifying the server ip
port = 9999        # specifying the port number
buffer = 1024 # Defines the maximus byte size of the message that can be received at once 
s.bind((server,port))  # binding server ip  address and port number



def handle_client(c,addr):  # handes client requests
    name = c.recv(buffer).decode(format)
    message = "Welcome"+" "+name
    encoded_message = bytes(message,format)  #have to convert the message to bytes before sending
    c.send(encoded_message)

    

def start():  #Starts the server and connects to the client
    s.listen() # to start listening to client requests
    print("Waiting for clients")
    while True:
        c, addr = s.accept() # returns the client socket and client address/ip+port
        name = c.recv(buffer).decode() #Name of the client. Not necessary
        print("Connected with",addr,name)
        handle_client(c,addr)  
        c.close() 

print("Server Started\n")
start()
