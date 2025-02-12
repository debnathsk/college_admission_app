# app/database.py

import sqlite3
from sqlite3 import Error

DATABASE = "college_admission.db"

def create_connection(db_file: str = DATABASE) -> sqlite3.Connection:
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, SQLite version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_table(conn: sqlite3.Connection) -> None:
    """Create a table to store student records."""
    try:
        sql_create_students_table = """ CREATE TABLE IF NOT EXISTS students (
                                            id integer PRIMARY KEY,
                                            student_id text NOT NULL,
                                            name text NOT NULL,
                                            age integer NOT NULL,
                                            gender text NOT NULL,
                                            marks text NOT NULL,  # Store 6 subjects as JSON
                                            qualification_exam text NOT NULL,
                                            desired_course text NOT NULL,
                                            eligibility_status text NOT NULL,
                                            timestamp text NOT NULL
                                        ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_students_table)
        conn.commit()
        print("Table 'students' created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")

def initialize_database() -> None:
    """Initialize the database and create tables."""
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    initialize_database()