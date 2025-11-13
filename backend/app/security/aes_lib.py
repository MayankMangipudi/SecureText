from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

def generate_aes_key():
    """Generate a random 256-bit AES key"""
    key = os.urandom(32)  # 32 bytes = 256 bits
    return base64.b64encode(key).decode('utf-8')  # Return as base64 string

def aes_encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext using AES-256-CBC"""
    try:
        # Decode base64 key
        key_bytes = base64.b64decode(key)
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key_bytes),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        # Pad the plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        
        # Encrypt
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine IV and ciphertext, then base64 encode
        result = base64.b64encode(iv + ciphertext).decode('utf-8')
        return result
    except Exception as e:
        raise ValueError(f"Encryption failed: {str(e)}")

def aes_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using AES-256-CBC"""
    try:
        # Decode base64 key and ciphertext
        key_bytes = base64.b64decode(key)
        encrypted_data = base64.b64decode(ciphertext)
        
        # Extract IV (first 16 bytes) and ciphertext
        iv = encrypted_data[:16]
        actual_ciphertext = encrypted_data[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key_bytes),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        # Decrypt
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")
