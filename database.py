import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

DATABASE_URL = 'sqlite:///chat_system.db'

# Function to drop (delete) the database file
def drop_database():
    if os.path.exists('chat_system.db'):
        os.remove('chat_system.db')
        print("Database dropped successfully.")
    else:
        print("Database file not found.")

if input("Enter Yes to drop the database: ") == "Yes":
    drop_database()

# Create an engine to connect to your database
engine = create_engine(DATABASE_URL, echo=False)

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
        return True
    
    except IntegrityError:
        session.rollback()
        return False

# Function to sign in a user
def signin(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    return True if user else False

def save_message(sender_username, receiver_username, message_text):
    new_message = Message(message=message_text)
    session.add(new_message)
    session.flush()  # Flush to get the message_id before committing

    user_chat = UserChat(
        sender_username=sender_username,
        receiver_username=receiver_username,
        message_id=new_message.message_id
    )

    session.add(user_chat)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    
def get_messages(username):
    messages_dict = {}
    
    # Query to get all messages where the given user is either the sender or receiver
    user_chats = session.query(UserChat).join(Message).filter(
        (UserChat.sender_username == username) | (UserChat.receiver_username == username)
    ).all()

    for user_chat in user_chats:
        other_username = user_chat.receiver_username if user_chat.sender_username == username else user_chat.sender_username
        
        if other_username not in messages_dict:
            messages_dict[other_username] = []
        
        message_info = {
            "sender": user_chat.sender_username,
            "receiver": user_chat.receiver_username,
            "message": user_chat.message.message
        }
        
        messages_dict[other_username].append(message_info)
    
    return messages_dict
