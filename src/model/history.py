import json
import sqlite3
from datetime import datetime

from src.helpers.json_convert import Result
from src.helpers.path import get_absolute_path

db_file_path = get_absolute_path(['data', 'data.db'])


def create(result: Result):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        query = "INSERT INTO history (run_date, service, recipient, subject, template, arg, status, message) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), result.service, result.recipient, result.subject,
            result.template, result.to_arg_json().replace("\n",""),
            str(result.status),
            result.message))
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e
    conn.close()


def get_all(limit: int):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT run_date, service , status , template , subject, recipient ,arg, message, id FROM history ORDER BY run_date desc LIMIT ?",
            (limit,))
        rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()
        return None
    conn.close()
    return rows

def get_by_id(id:int):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id,run_date, service , status , template , subject, recipient ,arg, message FROM history WHERE id = ?",
            (id,))
        rows = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()
        return None
    conn.close()
    return rows