import socket
import random
import time



HEADER = 64
PORT = 2005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.33.2.75"
ADDR = (SERVER, PORT)
LOGIN = False
count = 0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_msg():
    global count
    msg_length = client.recv(HEADER).decode(FORMAT)
    global LOGIN
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        if(str(msg)=="True"):
            LOGIN=True
            print("Login successful")
        elif(str(msg)=="False"):
            print("Login failed...")
        else:
            if msg == 'ERROR':
                count-=1
                #send("ROLLBACK")
            print(msg)
            
            
        
        
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    receive_msg()
    

while LOGIN==False:
    print("Please Login... or write \'esc\' to exit...")
    username = input("Username: ")
    if(username=='esc'):
        send(DISCONNECT_MESSAGE)
        exit()
    password = input("Password: ")
    send('u'+username+" "+'p'+password)


start_time = time.time()
while LOGIN==True:
    #print("You can do the following tasks:")
    #print("1 for checking balance, \n2 for depositning, \n3 for withdrals\n4 fro exit")
    # Generate a random integer between 1 and 10 (inclusive)
    count+=1
        
    s = random.randint(2, 3)
    print(s)

    if s == 1:
        send('1')
    elif s == 2:
        amount=random.randint(1000,50000)
        send(2+" "+amount)
    elif s == 3:
        amount=random.randint(1000,50000)
        send(3+" "+amount)
    elif s == 4:
        send(DISCONNECT_MESSAGE)
        exit()
    if count == 100:
        break
end_time = time.time()

print(end_time-start_time)

