import sqlite3

from config import DATABASE_PATH
from security import (
    encrypt_password,
    decrypt_password
)


# ==========================================
# Connect to Database
# ==========================================

def connect_database():
    return sqlite3.connect(DATABASE_PATH)


# ==========================================
# Create Tables
# ==========================================

def create_tables():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            master_password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# Add Credential
# ==========================================

def add_credential(website, username, password):

    encrypted_password = encrypt_password(password)

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO credentials
        (website, username, password)
        VALUES (?, ?, ?)
    """, (
        website,
        username,
        encrypted_password
    ))

    connection.commit()
    connection.close()


# ==========================================
# Get Credentials
# ==========================================

def get_credentials():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, website, username, password, created_at
        FROM credentials
        ORDER BY id
    """)

    credentials = cursor.fetchall()

    connection.close()

    decrypted_credentials = []

    for credential in credentials:

        decrypted_password = decrypt_password(
            credential[3]
        )

        decrypted_credentials.append((
            credential[0],
            credential[1],
            credential[2],
            decrypted_password,
            credential[4]
        ))

    return decrypted_credentials


# ==========================================
# Search Credentials
# ==========================================

def search_credentials(search_term):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, website, username, password, created_at
        FROM credentials
        WHERE website LIKE ?
        ORDER BY id
    """, (
        f"%{search_term}%",
    ))

    credentials = cursor.fetchall()

    connection.close()

    decrypted_credentials = []

    for credential in credentials:

        decrypted_password = decrypt_password(
            credential[3]
        )

        decrypted_credentials.append((
            credential[0],
            credential[1],
            credential[2],
            decrypted_password,
            credential[4]
        ))

    return decrypted_credentials


# ==========================================
# Update Credential
# ==========================================

def update_credential(
    credential_id,
    website,
    username,
    password
):

    encrypted_password = encrypt_password(password)

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE credentials
        SET website = ?,
            username = ?,
            password = ?
        WHERE id = ?
    """, (
        website,
        username,
        encrypted_password,
        credential_id
    ))

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


# ==========================================
# Delete Credential
# ==========================================

def delete_credential(credential_id):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM credentials
        WHERE id = ?
    """, (
        credential_id,
    ))

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted