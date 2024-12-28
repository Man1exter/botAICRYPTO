<<<<<<< HEAD
# Security Guidelines

## Overview

This document provides security guidelines and instructions for securely handling sensitive data and configuration settings in the Trading Bot Dashboard project.

## Encryption

### Generating an Encryption Key

To securely store sensitive data, an encryption key must be generated. This key will be used to encrypt and decrypt the configuration file.

1. Run the `securize.sh` script to generate the encryption key and encrypt the configuration file:

```sh
bash securize.sh
```

### Encrypting the Configuration File

The `securize.sh` script will encrypt the `config.json` file and save the encrypted data to `secure_config.enc`. The plain `config.json` file will be removed for security.

### Decrypting the Configuration File

If you need to decrypt the configuration file, you can use the `decrypt_config` function in the `securize.sh` script:

```sh
bash securize.sh
```

When prompted, choose `y` to decrypt the configuration file.

## Secure Configuration Handling

### Loading Secure Configuration

The `security.py` module provides functions for securely loading configuration settings. The `load_secure_config` function is used to load the encrypted configuration file:

```python
from security import load_secure_config

config = load_secure_config('secure_config.enc')
```

### Saving Secure Configuration

The `security.py` module also provides functions for securely saving configuration settings. The `save_secure_config` function is used to save the configuration file in an encrypted format:

```python
from security import save_secure_config

config = {
    "api_key": "your_api_key",
    "api_secret": "your_api_secret"
}

save_secure_config(config, 'secure_config.enc')
```

## Secure API Key Management

### Storing API Keys

API keys and other sensitive data should be stored in the encrypted configuration file. Do not hard-code API keys directly in the source code.

### Loading API Keys

Load API keys from the encrypted configuration file using the `load_secure_config` function:

```python
config = load_secure_config('secure_config.enc')
api_key = config['api_key']
api_secret = config['api_secret']
```

## Best Practices

1. **Do not share the encryption key (`secret.key`) with unauthorized individuals.**
2. **Do not commit the plain `config.json` file to version control.**
3. **Regularly rotate API keys and update the encrypted configuration file.**
4. **Ensure that the `securize.sh` script is executed in a secure environment.**

## License

This project is licensed under the MIT License.
=======
# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a
reported vulnerability, what to expect if the vulnerability is accepted or
declined, etc.
>>>>>>> 7985d37d62f3bc0529ec613eeeb2eb1af2fe2975
