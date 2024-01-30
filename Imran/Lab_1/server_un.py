import socket
import threading
import random
HEADER = 64
PORT = 9999
SERVER = 'localhost'
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# print(SERVER)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

balance = 10000
for_rollback = 0
amount_rollback = ""
def login(id,passkey):
    id = int(id)
    passkey = int(passkey)
    if(id==1234) and (passkey==1234):
        return True
    else:
        return False
    
def checkBalance():
    return str(balance)

def credit(message):
    global balance
    message = int(message)
    if (message<=0):
        return "Please give a valid amount"
    balance += message
    return(f"Credited Successfully. Total balance {balance}")
    
def debit (message):
    global balance
    message = int(message)
    if message>balance:
        return ("Insuficient balance")
    balance-=message
    return f"Debited successfullt total balance {balance}"
    

        

def random_error(error):
    if random.randint(1, 10) <= error:
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
    print(f'[New Connection] {addr} connected')

    connected = True
    while connected:
        
        
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg=='ROLLBACK':
                if for_rollback==2:
                    debit(amount_rollback)
                    send("Roll back Successfull",conn)
                elif for_rollback==3:
                    credit(amount_rollback)
                    send("Roll back Successfull",conn)
            
            elif (msg[0]=='u'):
                id = msg.split(" ")[0][1:]
                passkey = msg.split(" ")[1][1:]
                print(id,passkey)
                if (login(id,passkey)):
                    print("Login Successful")
                    send("True",conn)
                else:
                    print("Wrong Id or Passkwy")
                    send("False",conn)
            elif msg[0]=='1':
                send(checkBalance(),conn)
            elif msg[0]=='2':
                for_rollback = 2
                amount_rollback = msg[1:]
                send(credit(msg[1:]),conn)
            elif msg[0]=='3':
                for_rollback = 3
                amount_rollback = msg[1:]
                send(debit(msg[1:]),conn)
                
             
            if msg == DISCONNECT_MESSAGE:
                connected = False
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
