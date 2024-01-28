import socket

HEADER = 64
PORT = 2005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.33.2.88"
ADDR = (SERVER, PORT)
LOGIN = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_msg():
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

while LOGIN==True:
    print("You can do the following tasks:")
    print("1 for checking balance, \n2 for depositning, \n3 for withdrals\n4 fro exit")
    s = input()
    if s == '4':
        send(DISCONNECT_MESSAGE)
        break
    s+=input()
    send(s)


