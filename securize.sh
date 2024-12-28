#!/bin/bash

# Check if the secret key file exists
if [ ! -f "secret.key" ]; then
    echo "Generating encryption key..."
    python3 -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); open('secret.key', 'wb').write(key)"
    echo "Encryption key generated and saved to secret.key"
else
    echo "Encryption key already exists."
fi

# Check if the configuration file exists
if [ ! -f "config.json" ]; then
    echo "Configuration file config.json not found!"
    exit 1
fi

# Encrypt the configuration file
echo "Encrypting configuration file..."
python3 -c "
import json
from security import save_secure_config

with open('config.json', 'r') as file:
    config = json.load(file)

save_secure_config(config, 'secure_config.enc')
"
echo "Configuration file encrypted and saved to secure_config.enc"

# Remove the plain configuration file
rm config.json
echo "Plain configuration file config.json removed for security."

# Function to decrypt the configuration file
decrypt_config() {
    echo "Decrypting configuration file..."
    python3 -c "
import json
from security import load_secure_config, save_sensitive_data

config = load_secure_config('secure_config.enc')
save_sensitive_data(config, 'config.json')
"
    echo "Configuration file decrypted and saved to config.json"
}

# Check if the user wants to decrypt the configuration file
read -p "Do you want to decrypt the configuration file? (y/n): " choice
if [ "$choice" = "y" ]; then
    decrypt_config
fi
