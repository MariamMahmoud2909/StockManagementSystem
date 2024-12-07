import pyodbc
class db_config:
    
    def connect_db():
        connection = pyodbc.connect(
            "DRIVER={{ODBC Driver 17 for SQL Server}};"
            "SERVER=DESKTOP-9UUO4AR;"
            "DATABASE=StockManagement;"
            "Trusted_Connection=yes;"
        )
        return connection
"""
def execute_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results"""