import sqlite3
import pandas as pd
import os

CSV_PATH = os.path.join("data", "products_clean.csv")
DB_PATH = os.path.join("database", "shopper.db")

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            brand TEXT,
            price REAL,
            rating REAL,
            review_summary TEXT,
            availability TEXT,
            image_url TEXT,
            product_link TEXT
        )
    """)
    conn.commit()
    print("Database and table created successfully.")
    return conn

def load_csv_to_db(conn):
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at {CSV_PATH}.")
        return
    df = pd.read_csv(CSV_PATH)
    df.to_sql("products", conn, if_exists="replace", index=False)
    print(f"Inserted {len(df)} rows into the products table.")

if __name__ == "__main__":
    connection = create_database()
    load_csv_to_db(connection)
    connection.close()