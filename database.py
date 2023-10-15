import sqlite3

def setup_database():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    
    # Create a table to store transactions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        tx_hash TEXT PRIMARY KEY,
        from_address TEXT,
        to_address TEXT,
        value REAL,
        gas_spent INTEGER,
        fees_paid REAL
    )
    ''')
    conn.commit()
    conn.close()

def insert_transaction(tx):
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO transactions (tx_hash, from_address, to_address, value, gas_spent, fees_paid)
    VALUES (?, ?, ?, ?, ?,?)
    ''', (tx['tx_hash'], tx['from_address'], tx['to_address'], float(tx['value']), tx['gas_spent'], float(tx['fees_paid'])))
    
    conn.commit()
    conn.close()

def fetch_and_store_transactions():
    transactions = fetch_transactions()
    for tx in transactions['data']['items']:
        insert_transaction(tx)

def transaction_exists(tx_hash):
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT 1 FROM transactions WHERE tx_hash = ?', (tx_hash,))
    exists = cursor.fetchone()
    
    conn.close()
    return exists is not None


if __name__ == "__main__":
    setup_database()
