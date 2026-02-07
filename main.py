# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
SELECT 
    e.firstName,
    e.lastName,
    e.jobTitle
FROM employees e
INNER JOIN offices o
    ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT 
    o.officeCode,
    o.city,
    o.country,
    COUNT(e.employeeNumber) as employee_count
FROM offices o
LEFT JOIN employees e
    ON o.officeCode = e.officeCode
GROUP BY o.officeCode, o.city, o.country
HAVING COUNT(e.employeeNumber) = 0
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT 
    e.firstName,
    e.lastName,
    o.city,
    o.state
FROM employees e
LEFT JOIN offices o
    ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT 
    c.contactFirstName,
    c.contactLastName,
    c.phone,
    c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o
    ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT 
    c.contactFirstName,
    c.contactLastName,
    p.amount,
    p.paymentDate
FROM customers c
INNER JOIN payments p
    ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
SELECT 
    e.employeeNumber,
    e.firstName,
    e.lastName,
    COUNT(c.customerNumber) as number_of_customers
FROM employees e
INNER JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY number_of_customers DESC
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT 
    p.productName,
    COUNT(DISTINCT od.orderNumber) as numorders,
    SUM(od.quantityOrdered) as totalunits
FROM products p
INNER JOIN orderdetails od
    ON p.productCode = od.productCode
GROUP BY p.productName
ORDER BY totalunits DESC
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT 
    p.productName,
    p.productCode,
    COUNT(DISTINCT o.customerNumber) as numpurchasers
FROM products p
INNER JOIN orderdetails od
    ON p.productCode = od.productCode
INNER JOIN orders o
    ON od.orderNumber = o.orderNumber
GROUP BY p.productName, p.productCode
ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT 
    o.officeCode,
    o.city,
    COUNT(c.customerNumber) as n_customers
FROM offices o
INNER JOIN employees e
    ON o.officeCode = e.officeCode
INNER JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY n_customers DESC
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
SELECT DISTINCT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    o.city,
    o.officeCode
FROM employees e
INNER JOIN offices o
    ON e.officeCode = o.officeCode
INNER JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
INNER JOIN orders ord
    ON c.customerNumber = ord.customerNumber
INNER JOIN orderdetails od
    ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT p.productCode
    FROM products p
    INNER JOIN orderdetails od2
        ON p.productCode = od2.productCode
    INNER JOIN orders o2
        ON od2.orderNumber = o2.orderNumber
    GROUP BY p.productCode
    HAVING COUNT(DISTINCT o2.customerNumber) < 20
)
ORDER BY e.lastName, e.firstName
""", conn)

conn.close()

# Display results
print("=" * 80)
print("STEP 1: Boston Employees")
print("=" * 80)
print(df_boston)
print(f"\nTotal: {len(df_boston)} employees\n")

print("=" * 80)
print("STEP 2: Offices with Zero Employees")
print("=" * 80)
print(df_zero_emp)
print(f"\nTotal: {len(df_zero_emp)} offices\n")

print("=" * 80)
print("STEP 3: All Employees with Office Locations")
print("=" * 80)
print(df_employee)
print(f"\nTotal: {len(df_employee)} employees\n")

print("=" * 80)
print("STEP 4: Customers Without Orders")
print("=" * 80)
print(df_contacts)
print(f"\nTotal: {len(df_contacts)} customers (expected: 24)\n")

print("=" * 80)
print("STEP 5: Customer Payments (Top 10)")
print("=" * 80)
print(df_payment.head(10))
print(f"\nTotal: {len(df_payment)} payment records\n")

print("=" * 80)
print("STEP 6: High-Credit Sales Reps")
print("=" * 80)
print(df_credit)
print(f"\nTotal: {len(df_credit)} employees (expected: 4)\n")

print("=" * 80)
print("STEP 7: Product Sales (Top 10)")
print("=" * 80)
print(df_product_sold.head(10))
print(f"\nTotal: {len(df_product_sold)} products\n")

print("=" * 80)
print("STEP 8: Products with Customer Count (Top 10)")
print("=" * 80)
print(df_total_customers.head(10))
print(f"\nTotal: {len(df_total_customers)} products\n")

print("=" * 80)
print("STEP 9: Customers Per Office")
print("=" * 80)
print(df_customers)
print(f"\nTotal: {len(df_customers)} offices\n")

print("=" * 80)
print("STEP 10: Employees Who Sold Underperforming Products")
print("=" * 80)
print(df_under_20)
print(f"\nTotal: {len(df_under_20)} employees\n")

print("=" * 80)
print("ALL QUERIES COMPLETED SUCCESSFULLY!")
print("=" * 80)