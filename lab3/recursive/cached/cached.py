import socket
import struct
import time

IP = 'localhost'
PORT = 4487
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
cached = {}



def handle_caches():
    for ki in cached:
        if cached[ki] == "DELETED":
            continue

        cur_time = int(time.perf_counter())
        elapsed_time = (cur_time - int(cached[ki][3])) * 1000
        if elapsed_time > cached[ki][2]:
            cached[ki] = "DELETED"


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
        message = input("Enter an address or enter 'data' to see the cahed data: ")
        if message == "data":
            print('\n ______Cached Data______\n')
            for i in cached:
                print(i + ' ' + cached[i][0])
                continue
            print('\n ______End______\n')
        else:
            client.sendto(message.encode(FORMAT), ADDR)
            msg, addr = client.recvfrom(SIZE)

            # print(struct.unpack("6H",msg))
            # msg,addr=client.recvfrom(SIZE)
            msg = msg.decode(FORMAT)
            print('hi' + msg)
            qu = msg.split()
            if qu[0] == 'error':
                continue
            else:
                cached[qu[0]] = (qu[1], qu[2], qu[3])


