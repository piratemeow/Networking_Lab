import socket

HEADER = 64
PORT = 2007
SERVER = '10.33.2.90'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def receive(client):
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return msg


def receive_file(client):
    filename = receive(client)
    if filename=="File not found":
        print(filename)
        return
    file_size = int(receive(client))/(8*100000)
    file_data = b""
    print(f"{filename} download started...")
    while len(file_data) < file_size:
        chunk = client.recv(400096)
        if not chunk:
            break
        file_data += chunk
    with open(f"received_{filename}", 'wb') as file:
        file.write(file_data)
    print(f"received_{filename} Downloaded successfully. Downloaded size: {file_size}MB")


def send(client, message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


client = connect_to_server()
exit_message = receive(client)
options = receive(client)
while True:
    # Receive options from the server

    print("Available Options:\n", options)

    # Choose an option
    selected_option = input(f"Select an option Enter {exit_message} to exit: ")

    # Check if the user wants to exit
    if int(selected_option) >= int(exit_message):
        send(client, DISCONNECT_MESSAGE)
        break

    # Send the selected option to the server
    send(client, selected_option)
    receive_file(client)

    # Receive the file from the server if the selected option is valid

client.close()
