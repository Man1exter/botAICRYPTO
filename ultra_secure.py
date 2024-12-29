import os
import json
import pyotp
import logging
from cryptography.fernet import Fernet
from getpass import getpass

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate a key and save it into a file
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    logging.info("Encryption key generated and saved to secret.key")

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
    logging.info(f"Sensitive data saved to {filename}")

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

# Function to generate a TOTP secret and save it to a file
def generate_totp_secret():
    secret = pyotp.random_base32()
    with open("totp_secret.key", "w") as file:
        file.write(secret)
    logging.info(f"TOTP secret generated and saved to totp_secret.key. Use this secret to set up your authenticator app: {secret}")

# Function to load the TOTP secret from a file
def load_totp_secret():
    return open("totp_secret.key", "r").read()

# Function to verify TOTP code
def verify_totp_code(code):
    secret = load_totp_secret()
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

# Function to perform multi-factor authentication
def perform_mfa():
    code = getpass("Enter the TOTP code from your authenticator app: ")
    if verify_totp_code(code):
        logging.info("MFA successful.")
    else:
        logging.error("Invalid TOTP code. MFA failed.")
        exit(1)

# Function to check if running in a secure environment
def check_secure_environment():
    if os.getenv("SECURE_ENV") != "true":
        logging.error("Not running in a secure environment. Set the SECURE_ENV environment variable to 'true'.")
        exit(1)

# Function to validate environment variables
def validate_environment_variables(required_vars):
    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)

# Function to log sensitive data access
def log_sensitive_data_access(action, filename):
    logging.info(f"{action} sensitive data in {filename}")

# Example usage
if __name__ == "__main__":
    # Check if running in a secure environment
    check_secure_environment()

    # Validate required environment variables
    required_vars = ["SECURE_ENV", "API_KEY", "API_SECRET"]
    validate_environment_variables(required_vars)

    # Perform multi-factor authentication
    perform_mfa()

    # Generate and save a key (only need to do this once)
    if not os.path.exists("secret.key"):
        generate_key()

    # Generate and save a TOTP secret (only need to do this once)
    if not os.path.exists("totp_secret.key"):
        generate_totp_secret()

    # Example sensitive data
    sensitive_data = {
        "api_key": os.getenv("API_KEY"),
        "api_secret": os.getenv("API_SECRET")
    }

    # Save sensitive data to a file
    save_sensitive_data(sensitive_data, "sensitive_data.enc")
    log_sensitive_data_access("Saved", "sensitive_data.enc")

    # Load sensitive data from a file
    loaded_data = load_sensitive_data("sensitive_data.enc")
    logging.info(f"Loaded sensitive data: {loaded_data}")
    log_sensitive_data_access("Loaded", "sensitive_data.enc")

    # Load configuration settings securely
    config = load_secure_config("sensitive_data.enc")
    logging.info(f"Loaded configuration: {config}")
    log_sensitive_data_access("Loaded", "secure_config.enc")

    # Save configuration settings securely
    save_secure_config(config, "secure_config.enc")
    log_sensitive_data_access("Saved", "secure_config.enc")
