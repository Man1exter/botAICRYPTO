#!/bin/bash

# Function to check if running in a secure environment
check_secure_environment() {
    if [ "$SECURE_ENV" != "true" ]; then
        echo "Error: Not running in a secure environment. Set the SECURE_ENV environment variable to 'true'."
        exit 1
    fi
}

# Function to generate an encryption key
generate_key() {
    if [ ! -f "system_secret.key" ]; then
        echo "Generating encryption key..."
        python3 -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); open('system_secret.key', 'wb').write(key)"
        echo "Encryption key generated and saved to system_secret.key"
    else
        echo "Encryption key already exists."
    fi
}

# Function to encrypt a file
encrypt_file() {
    local filename=$1
    if [ -f "$filename" ]; then
        echo "Encrypting $filename..."
        python3 -c "
import json
from cryptography.fernet import Fernet

def load_key():
    return open('system_secret.key', 'rb').read()

def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(message.encode())

with open('$filename', 'r') as file:
    data = file.read()

encrypted_data = encrypt_message(data)

with open('${filename}.enc', 'wb') as file:
    file.write(encrypted_data)
"
        echo "$filename encrypted and saved as ${filename}.enc"
    else
        echo "Error: $filename not found."
    fi
}

# Function to decrypt a file
decrypt_file() {
    local filename=$1
    if [ -f "$filename" ]; then
        echo "Decrypting $filename..."
        python3 -c "
from cryptography.fernet import Fernet

def load_key():
    return open('system_secret.key', 'rb').read()

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

with open('$filename', 'rb') as file:
    encrypted_data = file.read()

decrypted_data = decrypt_message(encrypted_data)

with open('${filename%.enc}', 'w') as file:
    file.write(decrypted_data)
"
        echo "$filename decrypted and saved as ${filename%.enc}"
    else
        echo "Error: $filename not found."
    fi
}

# Function to securely delete a file
secure_delete() {
    local filename=$1
    if [ -f "$filename" ]; then
        echo "Securely deleting $filename..."
        shred -u "$filename"
        echo "$filename securely deleted."
    else
        echo "Error: $filename not found."
    fi
}

# Function to backup a file
backup_file() {
    local filename=$1
    if [ -f "$filename" ]; then
        local backup_filename="${filename}.bak"
        cp "$filename" "$backup_filename"
        echo "$filename backed up as $backup_filename"
    else
        echo "Error: $filename not found."
    fi
}

# Function to restore a file from backup
restore_file() {
    local backup_filename=$1
    if [ -f "$backup_filename" ]; then
        local original_filename="${backup_filename%.bak}"
        cp "$backup_filename" "$original_filename"
        echo "$backup_filename restored as $original_filename"
    else
        echo "Error: $backup_filename not found."
    fi
}

# Function to monitor system resources
monitor_system() {
    echo "Monitoring system resources..."
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'
    echo "Memory Usage:"
    free -h
    echo "Disk Usage:"
    df -h
}

# Function to add a new user
add_user() {
    local username=$1
    local password=$2
    sudo useradd -m "$username"
    echo "$username:$password" | sudo chpasswd
    echo "User $username added successfully."
}

# Function to delete a user
delete_user() {
    local username=$1
    sudo userdel -r "$username"
    echo "User $username deleted successfully."
}

# Example usage
if [ "$1" == "check_secure_environment" ]; then
    check_secure_environment
elif [ "$1" == "generate_key" ]; then
    generate_key
elif [ "$1" == "encrypt_file" ]; then
    encrypt_file "$2"
elif [ "$1" == "decrypt_file" ]; then
    decrypt_file "$2"
elif [ "$1" == "secure_delete" ]; then
    secure_delete "$2"
elif [ "$1" == "backup_file" ]; then
    backup_file "$2"
elif [ "$1" == "restore_file" ]; then
    restore_file "$2"
elif [ "$1" == "monitor_system" ]; then
    monitor_system
elif [ "$1" == "add_user" ]; then
    add_user "$2" "$3"
elif [ "$1" == "delete_user" ]; then
    delete_user "$2"
else
    echo "Usage: $0 {check_secure_environment|generate_key|encrypt_file|decrypt_file|secure_delete|backup_file|restore_file|monitor_system|add_user|delete_user} [filename|username] [password]"
fi
