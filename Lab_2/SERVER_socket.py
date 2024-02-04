import os.path
import socket
import threading

HEADER = 64
PORT = 2007
SERVER = '10.33.2.90'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# print(SERVER)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


# ... (existing code)
def send_file(filename, conn,addr):
    try:
        with open(filename, 'rb') as file:
            file_size = os.path.getsize(filename)
            file_data = file.read()
            send(f"received_{filename}", conn)
            send(str(file_size), conn)
            print(f"Sending {filename} to {addr}")
            conn.send(file_data)
            print(f"Successfully sent {filename} to {addr}")

    except FileNotFoundError:
        send("File not found", conn)


DOWNLOAD_OPTIONS = {
    '1': 'image1.jpg',
    '2': 'image2.jpg',
    '3': 'image3.jpeg',
    '4': 'video.mp4',
    '5': 'video1.mp4'
}


def send_options(conn):
    send(str(len(DOWNLOAD_OPTIONS)+1), conn)
    print("Sent size")
    options = "\n".join([f"{key}: {value}" for key, value in DOWNLOAD_OPTIONS.items()])
    send(options, conn)
    print("sent options")


# Modify the handle_client function
def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected")

    # Send the available options to the client
    send_options(conn)

    connected = True
    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            option = msg[0]
            if option in DOWNLOAD_OPTIONS:
                filename = DOWNLOAD_OPTIONS[option]
                print(f"{addr} requested to download: {filename}")
                send_file(filename, conn,addr)
            elif msg == DISCONNECT_MESSAGE:
                connected = False
                send("SERVER is disconnected", conn)
                print(f"[{addr}] {msg}")

    conn.close()

# ... (existing code)


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
