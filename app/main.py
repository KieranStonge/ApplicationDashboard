from database import get_connection

STAGE_MAP = {
    "1": "Applied",
    "2": "Interview",
    "3": "In Review",
    "4": "Rejected",
    "5": "Offer",
}


def init_db(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        stage TEXT NOT NULL
    )
    """)

def prompt_application():
    company = input("Company: ").strip()
    role = input("Role: ").strip()

    print("\nStage:")
    for key, value in STAGE_MAP.items():
        print(f"{key}. {value}")

    stage_choice = input("Choose stage (1-5): ").strip()
    stage = STAGE_MAP.get(stage_choice)

    if not company or not role:
        print("Company and role are required.\n")
        return None

    if stage is None:
        print("Invalid stage selection.\n")
        return None

    return company, role, stage

def add_application(cursor, company, role, stage):
    cursor.execute(
        "INSERT INTO applications (company, role, stage) VALUES (?, ?, ?)",
        (company, role, stage)
    )

def fetch_applications(cursor):
    cursor.execute("SELECT id, company, role, stage FROM applications ORDER BY id DESC")
    return cursor.fetchall()

def fetch_stage_summary(cursor):
    cursor.execute("""
        SELECT stage, COUNT(*) AS count
        FROM applications
        GROUP BY stage
        ORDER BY count DESC
    """)
    return cursor.fetchall()

def print_table(rows):
    if not rows:
        print("No applications found.\n")
        return

    headers = ("ID", "Company", "Role", "Stage")
    str_rows = [(str(r[0]), r[1], r[2], r[3]) for r in rows]

    widths = [
        max(len(headers[0]), max(len(r[0]) for r in str_rows)),
        max(len(headers[1]), max(len(r[1]) for r in str_rows)),
        max(len(headers[2]), max(len(r[2]) for r in str_rows)),
        max(len(headers[3]), max(len(r[3]) for r in str_rows)),
    ]

    fmt = f"{{:<{widths[0]}}}  {{:<{widths[1]}}}  {{:<{widths[2]}}}  {{:<{widths[3]}}}"
    print(fmt.format(*headers))
    print("-" * (sum(widths) + 6))

    for r in str_rows:
        print(fmt.format(*r))

    print()

def print_stage_summary(rows):
    if not rows:
        return

    print("Stage summary:")
    for stage, count in rows:
        print(f"{stage}: {count}")
    print()

def main():
    conn = get_connection()
    cursor = conn.cursor()
    init_db(cursor)
    conn.commit()

    print("Application Dashboard\n")

    while True:
        data = prompt_application()
        if data is None:
            again = input("Try again? (y/n): ").strip().lower()
            if again != "y":
                break
            print()
            continue

        company, role, stage = data
        add_application(cursor, company, role, stage)
        conn.commit()

        print("\nSaved.\n")

        apps = fetch_applications(cursor)
        summary = fetch_stage_summary(cursor)

        print_table(apps)
        print_stage_summary(summary)

        again = input("Add another application? (y/n): ").strip().lower()
        print()
        if again != "y":
            break

    conn.close()
    print("Goodbye.")

if __name__ == "__main__":
    main()
