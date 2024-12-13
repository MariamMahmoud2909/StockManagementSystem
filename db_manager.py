import pyodbc

class DBManager:
    
    def __init__(self, server, database):
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};DATABASE={database};"
                f"Trusted_Connection=yes;"
            )
            self.cursor = self.connection.cursor()
            print("Database connection established successfully.")
            self.create_tables()
            self.create_table_orders()
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
        except pyodbc.Error as e:
            print(f"Error closing connection: {e}")

    def create_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            if not exists (select * from sys.tables WHERE name = 'Products')
            begin
                CREATE TABLE Products (
                product_id INT identity PRIMARY KEY,
                name NVARCHAR(50) not null,
                price DECIMAL(10, 2) not null,
                quantity INT default 0,
                threshold DECIMAL(10, 2) default 50
            );
            end
        """)
            self.connection.commit()  
             
    def create_table_orders(self):
        with self.connection.cursor() as cursor:    
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Orders')
            BEGIN
                CREATE TABLE Orders (
                    order_id INT PRIMARY KEY IDENTITY(1,1),
                    user_id INT,
                    product_id INT NOT NULL,
                    quantity INT DEFAULT 1,
                    total_price DECIMAL(10, 2),
                    order_date DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (product_id) REFERENCES Products(product_id)
                );
            END;
            """)
            
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.sequences WHERE name = 'UserIdSequence')
            BEGIN
                CREATE SEQUENCE UserIdSequence
                AS INT
                START WITH 1
                INCREMENT BY 1;
            END;
            """)

            self.connection.commit()
            
    def create_user(self):
        with self.connection.cursor() as cursor:    
            cursor.execute("""
            
                CREATE TRIGGER SetUserId
                ON Orders
                AFTER INSERT
                AS
                BEGIN
                    UPDATE Orders
                    SET user_id = NEXT VALUE FOR UserIdSequence
                    WHERE user_id IS NULL;
                END;
            """)

            self.connection.commit()



