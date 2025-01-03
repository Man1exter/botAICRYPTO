#!/bin/bash

# Function to log messages
log_message() {
    local message=$1
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $message"
}

# Check if the secret key file exists
if [ ! -f "secret.key" ]; then
    log_message "Generating encryption key..."
    python3 -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); open('secret.key', 'wb').write(key)"
    if [ $? -eq 0 ]; then
        log_message "Encryption key generated and saved to secret.key"
    else
        log_message "Error generating encryption key"
        exit 1
    fi
else
    log_message "Encryption key already exists."
fi

# Check if the configuration file exists
if [ ! -f "config.json" ]; then
    log_message "Configuration file config.json not found!"
    exit 1
fi

# Encrypt the configuration file
log_message "Encrypting configuration file..."
python3 -c "
import json
from security import save_secure_config

try:
    with open('config.json', 'r') as file:
        config = json.load(file)
    save_secure_config(config, 'secure_config.enc')
    print('Configuration file encrypted and saved to secure_config.enc')
except Exception as e:
    print(f'Error encrypting configuration file: {e}')
    exit(1)
"
if [ $? -eq 0 ]; then
    log_message "Configuration file encrypted and saved to secure_config.enc"
else
    log_message "Error encrypting configuration file"
    exit 1
fi

# Remove the plain configuration file
rm config.json
if [ $? -eq 0 ]; then
    log_message "Plain configuration file config.json removed for security."
else
    log_message "Error removing plain configuration file"
    exit 1
fi

# Function to decrypt the configuration file
decrypt_config() {
    log_message "Decrypting configuration file..."
    python3 -c "
import json
from security import load_secure_config, save_sensitive_data

try:
    config = load_secure_config('secure_config.enc')
    save_sensitive_data(config, 'config.json')
    print('Configuration file decrypted and saved to config.json')
except Exception as e:
    print(f'Error decrypting configuration file: {e}')
    exit(1)
"
    if [ $? -eq 0 ]; then
        log_message "Configuration file decrypted and saved to config.json"
    else
        log_message "Error decrypting configuration file"
        exit 1
    fi
}

# Check if the user wants to decrypt the configuration file
read -p "Do you want to decrypt the configuration file? (y/n): " choice
if [ "$choice" = "y" ]; then
    decrypt_config
fi
