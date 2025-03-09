import mysql.connector
connection = mysql.connector.connect(
    host="localhost",    
    user="root",        
    password="password" 
)

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS shop")
print("Database 'shop' created or already exists.")

connection.database = 'shop'

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        CustomerID INT PRIMARY KEY AUTO_INCREMENT,
        Name VARCHAR(50),
        Email VARCHAR(50),
        Phone VARCHAR(15)
    )
""")
print("Table 'customer' created or already exists.")

def add_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    phone = input("Enter customer phone: ")
    cursor.execute("INSERT INTO customer (Name, Email, Phone) VALUES (%s, %s, %s)", (name, email, phone))
    connection.commit()
    print("Customer details added successfully.")

def update_customer():
    customer_id = int(input("Enter CustomerID to update: "))
    print("What would you like to update?")
    print("1. Name")
    print("2. Email")
    print("3. Phone")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE customer SET Name = %s WHERE CustomerID = %s", (new_name, customer_id))
    elif choice == 2:
        new_email = input("Enter new email: ")
        cursor.execute("UPDATE customer SET Email = %s WHERE CustomerID = %s", (new_email, customer_id))
    elif choice == 3:
        new_phone = input("Enter new phone: ")
        cursor.execute("UPDATE customer SET Phone = %s WHERE CustomerID = %s", (new_phone, customer_id))
    else:
        print("Invalid choice.")
        return
    
    connection.commit()
    print("Customer details updated successfully.")

def delete_customer():
    customer_id = int(input("Enter CustomerID to delete: "))
    cursor.execute("DELETE FROM customer WHERE CustomerID = %s", (customer_id,))
    connection.commit()
    print("Customer details deleted successfully.")

def display_customers():
    cursor.execute("SELECT * FROM customer")
    records = cursor.fetchall()
    if records:
        print("\nCustomer Details:")
        for record in records:
            print(f"CustomerID: {record[0]}, Name: {record[1]}, Email: {record[2]}, Phone: {record[3]}")
    else:
        print("No customer details found.")

def menu():
    while True:
        print("\nMenu")
        print("1. Add Customer Details")
        print("2. Update Customer Details")
        print("3. Delete Customer Details")
        print("4. Display All Customer Details")
        print("5. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            add_customer()
        elif choice == 2:
            update_customer()
        elif choice == 3:
            delete_customer()
        elif choice == 4:
            display_customers()
        elif choice == 5:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

menu()

cursor.close()
connection.close()
