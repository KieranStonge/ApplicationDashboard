from database import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        stage TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database Intialized")

if __name__ == "__main__":
    main()