# encryption_hybrid.py

import os
import zipfile
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from datetime import datetime


def hybrid_encrypt(file_name, output_name, public_key_path="public_key/public_key.pem"):
    # Generate a random AES key
    aes_key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the file using AES
    with open(file_name, "rb") as f:
        plaintext = f.read()
        ct = encryptor.update(plaintext) + encryptor.finalize()

    # Encrypt the AES key using RSA
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    # Store the encrypted AES key, IV, and encrypted data together
    with open(output_name, "wb") as f:
        for data in (encrypted_aes_key, iv, ct):
            f.write(data)


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))


if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    items_to_encrypt = [f for f in os.listdir() if f not in [script_name, "public_key.pem", "encrypt.bat"]]

    print("Archiving files and directories...")
    with zipfile.ZipFile('files.zip', 'w') as zipf:
        for item in items_to_encrypt:
            if os.path.isfile(item):
                zipf.write(item)
                print(f"Added file {item} to archive")
            elif os.path.isdir(item):
                zipdir(item, zipf)
                print(f"Added directory {item} to archive")

    # Add datetime prefix to the encrypted file's name
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    encrypted_file_name = f"ORBARCH_{current_datetime}.zip.enc"

    print(f"Encrypting archive as {encrypted_file_name}...")
    hybrid_encrypt("files.zip", encrypted_file_name)

    # Cleanup
    for item in items_to_encrypt:
        if os.path.isfile(item):
            os.remove(item)
            print(f"Deleted file {item}")
        elif os.path.isdir(item):
            for root, dirs, files in os.walk(item, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                    print(f"Deleted file {os.path.join(root, name)}")
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
                    print(f"Deleted directory {os.path.join(root, name)}")
            os.rmdir(item)
            print(f"Deleted directory {item}")
    os.remove("files.zip")

    print("Files encrypted successfully!")
