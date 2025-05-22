import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

clients = {}
usernames = {}

def broadcast(message, exclude=None):
    for client in clients:
        if client != exclude:
            try:
                client.sendall(message)
            except:
                client.close()

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()
        usernames[client_socket] = username
        clients[client_socket] = client_socket
        update_user_list()

        while True:
            msg = client_socket.recv(4096)
            if not msg:
                break
            broadcast(msg, exclude=client_socket)
    except:
        pass
    finally:
        if client_socket in clients:
            clients.pop(client_socket)
        if client_socket in usernames:
            usernames.pop(client_socket)
        update_user_list()
        client_socket.close()

def update_user_list():
    user_list = "|USERLIST|" + ",".join(usernames.values())
    broadcast(user_list.encode())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[+] Server listening on port {PORT}")
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()
