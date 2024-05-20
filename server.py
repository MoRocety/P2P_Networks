import socket
import threading
import database

listener_ports = {}

def receive_messages(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode().split(" ")

            if data[0] == "/server":
                conn.send((str(listener_ports)).encode())

            elif data[0] == "/signup":
                fields = data[1].split(",")
                username = fields[0]
                password = fields[1]

                success = str(database.signup(username, password))
                conn.send(success.encode())
                
            elif data[0] == "/signin":
                fields = data[1].split(",")
                username = fields[0]
                password = fields[1]

                success = database.signin(username, password)

                if success:
                    listener_port = int(fields[2])
                    listener_ports[username] = listener_port
                    conn.send(str(success).encode())
                    messages = database.get_messages(username)
                    conn.send(f"{username}|||{messages}".encode())
                
            elif data[0] == "/db":
                names = data[1].split(",")
                sender = names[0]
                receiver = names[1]

                message = conn.recv(1024).decode()
                database.save_message(sender, receiver, message)

            print(data, listener_ports)

        except ConnectionResetError:
            print("Connection with", addr, "reset by peer.")
            break

def handle_client(conn, addr):
    print("Connection from:", addr)
    receive_thread = threading.Thread(target=receive_messages, args=(conn, addr))
    receive_thread.start()

def main():
    host = '127.0.0.1'
    port = 55555
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(4)
    print("Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
