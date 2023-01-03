import socket
import threading


# connection data
hostname = socket.gethostname()
get_host_ip = socket.gethostbyname(hostname)

print(f"[*] Connection id : {get_host_ip}")

host = get_host_ip
port = 443

# starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists for clients and theri nicknames
clients = []
nicknames = []


# sending messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling messages from clients

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # Accept connection

        client, address = server.accept()
        print(f"[*] Connection established with {address}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
