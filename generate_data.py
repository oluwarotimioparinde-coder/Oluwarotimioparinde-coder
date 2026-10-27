import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

# Initialize Faker for realistic data generation
fake = Faker()
Faker.seed(42)
random.seed(42)

DB_NAME = "company_data.db"

def init_database():
    """Connects to SQLite and builds the entry-level relational schema."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"⚙️ Initializing database: {DB_NAME}...")
    
    # 1. Create Employees Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department TEXT,
            hire_date DATE
        )
    ''')
    
    # 2. Create Sales Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            product_name TEXT NOT NULL,
            sale_amount REAL NOT NULL,
            sale_date DATE,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def populate_mock_data():
    """Generates and safely injects synthetic records into the database."""
    conn = sqlite3.connect(DB_NAME)
    
    departments = ['Sales', 'Marketing', 'Engineering', 'Success']
    products = ['Cloud Analytics Pro', 'Data Core API', 'SaaS Dashboard Engine', 'Enterprise Security Suite']
    
    # Generate 15 Fake Employees
    employees_data = []
    for _ in range(15):
        hire_date = fake.date_between(start_date='-3y', end_date='today')
        employees_data.append((
            fake.first_name(),
            fake.last_name(),
            random.choice(departments),
            hire_date
        ))
        
    df_emp = pd.DataFrame(employees_data, columns=['first_name', 'last_name', 'department', 'hire_date'])
    df_emp.to_sql('employees', conn, if_exists='append', index=False)
    
    # Generate 100 Fake Sales Records mapping back to employees
    sales_data = []
    start_date = datetime.now() - timedelta(days=365)
    
    for _ in range(100):
        sale_date = fake.date_between(start_date=start_date, end_date='today')
        sales_data.append((
            random.randint(1, 15), # Links to employee_id 1-15
            random.choice(products),
            round(random.uniform(150.0, 2500.0), 2),
            sale_date
        ))
        
    df_sales = pd.DataFrame(sales_data, columns=['employee_id', 'product_name', 'sale_amount', 'sale_date'])
    df_sales.to_sql('sales', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print("✅ Successfully generated 15 employees and 100 sales performance records!")

if __name__ == "__main__":
    init_database()
    populate_mock_data()
