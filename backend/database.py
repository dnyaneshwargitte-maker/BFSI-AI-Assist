"""
CloudifyOps BFSI Intelligence Platform - Database Connector
Connects directly to Local PostgreSQL (Port 5432/5433).
"""
import os
from typing import Dict, List, Optional, Any

# Load .env if present
env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "bfsi_db")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

class Database:
    def __init__(self):
        self.use_postgres = False
        self._test_connection()

    def _test_connection(self):
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                dbname=DB_NAME,
                connect_timeout=3
            )
            conn.close()
            self.use_postgres = True
            print(f"[OK] Database: Connected to Local PostgreSQL ({DB_HOST}:{DB_PORT}/{DB_NAME})")
        except Exception as e:
            self.use_postgres = False
            print(f"[!] Database: Local PostgreSQL connection failed ({e}).")

    def get_connection(self):
        if self.use_postgres:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            return psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                dbname=DB_NAME,
                cursor_factory=RealDictCursor
            )
        else:
            # Fallback connection if postgres not connected yet
            import sqlite3
            sqlite_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bfsi_local.db")
            conn = sqlite3.connect(sqlite_path)
            conn.row_factory = sqlite3.Row
            return conn

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            if not self.use_postgres:
                query = query.replace("%s", "?")
            cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            if not self.use_postgres:
                query = query.replace("%s", "?")
            cur.execute(query, params)
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> Any:
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            if not self.use_postgres:
                query = query.replace("%s", "?")
            cur.execute(query, params)
            conn.commit()
            return cur.lastrowid if hasattr(cur, "lastrowid") else None
        finally:
            conn.close()

    def health_check(self) -> str:
        """Return 'postgres' or 'sqlite' based on active backend."""
        try:
            conn = self.get_connection()
            conn.close()
            return "postgres" if self.use_postgres else "sqlite"
        except Exception as e:
            raise RuntimeError(f"DB unreachable: {e}")

db = Database()
