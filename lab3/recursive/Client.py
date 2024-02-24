import socket
import struct

ADDR = ('localhost', 2403)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    choice = input("Select your choice:\n1. sent message\n2. exit\n")
    if choice == '2':
        # client.sendto(DISCONNECT_MESSAGE.encode(FORMAT), ADDR)
        break
    else:
        try:
            client.connect(ADDR)
            message = input("Enter a message to send to the server: \n")
            client.sendto(message.encode(FORMAT), ADDR)

            msg, addr = client.recvfrom(SIZE)
            print('Received response from server: ')
            print('In bytes: ', msg)

            ms = msg.decode('utf-8')
            print('After Decoding: ', ms)
            ms = ms.split()
            print("final message: ", ms[2])
        except Exception as e:
            print('An error occurred:', e)
