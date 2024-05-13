import socket
import threading

client_connections = []

def receive_messages(conn, addr):
    print("rec called")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Received message from", addr, ":", data)

def send_messages():
    while True:
        message = input("Enter message: ")
        print("send called")
        for conn in client_connections:
            print(len(client_connections))
            conn.send(message.encode())

def handle_client(conn, addr):
    print("Connection from:", addr)
    client_connections.append(conn)
    receive_thread = threading.Thread(target=receive_messages, args=(conn, addr))
    receive_thread.start()

def main():
    host = '127.0.0.1'
    port = 55555
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)  # Listen for up to 2 connections
    print("Waiting for connections...")

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
