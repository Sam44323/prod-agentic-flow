import sqlite3


def execute_query(query: str) -> str:
    """
    Execute a read-only SQL query.
    """

    connection = sqlite3.connect("data/information.db")

    cursor = connection.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    connection.close()

    return str(rows)
