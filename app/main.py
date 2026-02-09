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

    company = input("Company: ")
    role = input("Role: ")
    stage = input("Stage (Applied / Interview / Rejected / Offer): ")

    cursor.execute("""
    INSERT INTO applications (company, role, stage)
    VALUES (?, ?, ?)
    """, (company, role, stage))

    conn.commit()

    cursor.execute("SELECT id, company, role, stage FROM applications")
    rows = cursor.fetchall()

    conn.close()

    print("\nApplications: ")
    for r in rows:
        print(r)

if __name__ == "__main__":
    main()