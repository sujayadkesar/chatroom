import socket
import threading

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 45454))


# listening to server and sending nicknames

def receive():
    while True:
        try:
            # Receive message from server
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # close connection because of error
            print("An error occured !! ")
            client.close()
            break

# sending messages to the server
def write():
    while True:
        message = '{}:{}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# Starting threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()