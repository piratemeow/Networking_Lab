import socket

c = socket.socket() #by default it has ipv4 and tcp parameters. Otherwise it has to be passed

server = 'localhost'
port = 9999
buffer = 1024 # Defines the maximus byte size of the message that can be received at once 
                # if the message size is greater than the buffer size
                # then multiple recv() method calls will be required to get the whole message
                # loop can be used in this case

def server_connect(server,port): #to connect to the server
    c.connect((server,port))  # making the connection to the server
    name = input("What is the client's name\n")
    c.send(bytes(name,'utf-8')) #sending message to the server. It has to be in bytes object
    c.send(bytes(name,'utf-8'))

def receive_message():
    message = c.recv(buffer).decode() # decode method decodes the bytes to str
    print(message)

server_connect(server,port)
receive_message()
