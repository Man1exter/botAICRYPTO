import os
import logging
from getpass import getpass
from cryptography.fernet import Fernet
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate a key and save it into a file
def generate_key():
    key = Fernet.generate_key()
    with open("system_secret.key", "wb") as key_file:
        key_file.write(key)
    logging.info("System encryption key generated and saved to system_secret.key")

# Function to load the key from the current directory named `system_secret.key`
def load_key():
    return open("system_secret.key", "rb").read()

# Function to encrypt a message
def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Function to decrypt an encrypted message
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Function to securely save user credentials to a file
def save_user_credentials(username, password):
    credentials = {
        "username": username,
        "password": encrypt_message(password)
    }
    with open("user_credentials.enc", "wb") as file:
        file.write(encrypt_message(json.dumps(credentials)))
    logging.info("User credentials saved securely")

# Function to load user credentials from a file
def load_user_credentials():
    with open("user_credentials.enc", "rb") as file:
        encrypted_data = file.read()
    decrypted_data = decrypt_message(encrypted_data)
    return json.loads(decrypted_data)

# Function to authenticate user
def authenticate_user():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    credentials = load_user_credentials()
    if username == credentials["username"] and password == decrypt_message(credentials["password"]):
        logging.info("User authenticated successfully")
    else:
        logging.error("Authentication failed")
        exit(1)

# Function to check if running in a secure environment
def check_secure_environment():
    if os.getenv("SECURE_ENV") != "true":
        logging.error("Not running in a secure environment. Set the SECURE_ENV environment variable to 'true'.")
        exit(1)

# Example usage
if __name__ == "__main__":
    # Check if running in a secure environment
    check_secure_environment()

    # Generate and save a key (only need to do this once)
    if not os.path.exists("system_secret.key"):
        generate_key()

    # Save user credentials (only need to do this once)
    if not os.path.exists("user_credentials.enc"):
        username = input("Set up a username: ")
        password = getpass("Set up a password: ")
        save_user_credentials(username, password)

    # Authenticate user
    authenticate_user()
