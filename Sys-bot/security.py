from cryptography.fernet import Fernet
import os
import json

# Function to generate a key and save it into a file
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key from the current directory named `secret.key`
def load_key():
    return open("secret.key", "rb").read()

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

# Function to securely save sensitive data to a file
def save_sensitive_data(data, filename):
    encrypted_data = encrypt_message(json.dumps(data))
    with open(filename, "wb") as file:
        file.write(encrypted_data)

# Function to securely load sensitive data from a file
def load_sensitive_data(filename):
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = decrypt_message(encrypted_data)
    return json.loads(decrypted_data)

# Function to securely load configuration settings
def load_secure_config(filename):
    config = load_sensitive_data(filename)
    return config

# Function to securely save configuration settings
def save_secure_config(config, filename):
    save_sensitive_data(config, filename)

# Example usage
if __name__ == "__main__":
    # Generate and save a key (only need to do this once)
    if not os.path.exists("secret.key"):
        generate_key()

    # Example sensitive data
    sensitive_data = {
        "api_key": "your_api_key",
        "api_secret": "your_api_secret"
    }

    # Save sensitive data to a file
    save_sensitive_data(sensitive_data, "sensitive_data.enc")

    # Load sensitive data from a file
    loaded_data = load_sensitive_data("sensitive_data.enc")
    print(loaded_data)

    # Load configuration settings securely
    config = load_secure_config("sensitive_data.enc")
    print(config)

    # Save configuration settings securely
    save_secure_config(config, "secure_config.enc")
