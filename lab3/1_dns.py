import socket
import threading
host = '10.33.2.90'

port = 2403


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))


print("SERVER STARTED")

def handle_client(data,addr):
    print(addr)
    data = data.split()
    requested_name = data[0]
    requested_type = data[1]

    print(requested_name,requested_type)

    file1 = open("servers.txt","r")

    for line in file1:
        line = line.split()
        name = line[0]
        value = line[1]
        type = line[2]
        ttl = line[3]
        if requested_name==name and (requested_type=="A" or requested_type=="AAAA"):
            print(value)
            return
    re = rec(requested_name,file1,requested_type)
    if re == None:
        print("does not exist")
    print(re)

    for line in file1:
        line = line.split()
        name = line[0]
        value = line[1]
        type = line[2]
        ttl = line[3]
        # print(name)
        ip_value = None
        if name==requested_name:
            if type=="NS" or type=="CNAME":
                requested_name = value
                for line in file1:
                    line = line.split()
                    name = line[0]
                    value = line[1]
                    type = line[2]
                    if requested_name== name:
                        ip_value = value

            elif type == "A" or type=="AAAA":
                ip_value = value




    if ip_value != None:
        print("Returning the ip value ",value)
        s.sendto(bytes(value,'utf-8'),addr)
        return

    else:
        print("No value found")
        s.sendto(bytes("Not found ",'utf-8'),addr)
        return


def rec (requested_name,file1,type):

    if(type=="A" or type=="AAAA"):
        for line in file1:
            line = line.split()
            name = line[0]
            value = line[1]
            type = line[2]
            ttl = line[3]
            if requested_name==name:
                return value
        # return requested_name

    for line in file1:
        line = line.split()
        name = line[0]
        value = line[1]
        type = line[2]
        ttl = line[3]
        if requested_name==name:
            rec(value,file1,type)
    return None



def handle_client(data,addr):
    data = data.split()

    requested_name = data[0]
    requested_type = data[1]

    file1 = open("servers.txt","r")

    container = file1.readlines()
    for i in range(len(container)):
        container[i] = container[i].split()
    
    for line in container:
        if (line[0]==requested_name):
            requested_type = line[1]

    return 
    

# def re(requested_name):
#     if ()


while True:
    data,addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    thread = threading.Thread(target=handle_client,args=(data,addr))
    thread.start()