import hashlib
import sqlite3
from pathlib import Path

from cryptography.fernet import Fernet

from config import DATABASE_PATH, KEY_FILE


# ==========================================
# Master Password Hashing
# ==========================================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ==========================================
# Master Password
# ==========================================

def master_password_exists():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM settings"
    )

    result = cursor.fetchone()[0]

    connection.close()

    return result > 0


def create_master_password(password):

    hashed_password = hash_password(password)

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO settings
        (id, master_password)
        VALUES (1, ?)
        """,
        (hashed_password,)
    )

    connection.commit()
    connection.close()


def verify_master_password(password):

    hashed_password = hash_password(password)

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT master_password
        FROM settings
        WHERE id = 1
        """
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return False

    return hashed_password == result[0]


# ==========================================
# Encryption Key
# ==========================================

def generate_encryption_key():

    key_path = Path(KEY_FILE)

    key_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not key_path.exists():

        key = Fernet.generate_key()

        with open(
            key_path,
            "wb"
        ) as file:

            file.write(key)


def load_encryption_key():

    key_path = Path(KEY_FILE)

    if not key_path.exists():

        generate_encryption_key()

    with open(
        key_path,
        "rb"
    ) as file:

        return file.read()


# ==========================================
# Encrypt Password
# ==========================================

def encrypt_password(password):

    key = load_encryption_key()

    cipher = Fernet(key)

    encrypted_password = cipher.encrypt(
        password.encode()
    )

    return encrypted_password.decode()


# ==========================================
# Decrypt Password
# ==========================================

def decrypt_password(encrypted_password):

    key = load_encryption_key()

    cipher = Fernet(key)

    decrypted_password = cipher.decrypt(
        encrypted_password.encode()
    )

    return decrypted_password.decode()