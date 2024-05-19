import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt
import qtawesome as qta

# Dictionary to store messages for each user
messages = {
    "username1": [],
    "username2": [],
    "username3": []
}

def createSignInDialog():
    dialog = QDialog()
    main_layout = QVBoxLayout(dialog)

    # Create a central widget
    central_widget = QWidget()
    central_layout = QVBoxLayout(central_widget)
    
    welcome_label = QLabel("Welcome to our App!")
    welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #EED3D9;")
    central_layout.addWidget(welcome_label, alignment=Qt.AlignCenter)

    # Add the central widget to the main layout
    main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    main_layout.addWidget(central_widget, alignment=Qt.AlignCenter)
    main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    username_edit = QLineEdit()
    username_edit.setFixedWidth(200)
    username_edit.setPlaceholderText("Username")
    central_layout.addWidget(username_edit, alignment=Qt.AlignCenter)


    password_edit = QLineEdit()
    password_edit.setEchoMode(QLineEdit.Password)
    password_edit.setFixedWidth(200)
    password_edit.setPlaceholderText("password")
    central_layout.addWidget(password_edit, alignment=Qt.AlignCenter)

    buttons_layout = QHBoxLayout()

    signin_button = QPushButton("Sign In")
    signin_button.setFixedWidth(100)
    signin_button.clicked.connect(dialog.accept)
    buttons_layout.addWidget(signin_button)

    signup_button = QPushButton("Sign Up")
    signup_button.setFixedWidth(100)
    signup_button.clicked.connect(dialog.accept)
    buttons_layout.addWidget(signup_button)

    central_layout.addLayout(buttons_layout)

    dialog.setStyleSheet("""
        QLabel {
            color: black;
            font-size: 14px;
            font-family: sans-serif;
            margin-bottom: auto;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid black;
            border-radius: 8px;
            font-size: 12px;
            margin-bottom: 16px;
        }
        QPushButton {
            padding: 8px;
            background-color: black;
            color: white;
            border-radius: 15px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: grey;
        }
        QDialog {
            background-color: white;
        }
    """)

    central_layout.setSpacing(8)
    dialog.setFixedSize(700, 500)
    dialog.setWindowTitle("Sign In Demo")

    return dialog

def createMessageDialog():
    dialog = QDialog()
    dialog.setFixedSize(700, 500)

    main_layout = QHBoxLayout(dialog)

    # Create the button area for the list of messages
    button_area_widget = QWidget()
    button_area_widget.setStyleSheet("""
        QWidget {
            background-color: #FAF3F0;
            border-radius: 16px;
        }
    """)
    button_area_layout = QVBoxLayout(button_area_widget)
    
    label = QLabel("Messages")
    button_area_layout.addWidget(label, alignment=Qt.AlignTop)
    
    users = ["username1", "username2", "username3"]  # Replace with actual usernames
    buttons = []
    for message in users:
        button = QPushButton(message)
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                text-align: left;
                padding-left: 16px;
                border: none;
                box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5);
            }
            QPushButton:hover{
                background-color: #F8F8FF;
            }
        """)
        button_area_layout.addWidget(button)
        button.setFixedWidth(200)
        button.clicked.connect(lambda _, name=message: set_username(name))  # Connect button click to set username
        buttons.append(button)

    main_layout.addWidget(button_area_widget, stretch=3)  # Increase the stretch factor to 3 for the button area

    # Create the right side layout
    right_side_layout = QVBoxLayout()
    right_side_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
    right_side_layout.setSpacing(0)  # Remove spacing
    
    # Display the initial username
    username_label = QLabel("Select user to chat with")
    username_label.setStyleSheet("font-size: 18px; font-weight: bold;")
    right_side_layout.addWidget(username_label)

    # Create a scroll area for the message display
    scroll_area = QScrollArea()
    scroll_area.setStyleSheet("border: none;")
    scroll_area_widget = QWidget()
    scroll_area_layout = QVBoxLayout(scroll_area_widget)
    scroll_area_layout.setAlignment(Qt.AlignTop)
    
    scroll_area.setWidget(scroll_area_widget)
    scroll_area.setWidgetResizable(True)
    
    right_side_layout.addWidget(scroll_area, stretch=7)

    # Create a QHBoxLayout for the message input field and buttons
    message_input_layout = QHBoxLayout()

    entermsg = QLineEdit()
    entermsg.setPlaceholderText("Enter message...")
    entermsg.setFixedHeight(40)  # Increased height of the input field
    entermsg.setFixedWidth(360)

    # Create two buttons with icons
    send_button = QPushButton()
    send_button.setIcon(qta.icon('fa.send'))
    send_button.setFixedWidth(40)
    send_button.setFixedHeight(40)
    
    cancel_button = QPushButton()
    cancel_button.setIcon(qta.icon('fa.paperclip'))
    cancel_button.setFixedWidth(40)
    cancel_button.setFixedHeight(40)

    # Add message input field and buttons to the QHBoxLayout
    message_input_layout.addWidget(entermsg)
    message_input_layout.addSpacing(6)  # Add space between the input field and buttons
    message_input_layout.addWidget(send_button)
    message_input_layout.addWidget(cancel_button)

    # Add the QHBoxLayout containing message input field and buttons to the right side layout
    right_side_layout.addLayout(message_input_layout)
    right_side_layout.setAlignment(message_input_layout, Qt.AlignBottom)  # Align to bottom
    main_layout.addLayout(right_side_layout, stretch=7)  # Add the right side layout to the main layout
    
    dialog.setStyleSheet("""
        QLabel {
            color: black;
            font-size: 14px;
            font-family: monospace;
        }
        QLineEdit {
            padding: 5px;
            background-color: #D4E2D4;
            border-radius: 8px;
            font-size: 12px;
        }
        QPushButton {
            padding: 8px;
            margin: 2px;
            background-color: white;
            border: 1px solid white;
            color: black;
            border-radius: 18px;
            font-size: 14px;
        }
        QDialog {
            background-color: white;
        }
    """)

    dialog.setWindowTitle("Messages")

    def clear_layout(layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def update_messages(username):
        clear_layout(scroll_area_layout)  # Clear the existing layout
        for message_text in messages.get(username, []):
            message_widget = QWidget()
            message_layout = QHBoxLayout(message_widget)
            message_label = QLabel(message_text)
            
            message_layout.addWidget(message_label)
            message_widget.setStyleSheet("""
                QWidget {
                    padding: 8px;
                    border-radius: 0;
                    border: none;
                }
            """)
            if username == "username1":
                message_layout.setAlignment(Qt.AlignRight)
                message_label.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;
                    padding: 8px;
                    font-size: 12px;
                    border-radius: 12px;
                }""")
            else:
                message_layout.setAlignment(Qt.AlignLeft)
                message_label.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;
                    padding: 8px;
                    font-size: 12px;
                    border-radius: 12px;
                }""")
            scroll_area_layout.addWidget(message_widget)
        scroll_area.setWidget(scroll_area_widget)

    def set_username(name):
        username_label.setText(name)
        update_messages(name)

    # Function to send a message
    def send_message():
        current_user = username_label.text()
        if current_user != "Select user to chat with":
            message = entermsg.text()
            if message:
                messages[current_user].append(message)
                entermsg.clear()
                update_messages(current_user)

    send_button.clicked.connect(send_message)

    return dialog

if __name__ == '__main__':
    app = QApplication(sys.argv)

    signInDialog = createSignInDialog()
    messageDialog = createMessageDialog()

    signInDialog.finished.connect(messageDialog.exec)

    signInDialog.show()
    sys.exit(app.exec_())
