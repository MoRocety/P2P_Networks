import socket, threading, sys, ast, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QInputDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal
from authenticate import createSignInDialog
from math import ceil

host = '127.0.0.1'
central_server_port = 55555

class Message:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        
class ChatWindow(QMainWindow):
    update_messages_signal = pyqtSignal()

    def __init__(self, username, server_socket_, listener_port, messages_db):
        super().__init__()
        self.break_threads = False
        self.username = username
        self.chosen_username = None
        self.server_socket = server_socket_
        self.listener_port = listener_port
        self.connections = {}
        self.message_logs = {user: [Message(msg["sender"], msg["receiver"], msg["message"]) for msg in msgs] for user, msgs in messages_db.items()}
        self.to_close = []

        self.initUI()

        self.update_messages_signal.connect(self.update_messages)

    def initUI(self):
        self.setWindowTitle(f"Chat - {self.username}")

        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)

        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Enter your message here...")

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(lambda: self.send_message(False))

        self.file_button = QPushButton("File Transfer", self)
        self.file_button.clicked.connect(lambda: self.send_message(True))

        self.server_button = QPushButton("Connect to Peer", self)
        self.server_button.clicked.connect(self.connect_to_server)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_area)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.file_button)
        layout.addWidget(self.server_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    def send_message(self, file_flag):
        if self.connections[self.chosen_username]:
            if file_flag:
                file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Send")
                if file_path:
                    file_size = os.path.getsize(file_path)
                    file_name = os.path.basename(file_path)
                    chunk_size = 1024
                    chunks = ceil(file_size / chunk_size)

                    header = f"/file {file_name} {file_size} {chunks}".encode()
                    self.connections[self.chosen_username].send(header)

                    with open(file_path, 'rb') as file:
                        while True:
                            chunk = file.read(chunk_size)
                            if not chunk:
                                break
                            self.connections[self.chosen_username].send(chunk)

                    self.chat_area.append(f"You sent a file: {file_name}")

            else:
                message = self.message_input.text()
                self.message_input.clear()
                self.connections[self.chosen_username].send(f"{self.username}: {message}".encode())

                if self.chosen_username in self.message_logs:
                    self.message_logs[self.chosen_username].append(Message(self.username, self.chosen_username, message))
                else:
                    self.message_logs[self.chosen_username] = [Message(self.username, self.chosen_username, message)]

                self.update_messages_signal.emit()
                self.server_socket.send(f"/db {self.username},{self.chosen_username}".encode())
                self.server_socket.send(message.encode())
        else:
            self.chat_area.append("Not connected to anyone yet.")

    def connect_to_server(self):
        self.server_socket.send("/server".encode())
        data = ast.literal_eval(self.server_socket.recv(1024).decode())
        other_listener_ports = {x: data[x] for x in data if data[x] != self.listener_port}

        if other_listener_ports:
            self.chosen_username, chosen_port = self.select_peer(other_listener_ports)
            if self.chosen_username:
                self.chat_area.append(f"Connecting to {self.chosen_username} on port {chosen_port}...")
                self.update_messages_signal.emit()
            
                if self.chosen_username not in self.connections:
                    self.connections[self.chosen_username] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.connections[self.chosen_username].connect((host, chosen_port))
                    self.connections[self.chosen_username].send(self.username.encode())

                    receive_thread = threading.Thread(target=self.receive_messages, args=(self.connections[self.chosen_username],))
                    receive_thread.start()

            else:
                self.chat_area.append("No peer selected.")
        else:
            self.chat_area.append("No other peers available.")

    def select_peer(self, peers):
        peer_list = list(peers.keys())
        chosen_username, ok = QInputDialog.getItem(self, "Select Peer", "Choose a peer to connect to:", peer_list, 0, False)
        if ok and chosen_username:
            return chosen_username, peers[chosen_username]
        return None, None

    def receive_messages(self, p2p_conn):
        self.to_close.append(p2p_conn)

        while True:
            try:
                data = p2p_conn.recv(1024).decode()

                if data.split(" ")[0] == "/file":
                    file_name = data.split(" ")[1]
                    file_chunks = int(data.split(" ")[3])
                    file_data = b''
                    for _ in range(file_chunks):
                        file_data += p2p_conn.recv(1024)

                    save_path, _ = QFileDialog.getSaveFileName(self, "Save File As", file_name)

                    if save_path:
                        with open(save_path, 'wb') as file:
                            file.write(file_data)
                        self.chat_area.append(f"Received file saved as: {save_path}")
                else:
                    sender = data.split(" ")[0][:-1]
                    message = " ".join(data.split(" ")[1:]).strip()

                    if sender in self.message_logs:
                        self.message_logs[sender].append(Message(sender, self.username, message))
                    else:
                        self.message_logs[sender] = [Message(sender, self.username, message)]

                
                    self.update_messages_signal.emit()

            except:
                print("Connection closed.")
                break
                
    def listener_handler(self, listener_socket):
        listener_socket.listen(3)

        while True:
            if self.break_threads:
                break
            
            p2p_conn, _ = listener_socket.accept()
            con_username = p2p_conn.recv(1024).decode()

            if con_username != "/close":
                self.connections[con_username] = p2p_conn
                receive_thread = threading.Thread(target=self.receive_messages, args=(p2p_conn,))
                receive_thread.start()

    def update_messages(self):
        self.chat_area.clear()
        if self.chosen_username in self.message_logs:
            for message in self.message_logs[self.chosen_username]:
                if message.sender == self.username and message.receiver == self.chosen_username:
                    self.chat_area.append(f"You: {message.message}")
                elif message.receiver == self.username and message.sender == self.chosen_username:
                    self.chat_area.append(f"{message.sender}: {message.message}")

    def closeEvent(self, event):
        self.break_threads = True
        self.server_socket.send(f"/signout {self.username}".encode())

        #Terminate the listener thread
        dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dummy_socket.connect((host, self.listener_port))
        dummy_socket.send("/close".encode())
        dummy_socket.close()

        # Terminate the receiver threads
        for connection in self.to_close:
            connection.close()

        sys.exit()

def main():
    # Client to Server connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, central_server_port))

    # Client to Client hole
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind((host, 0))
    _, listener_port = listener_socket.getsockname()

    app = QApplication(sys.argv)
    signInDialog = createSignInDialog(client_socket, listener_port)
    signInDialog.show()
    app.exec_()
    
    data = client_socket.recv(1024).decode()

    if data != "/successnt":
        data = data.split("|||")
        username = data[0]

    else:
        username = None

    if username:
        # Launch Chat Window
        message_db = data[1]
        message_db = ast.literal_eval(message_db)
        chat_window = ChatWindow(username, client_socket, listener_port, message_db)

        # Start listener thread
        listener_thread = threading.Thread(target=chat_window.listener_handler, args=(listener_socket,))
        listener_thread.start()
    else:
        print("Invalid username or password.")

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()