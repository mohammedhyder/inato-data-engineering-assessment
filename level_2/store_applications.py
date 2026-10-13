
import json
import os
from pathlib import Path

import mysql.connector


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "processed"


def main():
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="inato",
    )

    try:
        cursor = connection.cursor()

        insert_sql = """
            INSERT INTO application
            (id, therapeutic_area, created_at, site_name, site_category)
            VALUES (%s, %s, %s, %s, %s)
        """

        files = sorted(PROCESSED_DIR.glob("application-*.json"))

        if not files:
            raise FileNotFoundError(
                f"No JSON files found in {PROCESSED_DIR}. Complete Step 1 first."
            )

        rows = []

        for file_path in files:
            with file_path.open(encoding="utf-8") as file:
                app = json.load(file)

            rows.append(
                (
                    app["id"],
                    app["therapeutic_area"],
                    app["created_at"],
                    app["site"]["name"],
                    app["site"]["category"],
                )
            )

        cursor.executemany(insert_sql, rows)
        connection.commit()

        print(f"Successfully inserted {cursor.rowcount} applications.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()