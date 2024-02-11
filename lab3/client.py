import socket
import struct

ADDR = ('10.33.2.90', 2403)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect(ADDR)
while True:
    choice = input("Select your choice:\n1. sent message\n2. exit\n")
    if choice == '2':
        # client.sendto(DISCONNECT_MESSAGE.encode(FORMAT), ADDR)
        break
    else:
        try:
            message = input("Enter a message to send to the server: \n")
            client.sendto(message.encode(FORMAT), ADDR)

            msg, addr = client.recvfrom(SIZE)
            print('Received response from server: ')
            print('In bytes: ', msg)

            ms = msg.decode('utf-8')
            print('After Decoding: ', ms)
            ms = ms.split()

            while ms[2] != 'A':
                new_adr = ('10.33.2.90', int(ms[1]))
                print('Connecting to port', ms[1])
                print(f'{ms[0]} ')
                client.sendto(ms[0].encode(FORMAT), new_adr)
                msg, adr = client.recvfrom(SIZE)
                msg1 = msg.decode(FORMAT)
                print('Received response from server: ', msg1)
                ms = msg1.split()

                print('Final message: ', ms[1])

        except Exception as e:
            print('An error occurred:', e)
