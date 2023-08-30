import logging
import sqlite3

from src.helpers.path import get_absolute_path

db_file_path = get_absolute_path(['data', 'data.db'])


def init_db():
    con = sqlite3.connect(db_file_path)
    cursor = con.cursor()
    try:
        # history 테이블
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
        table_exists = cursor.fetchone()

        if not table_exists:
            logging.info("Table is not Found. Init history table")
            cursor.execute('''CREATE TABLE history (
                                id INTEGER PRIMARY KEY,
                                run_date TEXT,
                                service TEXT,
                                recipient TEXT,
                                subject TEXT,
                                template TEXT,
                                arg TEXT,
                                status TEXT,
                                message TEXT
                            );''')
            con.commit()

        # template 테이블
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='template'")
        table_exists = cursor.fetchone()

        if not table_exists:
            logging.info("Table is not Found. Init template table")
            cursor.execute('''CREATE TABLE template (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                arg TEXT
                            );''')
            cursor.execute('CREATE INDEX idx_template_name ON template(name);')
            con.commit()
    except Exception as e:
        logging.error("Failed init database. error: " + str(e))
        con.rollback()
        con.close()
        exit(1)
    finally:
        con.close()
