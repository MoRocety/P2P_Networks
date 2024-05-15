import socket
import threading

listener_ports = {}

def receive_messages(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()

            if data == "/server":
                conn.send((str(listener_ports)).encode())

            else:
                username = data.split(",")[0]
                listener_port = int(data.split(",")[1])
                listener_ports[username] = listener_port                

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
