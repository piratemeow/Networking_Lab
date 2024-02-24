import socket
import threading

host = 'localhost'

port = 2403
TLD=(host,4488)
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
dic = {
    "www.google.com": ('100.20.8.1', 'A', 86400),
    "www.cse.du.ac.bd": ('dns.cse.du.ac.bd', 'NS', 86400),
    "www.yahoo.com": ('dns.yahoo.com', "NS", 86400),
    "www.youtube.com": ('dns.youtube.com', 'NS', 86400)
}

print("SERVER STARTED")


def handle_client(data, addr):
    print(addr)

    # print(requested_name,requested_type)

    # file1 = open("servers.txt","r")

    print(f"[RECEIVED MESSAGE] {data} from {addr}.")
    if (dic[data] != None):
        try:
            if dic[data][1] == 'A' or dic[data][1] == 'AAAA':
                msg = f'{data} {dic[data][0]} {dic[data][1]} {dic[data][2]}'
                s.sendto(bytes(msg, 'utf-8'), addr)
                print(msg)
            else:
                print("Sending to TLD server")
                s.sendto(data.encode(FORMAT), TLD)

                ans, tld_adr = s.recvfrom(1024)
                msg = ans.decode(FORMAT)
                s.sendto(bytes(msg, 'utf-8'), addr)
                print(msg)
        except Exception as e:
            print("ERROR: ", str(e))

    else:
        print("No value found")
        s.sendto(bytes("Not found ", 'utf-8'), addr)
        return


while True:
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    # thread = threading.Thread(target=handle_client, args=(data, addr))
    # thread.start()
    handle_client(data,addr)