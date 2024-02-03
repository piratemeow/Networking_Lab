import socket
import threading

HEADER = 64
PORT = 2005
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# print(SERVER)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def message_capitalize(message):
    return message.upper()

def message_smallarize(message):
    return message.lower()

def isPalindrome(message):
    if message == message[::-1]:
        return True
    else:
        return False
    
def isPrime(message):
    message = int(message)
    print(message)
    if message==1:
        return False
    count = 0
    for i in range(1,message+1):
        if(message%i ==0):
            count +=1
    if (count==2):
        return True
    else:
        return False
    
   


def send(msg,conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    conn.send(send_length)
    conn.send(message)
    

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg[0]=='1':
                print(f'Capitalize {msg[1:]}')
                print(message_capitalize(msg[1:]))
                send(f'Capitalized message: {message_capitalize(msg[1:])}',conn)
            elif msg[0]=='2':
                print(f'Smallarize {msg[1:]}')
                print(message_smallarize(msg))
                send(f'Smallaraized message: {message_smallarize(msg[1:])}',conn)
            elif msg[0]=='3':
                print(f'Check palindrome {msg[1:]}')
                print(isPalindrome(msg[1:]))

                if isPalindrome(msg[1:]):
                    send(f'{msg[1:]} is a palindrome', conn)
                else:
                    send(f'{msg[1:]} is not a palindrome', conn)

            elif msg[0]=='4':
                print(f'Check prime {msg[1:]}')
                if isPrime(msg[1:]):
                    send(f'{msg[1:]} is a prime', conn)
                else:
                    send(f'{msg[1:]} is not a prime', conn)
            
                
            
            if msg == DISCONNECT_MESSAGE:
                connected = False
                send("SERVER is disconnected",conn)
                print(f"[{addr}] {msg}")


    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")

    pass


print("[Starting] server is starting...")
start()


    
