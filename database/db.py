import sqlite3
from datetime import datetime

conn = sqlite3.connect("kontakt.db")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        tag TEXT,
        image TEXT,
        created_at TEXT
    )
    """)
    conn.commit()

def add_contact(name, phone, email, tag, image):
    cursor.execute(
        "INSERT INTO contacts (name, phone, email, tag, image, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (name, phone, email, tag, image, datetime.now().isoformat())
    )
    conn.commit()

def get_contacts(filter_text="", tag_filter="All", sort_option="Newest"):
    query = "SELECT * FROM contacts WHERE 1=1"
    params = []

    if filter_text:
        query += " AND (name LIKE ? OR phone LIKE ? OR email LIKE ?)"
        params.extend([f"%{filter_text}%"] * 3)

    if tag_filter != "All":
        query += " AND tag=?"
        params.append(tag_filter)

    if sort_option == "A-Z":
        query += " ORDER BY name ASC"
    elif sort_option == "Z-A":
        query += " ORDER BY name DESC"
    else:
        query += " ORDER BY datetime(created_at) DESC"

    cursor.execute(query, params)
    return cursor.fetchall()

def delete_contact(contact_id):
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()

def update_contact(contact_id, name, phone, email, tag, image):
    cursor.execute("""
    UPDATE contacts SET name=?, phone=?, email=?, tag=?, image=? WHERE id=?
    """, (name, phone, email, tag, image, contact_id))
    conn.commit()

def is_duplicate(phone, email):
    cursor.execute("""
    SELECT * FROM contacts WHERE phone=? OR email=?
    """, (phone, email))
    return cursor.fetchone() is not None