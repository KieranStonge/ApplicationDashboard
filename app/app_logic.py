from app.stages import STAGE_MAP
from app.display import print_table, print_stage_summary

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

def run_app(conn):
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

    print("Goodbye.")
