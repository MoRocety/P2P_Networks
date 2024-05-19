import socket, threading, sys, ast
from PyQt5.QtWidgets import QApplication, QDialog
from authenticate import createSignInDialog

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
def send_messages(username, server_socket_, listener_port):
    socket_ = None

    while True:
        message = input("Enter your message: ")

        if message.split(" ")[0] == "/server":
            socket_ = server_socket_
            socket_.send("/server".encode())
            data = ast.literal_eval(socket_.recv(1024).decode())
            other_listener_ports = {x:data[x] for x in data if data[x] != listener_port}

            if other_listener_ports:
                print(other_listener_ports)
                chosen_username = input("Pick your poison: ")
                chosen_port = other_listener_ports[chosen_username]
                print("Connecting to port:", chosen_port)

                if chosen_username in connections:
                    socket_ = connections[chosen_username]
                
                else:
                    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_.connect((host, chosen_port))
                    connections[chosen_username] = socket_

                server_thread = threading.Thread(target=receive_messages, args=(socket_,))
                server_thread.start()

            else:
                print("No other peers available.")
        
        else:
            if socket_ is not None:
                socket_.send(message.encode())

            else:
                print("Not connected to anyone yet.")


def listener_handler(username, listener_socket):
    listener_socket.listen(3)
    print("Waiting for connections...")

    while True:
        p2p_conn, _ = listener_socket.accept()
        connections[username] = p2p_conn

        # Send and receive here via p2p_conn
        receive_thread = threading.Thread(target=receive_messages, args=(p2p_conn, ))
        receive_thread.start()
    
def main():
    # Client to Server connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, central_server_port))

    # Client to Client hole
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind((host, 0))
    _, listener_port = listener_socket.getsockname()

    app = QApplication(sys.argv)
    signInDialog = createSignInDialog(client_socket, listener_socket, listener_port)
    signInDialog.show()
    app.exec_()

    username = client_socket.recv(1024).decode()

    if username:
        print("Sign in successful.")

        # Receive and process other listener port numbers
        send_thread = threading.Thread(target=send_messages, args=(username, client_socket, listener_port,))
        send_thread.start()

        # So it does not block the server communication but still sets up listener
        listener_thread = threading.Thread(target=listener_handler, args=(username, listener_socket,))
        listener_thread.start()
        listener_thread.join()

    else:
        print("Invalid username or password.")
        

if __name__ == "__main__":
    main()
    

