import sqlite3

def connect_db():
    return sqlite3.connect('customer_data.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        previous_reading INTEGER NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        customer_id INTEGER NOT NULL,
        bill_amount REAL NOT NULL,
        date TEXT NOT NULL,
        paid BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )''')

    conn.commit()
    conn.close()

def add_customer(name, address, previous_reading):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, address, previous_reading) VALUES (?, ?, ?)",
                   (name, address, previous_reading))
    conn.commit()
    conn.close()

def get_customer_by_id(customer_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def save_bill(customer_id, bill_amount, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bills (customer_id, bill_amount, date) VALUES (?, ?, ?)",
                   (customer_id, bill_amount, date))
    conn.commit()
    conn.close()

def get_bills_for_customer(customer_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bills WHERE customer_id = ?", (customer_id,))
    bills = cursor.fetchall()
    conn.close()
    return bills
