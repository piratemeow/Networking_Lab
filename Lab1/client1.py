import socket

HEADER = 64
PORT = 2005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_msg():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        print(f'Received from Server: {msg}')
        
        
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    receive_msg()
    

print("Connected to the server")
while True:
    print("What you want to do? Please enter\n1 for making uppercase, \n2 for making making lowecase.\n3 for palindrome.\n4 for checking prime.\n5 for closeing.")
    s = input()
    if s == '5':
        send(DISCONNECT_MESSAGE)
        break
    elif s=='1' or s == '2':
        s+=input("give a sentence or word: ")
    elif s == '3' or s =='4':
        s+=input("give a number: ")
    send(s)
    
    
    


