import socket
import threading
host = 'localhost'

port = 4488


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
dic={
    "www.google.com":('100.20.8.1','A',86400),
    "www.cse.du.ac.bd": ('4489','NS',86400),
    "www.yahoo.com":('10.33.2.44',"A",86400),
    "www.youtube.com":('4489','NS',86400)
}


print("SERVER STARTED")

def handle_client(data,addr):
    print(addr)


    # print(requested_name,requested_type)

    # file1 = open("servers.txt","r")

    if data in dic:
        msg = f'{data} {dic[data][0]} {dic[data][1]} {dic[data][2]}'
        
        s.sendto(bytes(msg,'utf-8'),addr)
        print(msg)
        
    else:
        print("No value found")
        s.sendto(bytes("Not found ",'utf-8'),addr)
        return 




while True:
    data,addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    print(data)
    thread = threading.Thread(target=handle_client,args=(data,addr))
    thread.start()