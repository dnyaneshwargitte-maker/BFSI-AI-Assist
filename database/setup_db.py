"""
============================================================================
CloudifyOps BFSI Intelligence Platform - Local PostgreSQL Setup Runner
Strictly targets Local PostgreSQL (the exact database used by pgAdmin).
============================================================================
"""
import os
import sys
import argparse
import getpass

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")
SEED_FILE = os.path.join(os.path.dirname(__file__), "seed.sql")

def run_local_postgres_setup(host="127.0.0.1", port=5432, user="postgres", password=None, dbname="bfsi_db"):
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    except ImportError:
        print("[!] Error: psycopg2 is required. Installing psycopg2-binary...")
        os.system(f"{sys.executable} -m pip install psycopg2-binary")
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    if not password:
        password = os.getenv("DB_PASSWORD")
        if not password:
            print(f"Connecting to Local PostgreSQL ({host}:{port}) as user '{user}'...")
            password = getpass.getpass(f"Enter password for local PostgreSQL user '{user}': ")

    ports_to_try = [port]
    # If 5432 fails, automatically try 5433 (PostgreSQL 13)
    if port == 5432:
        ports_to_try.append(5433)
    elif port == 5433:
        ports_to_try.append(5432)

    connected_port = None
    target_conn = None

    for p in ports_to_try:
        print(f"\n[*] Attempting connection to Local PostgreSQL on port {p}...")
        try:
            # Step 1: Connect to maintenance db 'postgres'
            conn = psycopg2.connect(
                host=host,
                port=p,
                user=user,
                password=password,
                dbname="postgres",
                connect_timeout=4
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            # Check or create target database
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
            if not cur.fetchone():
                print(f"[+] Creating database '{dbname}' in local PostgreSQL...")
                cur.execute(f'CREATE DATABASE "{dbname}" OWNER "{user}"')
                print(f"[+] Database '{dbname}' created successfully.")
            else:
                print(f"[+] Target database '{dbname}' already exists in local PostgreSQL.")
            
            cur.close()
            conn.close()
            connected_port = p
            break
        except Exception as e:
            err_str = str(e)
            if "password authentication failed" in err_str.lower():
                print(f"[!] Authentication Failed: Password for user '{user}' is incorrect.")
                return False
            elif "10013" in err_str or "connection refused" in err_str.lower() or "timeout" in err_str.lower():
                print(f"[-] Port {p} is not accepting connections (service might be stopped or on another port).")
            else:
                print(f"[-] Attempt on port {p} failed: {e}")

    if not connected_port:
        print("\n" + "="*65)
        print(" [!] ERROR: Could not connect to Local PostgreSQL.")
        print("="*65)
        print("Possible Reasons:")
        print(" 1. The PostgreSQL Windows Service is STOPPED.")
        print("    -> Fix: Press Win+R -> type 'services.msc' -> Right-click 'postgresql-x64-18' (or 13) -> click 'Start'.")
        print(" 2. The password entered was incorrect.")
        print("="*65)
        return False

    # Step 2: Connect to target database 'bfsi_db' and execute schema & seed
    print(f"\n[*] Connected to Local PostgreSQL on port {connected_port}!")
    print(f"[*] Applying 12-table schema from '{SCHEMA_FILE}' to '{dbname}'...")
    try:
        target_conn = psycopg2.connect(
            host=host,
            port=connected_port,
            user=user,
            password=password,
            dbname=dbname
        )
        cur = target_conn.cursor()

        # Read & Execute schema.sql
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cur.execute(schema_sql)
        target_conn.commit()
        print("[+] Schema created successfully in local PostgreSQL.")

        # Read & Execute seed.sql
        print(f"[*] Seeding 5 Indian Personas and 3 Demo Agents from '{SEED_FILE}'...")
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            seed_sql = f.read()
        cur.execute(seed_sql)
        target_conn.commit()
        print("[+] Seed data populated successfully.")

        # Save config into .env so backend uses this exact local PostgreSQL connection
        env_content = f"""# Local PostgreSQL Connection for pgAdmin and FastAPI Backend
DB_HOST={host}
DB_PORT={connected_port}
DB_USER={user}
DB_PASSWORD={password}
DB_NAME={dbname}
DATABASE_URL=postgresql://{user}:{password}@{host}:{connected_port}/{dbname}
"""
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"), "w", encoding="utf-8") as f:
            f.write(env_content)
        print("[+] Updated .env with local PostgreSQL credentials.")

        # Step 3: Print Table Verification Summary from Local PostgreSQL
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cur.fetchall()]

        print("\n" + "="*65)
        print(f" [SUCCESS] Local PostgreSQL '{dbname}' (Port {connected_port}) is Ready!")
        print("="*65)
        for t in tables:
            cur.execute(f'SELECT COUNT(*) FROM "{t}";')
            cnt = cur.fetchone()[0]
            print(f"  • Table: {t:<28} | Rows in Local PG: {cnt}")
        print("="*65)
        print("\n>> You can now open pgAdmin and view 'bfsi_db' directly with all tables and rows!")

        cur.close()
        target_conn.close()
        return True

    except Exception as e:
        print(f"[!] Error creating tables in local PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CloudifyOps BFSI Local PostgreSQL Initializer")
    parser.add_argument("--host", default="127.0.0.1", help="PostgreSQL Host (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5432, help="PostgreSQL Port (5432 or 5433)")
    parser.add_argument("--user", default="postgres", help="PostgreSQL User (default postgres)")
    parser.add_argument("--password", default=None, help="PostgreSQL Password")
    parser.add_argument("--dbname", default="bfsi_db", help="Target Database Name (default bfsi_db)")
    args = parser.parse_args()

    run_local_postgres_setup(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        dbname=args.dbname
    )
