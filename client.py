import socket
import threading
import ast

host = '127.0.0.1'
central_server_port = 55555
connections = {}

# Only receives from the p2p connection
def receive_messages(p2p_conn):
    while True:
        data = p2p_conn.recv(1024).decode()
        if not data:
            break
        
        print("Received message:", data)

# Only sends to the p2p connection unless the user wants to send to the server, calls server_communication in that case
def send_messages(username, client_socket, listener_port, p2p_conn):
    while True:
        message = input("Enter your message: ")
        if message.split(" ")[0] == "/server":
            server_thread = threading.Thread(target=server_communication, args=(username, client_socket, listener_port,))
            server_thread.start()
            server_thread.join()
        
        else:
            p2p_conn.send(message.encode())

# Sets up a p2p connection with another client whenever called
def server_communication(username, client_socket, listener_port):
    # Send listener port number
    client_socket.send(f"{username},{listener_port}".encode())

    # Receive and process other listener port numbers
    data = ast.literal_eval(client_socket.recv(1024).decode())
    other_listener_ports = {x:data[x] for x in data if data[x] != listener_port}

    print(other_listener_ports)
    
    if other_listener_ports:
        chosen_username = input("Pick your poison: ")
        chosen_port = other_listener_ports[chosen_username]
        print("Connecting to port:", chosen_port)

        if chosen_username in connections:
            p2p_socket = connections[chosen_username]
        
        else:
            p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p2p_socket.connect((host, chosen_port))
            connections[chosen_username] = p2p_socket
        
        receive_thread = threading.Thread(target=receive_messages, args=(p2p_socket,))
        send_thread = threading.Thread(target=send_messages, args=(username, client_socket, listener_port, p2p_socket,))
        
        receive_thread.start()
        send_thread.start()
        
        receive_thread.join()
        send_thread.join()
    else:
        print("No other peers available.")

def listener_handler(username, client_socket, listener_port, listener_socket):
    # changes need to be made here to listen for multiple connections, implement similar architecture to what server had for this, use a list and a /username mechanism to communicate with desired connection
    listener_socket.listen(2)
    print("Waiting for connections...")

    while True:
        p2p_conn, _ = listener_socket.accept()
        connections[username] = p2p_conn

        # Listener should add that connection to connections list but not immediately switch to that connection, maybe not start a new sending thread?

        # Send and receive here via p2p_conn
        receive_thread = threading.Thread(target=receive_messages, args=(p2p_conn, ))
        receive_thread.start()

    
def main():
    # Client to server connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, central_server_port))

    # Client to Client hole
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind((host, 0))
    _, listener_port = listener_socket.getsockname()

    username = input("Enter your username: ")

    # So it does not block the server communication but still sets up listener
    listener_thread = threading.Thread(target=listener_handler, args=(username, client_socket, listener_port, listener_socket, ))
    listener_thread.start()

    server_thread = threading.Thread(target=server_communication, args=(username, client_socket, listener_port,))
    server_thread.start()

    listener_thread.join()
    server_thread.join()
    
    client_socket.close()

if __name__ == "__main__":
    main()
