# 1 for pdf and 2 for video
import socket
import threading
import os.path

format = "utf-8"
server = "localhost"
port = 9990

files = {"1" :"1.pdf","2":"2.mp4"}

s = socket.socket()

s.bind((server,port))

print("Server started\nlistening")

s.listen()
def handle_client(c,addr):

    message = "What do you want to download?\nebook-> press 1\nvideo -> press 2\n"

    c.send(bytes(message,format))

    option = c.recv(1234).decode(format)
    filename = files[option]
    try:
        with open(filename,'rb') as file:
            file_stat = os.path.getsize(filename)
            print("Sending "+filename)
            print(f"size {file_stat/1000000} MB")
            c.send(bytes(str(file_stat),format))
            c.send(file.read())
        print("File Sent")
        
    except FileExistsError:
        print("FILE IS FOUND")


while True:
    c,addr = s.accept()

    thread = threading.Thread(target=handle_client,args=(c,addr))
    thread.start()

s.close()





