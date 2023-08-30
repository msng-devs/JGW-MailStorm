import logging
import os
import sqlite3
from sqlite3 import Cursor, Connection

from src.core.template import parse
from src.helpers.path import get_absolute_path

db_file_path = get_absolute_path(['data', 'data.db'])
template_file_path = get_absolute_path(['data', 'template'])


def refresh_template_list() -> bool:
    #get file list
    files = find_all_filenames(template_file_path)

    if files is None or len(files) == 0:
        logging.error("Failed refresh template list. template file is not found")
        return False

    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    #delete all template
    try:
        delete_all(conn, cursor)

    except Exception as e:
        logging.error(f"Failed delete all template. error : {str(e)}")
        conn.rollback()
        conn.close()
        return False

    #create template
    for file in files:
        logging.info(f"Create template: {file}")
        try:
            args = parse(get_absolute_path(["data", "template", file + ".html"]))
            create(conn, cursor, file, args)

        except Exception as e:
            logging.error(f"In refresh template list, Failed create template: {file} error: {str(e)}")
            conn.rollback()
            conn.close()
            return False

    conn.close()
    logging.info("Success refresh template list")
    return True


def find_all_filenames(directory):
    try:
        filename_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                filename = os.path.basename(file)
                file_format = filename.split(".")[1].strip()
                if file_format == "html":
                    filename_list.append(filename.split(".")[0].strip())

    except Exception as e:
        logging.error("Failed to find all filenames")
        return None

    return filename_list


def delete_all(conn: Connection, cursor: Cursor):
    cursor.execute("DELETE FROM template")
    conn.commit()


def create(conn: Connection, cursor: Cursor, name: str, arg: str):
    cursor.execute("INSERT INTO template (name, arg) VALUES (?, ?)", (name, arg))
    conn.commit()


def get(name: str):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    row = None
    try:
        cursor.execute("SELECT * FROM template WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.commit()

    except Exception as e:
        logging.error(f"Failed get template: {name} error: {str(e)}")
        conn.rollback()

    conn.close()
    return row
