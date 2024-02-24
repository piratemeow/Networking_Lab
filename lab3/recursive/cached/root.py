import os
import socket
import threading
import struct

IP = 'localhost'
PORT = 4487
ADDR = (IP, PORT)
tld = (IP, 4488)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
dic = {
    "www.google.com": ('100.20.8.1', 'A', 86400),
    "www.cse.du.ac.bd": ('100.20.55.2', 'A', 86400),
    "www.yahoo.com": ('100.20.89.7', "A", 86400)
}





def handle_client(data, addr, server):
    try:
        print(f"[RECEIVED MESSAGE] {data} from {addr}.")
        if dic[data][1] == 'A' or dic[data][1] == 'AAAA':
            msg = str(data + ' ' + dic[data][0] + ' ' + dic[data][1] + ' ' + str(dic[data][2]))
            server.sendto(bytes(msg,FORMAT), addr)

    except Exception as e:
        print("ERROR: ", str(e))
        server.sendto(('error').encode(FORMAT), addr)


print("[STARTING] ROOT Server is starting")
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)
print(f"[LISTENING] ROOT Server is listening on {IP}:{PORT}.")

while True:
        data, addr = server.recvfrom(SIZE)
        data = data.decode(FORMAT)
        # thread = threading.Thread(target=handle_client, args=(data, addr,server))
        # thread.start()
        handle_client(data, addr, server)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


