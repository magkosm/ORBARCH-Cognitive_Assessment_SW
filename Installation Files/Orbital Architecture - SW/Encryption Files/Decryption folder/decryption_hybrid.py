# decryption_hybrid.py

import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def hybrid_decrypt(file_name, output_name, private_key_path="private_key.pem"):
    with open(file_name, "rb") as f:
        encrypted_aes_key = f.read(256)  # Assuming 2048-bit RSA key
        iv = f.read(16)
        ct = f.read()

    # Decrypt the AES key using RSA
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    # Decrypt the data using AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ct) + decryptor.finalize()

    with open(output_name, "wb") as f:
        f.write(plaintext)

if __name__ == "__main__":
    # Auto-detect the encrypted file
    encrypted_files = [f for f in os.listdir() if f.startswith("ORBARCH") and f.endswith(".enc")]

    if not encrypted_files:
        print("Error: No encrypted file starting with 'ORBARCH' and ending with '.enc' found!")
        exit(1)

    encrypted_file_name = encrypted_files[0]
    print(f"Found encrypted file: {encrypted_file_name}")

    print("Decrypting archive...")
    output_file_name = encrypted_file_name[:-4]  # Remove .enc extension
    hybrid_decrypt(encrypted_file_name, output_file_name)

    print(f"Decrypted file saved as: {output_file_name}")
