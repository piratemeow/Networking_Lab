# 1 for pdf and 2 for video
import socket
import threading
import os.path

format = "utf-8"
server = "localhost"
port = 9990

files = {"1" :".pdf","2":".mp4"}
filename = "received"

c = socket.socket()


print("client started")


c.connect((server,port))

options = c.recv(1234).decode(format)

select = input(options)

c.send(bytes(select,format))

x = c.recv(1234).decode(format)
file_data = b""
while len(file_data)<int(x):
    print(len(file_data))
    chunk = c.recv(100000000)
    if not chunk:
        break
    
    file_data+=chunk

with open(filename+files[select],"wb") as file:
    file.write(file_data)

    file.close()    
    print("file received")

print(int(x)/1000000 ," MB")
c.close()
