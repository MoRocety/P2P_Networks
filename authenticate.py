from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from database import signin, signup

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
    password_edit.setPlaceholderText("Password")
    central_layout.addWidget(password_edit, alignment=Qt.AlignCenter)

    buttons_layout = QHBoxLayout()

    signin_button = QPushButton("Sign In")
    signin_button.setFixedWidth(100)
    signin_button.clicked.connect(lambda: signin_clicked(username_edit, password_edit))
    buttons_layout.addWidget(signin_button)

    signup_button = QPushButton("Sign Up")
    signup_button.setFixedWidth(100)
    signup_button.clicked.connect(lambda: signup_clicked(username_edit, password_edit))
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

def signin_clicked(username_edit, password_edit):
    username = username_edit.text()
    password = password_edit.text()
    if username and password:
        signin(username, password)
        clear_input_boxes([username_edit, password_edit])  # Clear input boxes after sign-in attempt
    else:
        print("Please enter both username and password.")

def signup_clicked(username_edit, password_edit):
    username = username_edit.text()
    password = password_edit.text()
    if username and password:
        signup(username, password)
        clear_input_boxes([username_edit, password_edit])  # Clear input boxes after sign-up attempt
    else:
        print("Please enter both username and password.")

def clear_input_boxes(entry_boxes):
    for entry_box in entry_boxes:
        entry_box.clear()
