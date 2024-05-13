import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget
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

header_style = 'font: 22pt "Exo"; font-weight: bold;'
bg_color = '#181E30'
fg_color = '#EEEEEE'
fg_color1 = '#000000'
button_color = '#FFD700'
font_style = 'font: 12pt "Andante"; font-weight: bold;'
font_style1 = 'font: 18pt "Exo"; font-weight: bold;'

rounded_button_style = (
    f"background-color: {button_color}; color: {fg_color1}; {font_style}"
    "border-radius: 20px;"
    "padding: 10px 20px;"
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Authenticate")
        self.setGeometry(0, 0, 325, 300)
        self.setFixedSize(self.size())

        # Set the background color for the entire window
        self.setStyleSheet(f"background-color: {bg_color};")
        self.init_ui()

        self.result_window = None

    def init_ui(self):
        layout = QVBoxLayout()

        lw_l1 = QLabel("WELCOME USER")
        lw_l1.setStyleSheet(f"color: {fg_color}; {header_style}")
        lw_l1.setAlignment(Qt.AlignCenter)
        layout.addWidget(lw_l1, alignment=Qt.AlignCenter)

        placeholders = ["Username", "Password"]
        self.entry_boxes = []

        for p in placeholders:
            entry_box = QLineEdit()
            entry_box_style = (
                f"background-color: {fg_color}; color: {fg_color1}; {font_style}"
                "border-radius: 15px;"
                "padding: 5px;"
            )
            entry_box.setStyleSheet(entry_box_style)
            entry_box.setPlaceholderText(f"{p}...")
            layout.addWidget(entry_box, alignment=Qt.AlignCenter)
            self.entry_boxes.append(entry_box)

        buttons = QHBoxLayout()

        sigin = QPushButton("Sign In")
        sigin.setStyleSheet(rounded_button_style)
        sigin.clicked.connect(self.signin_clicked)  # Connect Sign In button
        buttons.addWidget(sigin, alignment=Qt.AlignCenter)

        signup = QPushButton("Sign Up")
        signup.setStyleSheet(rounded_button_style)
        signup.clicked.connect(self.signup_clicked)  # Connect Sign Up button
        buttons.addWidget(signup, alignment=Qt.AlignCenter)

        layout.addLayout(buttons)  # Add buttons layout to main layout

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def signin_clicked(self):
        username = self.entry_boxes[0].text()
        password = self.entry_boxes[1].text()
        if username and password:
            signin(username, password)
            self.clear_input_boxes()  # Clear input boxes after sign-in attempt
        else:
            print("Please enter both username and password.")

    def signup_clicked(self):
        username = self.entry_boxes[0].text()
        password = self.entry_boxes[1].text()
        if username and password:
            signup(username, password)
            self.clear_input_boxes()  # Clear input boxes after sign-up attempt
        else:
            print("Please enter both username and password.")

    def clear_input_boxes(self):
        for entry_box in self.entry_boxes:
            entry_box.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
