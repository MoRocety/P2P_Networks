import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

# Function to drop (delete) the database file
def drop_database():
    if os.path.exists('chat_system.db'):
        os.remove('chat_system.db')
        print("Database dropped successfully.")
    else:
        print("Database file not found.")

inp = int(input("Do we drop the db (0 for No, 1 for Yes): "))

if inp == 1:
    drop_database()

# Create an engine to connect to your database
engine = create_engine('sqlite:///chat_system.db', echo=False)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define your database schema by defining classes
class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)

class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    message = Column(String)

class UserChat(Base):
    __tablename__ = 'user_chats'
    sender_username = Column(String, ForeignKey('users.username'), primary_key=True)
    receiver_username = Column(String, ForeignKey('users.username'), primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.message_id'), primary_key=True)

    sender = relationship('User', foreign_keys=[sender_username])
    receiver = relationship('User', foreign_keys=[receiver_username])
    message = relationship('Message')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Function to sign up a new user
def signup(username, password):
    new_user = User(username=username, password=password)
    session.add(new_user)
    try:
        session.commit()
        print("User signed up successfully.")
    except IntegrityError:
        session.rollback()
        print("Username already exists. Please choose another username.")

# Function to sign in a user
def signin(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        print("Sign in successful.")
    else:
        print("Invalid username or password.")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    signInDialog = createSignInDialog()
    signInDialog.show()
    sys.exit(app.exec_())
