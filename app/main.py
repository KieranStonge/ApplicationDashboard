from database import get_connection
from app_logic import run_app

def main():
    conn = get_connection()
    try:
        run_app(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
