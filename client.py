import socket
import threading
import ast

host = '127.0.0.1'
central_server_port = 55555

def receive_messages(p2p_conn):
    while True:
        data = p2p_conn.recv(1024).decode()
        if not data:
            break
        print("Received message:", data)

def send_messages(p2p_conn):
    while True:
        message = input("Enter your message: ")
        p2p_conn.send(message.encode())

def server_communication(client_socket, listener_port):
    client_socket.send(str(listener_port).encode())
    data = client_socket.recv(1024).decode()
    other_listener_ports = ast.literal_eval(data)

    print(other_listener_ports)
    
    if other_listener_ports:
        chosen_port = other_listener_ports[int(input("Pick your poison: "))]  # Choosing the first available port for simplicity
        print("Connecting to port:", chosen_port)
        
        p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p2p_socket.connect((host, chosen_port))
        
        receive_thread = threading.Thread(target=receive_messages, args=(p2p_socket,))
        send_thread = threading.Thread(target=send_messages, args=(p2p_socket,))
        
        receive_thread.start()
        send_thread.start()
        
        receive_thread.join()
        send_thread.join()
    else:
        print("No other peers available.")

def listener_handler(listener_socket):
    listener_socket.listen(1)
    p2p_conn, _ = listener_socket.accept()
    
    # send and receive here via p2p_conn
    receive_thread = threading.Thread(target=receive_messages, args=(p2p_conn, ))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(p2p_conn, ))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    
def main():
    # Client to server connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, central_server_port))

    # Client to Client hole
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind((host, 0))
    _, listener_port = listener_socket.getsockname()

    # So it does not block the server communication but still sets up listener
    listener_thread = threading.Thread(target=listener_handler, args=(listener_socket, ))
    listener_thread.start()

    server_thread = threading.Thread(target=server_communication, args=(client_socket, listener_port,))
    server_thread.start()

    listener_thread.join()
    server_thread.join()
    
    client_socket.close()

if __name__ == "__main__":
    main()
