import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

def run_entire_system():
    print("⚙️ Building relational schema in browser memory...")

    # Create database inside your browser's RAM memory to bypass file errors
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department TEXT,
            hire_date DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            product_name TEXT NOT NULL,
            sale_amount REAL NOT NULL,
            sale_date DATE
        )
    ''')

    # Insert 15 Fake Employees
    departments = ['Sales', 'Marketing', 'Engineering', 'Success']
    employees_data = [(fake.first_name(), fake.last_name(), random.choice(departments), fake.date_between(start_date='-3y', end_date='today')) for _ in range(15)]
    pd.DataFrame(employees_data, columns=['first_name', 'last_name', 'department', 'hire_date']).to_sql('employees', conn, if_exists='append', index=False)

    # Insert 100 Fake Sales
    products = ['Cloud Analytics Pro', 'Data Core API', 'SaaS Dashboard Engine']
    sales_data = [(random.randint(1, 15), random.choice(products), round(random.uniform(150.0, 2500.0), 2), fake.date_between(start_date='-1y', end_date='today')) for _ in range(100)]
    pd.DataFrame(sales_data, columns=['employee_id', 'product_name', 'sale_amount', 'sale_date']).to_sql('sales', conn, if_exists='append', index=False)

    print("✅ Memory Database generated successfully!")
    print("🚀 Extracting and running analytics reporting...")

    df_employees = pd.read_sql_query("SELECT * FROM employees;", conn)
    df_sales = pd.read_sql_query("SELECT * FROM sales;", conn)

    # Merge data (SQL INNER JOIN equivalent)
    df_merged = pd.merge(df_sales, df_employees, on="employee_id", how="inner")

    total_revenue = df_merged["sale_amount"].sum()
    avg_sale = df_merged["sale_amount"].mean()

    # Print the Final Corporate Dashboard
    print("\n================ BUSINESS SUMMARY ================")
    print(f"💰 Total Enterprise Revenue:  ${total_revenue:,.2f}")
    print(f"📈 Average Transaction Value: ${avg_sale:,.2f}")
    print("==================================================\n")

    print("🏢 Performance Breakdown by Department:")
    dept_summary = df_merged.groupby("department")["sale_amount"].agg(['sum', 'count', 'mean'])
    dept_summary.columns = ['Total Sales', 'Deal Count', 'Avg Deal Size']

    print(dept_summary.to_string(formatters={
        'Total Sales': '${:,.2f}'.format,
        'Avg Deal Size': '${:,.2f}'.format
    }))

    conn.close()
    print("\n✅ Pipeline execution finished successfully!")

run_entire_system()
