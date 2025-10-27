# database.py
import sqlite3


def setup_database() -> sqlite3.Connection:
    """
    Creates a SQLite database and populates it with
    four tables: employees, customers, products, and sales.
    """
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    # --- Table 1: Employees ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS employees
                   (
                       id            INTEGER PRIMARY KEY,
                       employee_name TEXT NOT NULL,
                       department    TEXT NOT NULL
                   );
                   """)

    # --- Table 2: Customers ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS customers
                   (
                       id     INTEGER PRIMARY KEY,
                       name   TEXT NOT NULL,
                       region TEXT NOT NULL
                   );
                   """)

    # --- Table 3: Products ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS products
                   (
                       id       INTEGER PRIMARY KEY,
                       name     TEXT NOT NULL,
                       category TEXT NOT NULL
                   );
                   """)

    # --- Table 4: Sales ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS sales
                   (
                       id          INTEGER PRIMARY KEY,
                       product_id  INTEGER,
                       customer_id INTEGER,
                       employee_id INTEGER,
                       amount      REAL,
                       name        TEXT,
                       FOREIGN KEY (product_id) REFERENCES products (id),
                       FOREIGN KEY (customer_id) REFERENCES customers (id),
                       FOREIGN KEY (employee_id) REFERENCES employees (id)
                   );
                   """)

    # --- Table 5: Queries, this table helps with query tracking
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries
                (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    result TEXT
                );
    """)
    # --- Populate Data ---

    cursor.executemany(
        "INSERT OR IGNORE INTO employees (id, employee_name, department) VALUES (?, ?, ?)",
        [
            (1, "Alice Smith", "Sales"),
            (2, "Bob Johnson", "Sales"),
            (3, "Charlie Lee", "Support"),
        ],
    )

    cursor.executemany(
        "INSERT OR IGNORE INTO customers (id, name, region) VALUES (?, ?, ?)",
        [
            (1, "BigCorp Inc.", "North"),
            (2, "SmallBiz LLC", "South"),
            (3, "TechStartup", "West"),
        ],
    )

    cursor.executemany(
        "INSERT OR IGNORE INTO products (id, name, category) VALUES (?, ?, ?)",
        [
            (1, "Laptop", "electronics"),
            (2, "Mouse", "electronics"),
            (3, "Coffee Mug", "kitchen"),
            (4, "Python Book", "books"),
            (5, "Keyboard", "electronics"),
            (6, "Blender", "kitchen"),
            (7, "SQL for Dummies", "books"),
        ],
    )

    cursor.executemany(
        "INSERT OR IGNORE INTO sales (product_id, customer_id, employee_id, amount, name) VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1, 1, 1200.00, "Corporate Deal"),
            (1, 3, 1, 1300.00, "Black Friday"),
            (2, 2, 2, 49.99, "Accessory Sale"),
            (3, 1, 3, 15.50, "Gift Shop Sale"),
            (1, 2, 1, 1150.50, "Online Sale"),
            (2, 3, 2, 55.00, "Online Sale"),
            (5, 1, 1, 150.00, "Corporate Deal"),
            (7, 3, 2, 35.00, "Student Sale"),
            (6, 2, 1, 89.90, "Home Goods Sale"),
        ],
    )

    conn.commit()
    return conn
