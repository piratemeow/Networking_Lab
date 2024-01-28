import socket

HEADER = 64
PORT = 2005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.33.2.88"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_msg():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        print(msg)
        
        
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    receive_msg()
    


while True:
    print("What you want to do?\n1 for making lowercase, \n2 for making making uppercase.\n3 for palindrome\n4 for checking prime.\n5 for closeing")
    s = input()
    if s == '5':
        send(DISCONNECT_MESSAGE)
        break
    s+=input()
    send(s)
    
    
    


