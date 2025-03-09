import sqlite3

db = sqlite3.connect('contacts.db')
cursor = db.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contact';")
table_exists = cursor.fetchone()

if table_exists:
    while True:
        reuse = input("A table with stored data was found. Do you want to reuse this table? (yes/no): ").lower()
        if reuse == 'yes':
            print("Reusing the existing table with stored data.")
            break
        elif reuse == 'no':
            cursor.execute('DROP TABLE IF EXISTS contact')
            print("Creating a new table.")
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact (
        name TEXT,
        contact TEXT UNIQUE,  -- Make contact a unique field
        city TEXT,
        email TEXT
    )
''')

def show_instructions():
    instructions = """
    Instructions:
    1. To add a new contact, select 'New' from the main menu. You will be prompted to enter a name, phone number, city, and email.
    2. To view all contacts, select 'All'. All stored contacts will be displayed.
    3. To edit an existing contact, select 'Edit'. You can update the name, phone number, city, or email.
    4. To search for a contact, select 'Search'. You can search by name or phone number.
    5. To delete a contact, select 'Delete'. Enter the name of the contact you want to remove.
    6. To exit the program, type 'Exit'.
    """
    print(instructions)

def welcome():
    while True:
        inn = input("Would you like to view the instructions? (yes/no): ").lower()
        if inn == 'yes':
            show_instructions()
            break
        elif inn == 'no':
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")
    
    return input("Choose an option: All, New, Edit, Search, Delete, or Exit: ").lower()

def check(sname):
    cursor.execute('SELECT name FROM contact WHERE name = ?', (sname,))
    obj = cursor.fetchone()
    return bool(obj)

def valid_no(sname):
    while True:
        scontact = input(f"Enter {sname}'s phone no: ")
        if scontact.isdigit() and (len(scontact) == 10 or len(scontact) == 8):
            return scontact
        else:
            print("Invalid number. Please enter a valid 8 or 10-digit phone number.")

def delete():
    sname = input("Enter the name to be deleted: ").title()
    if check(sname):
        cursor.execute('DELETE FROM contact WHERE name = ?', (sname,))
        print("Delete successful.")
    else:
        print(f"No contact exists with the name '{sname}'.")
    db.commit()

def new():
    sname = input("Enter new contact name: ").title()
    scontact = valid_no(sname)
    city = input("Enter city: ").strip()
    email = input("Enter email: ").strip()

    if not sname or not scontact or not city or not email:
        print("Error: All fields (name, contact, city, email) must be filled.")
        return

    try:
        cursor.execute('INSERT INTO contact (name, contact, city, email) VALUES (?, ?, ?, ?)',
                       (sname, scontact, city, email))
        print("New contact added!")
        db.commit()
    except sqlite3.IntegrityError:
        print("Error: A contact with this phone number already exists. Phone numbers must be unique.")

def all():
    cursor.execute('SELECT * FROM contact')
    obj = cursor.fetchall()
    if not obj:
        print("No contacts exist!")
    else:
        headers = ["Name", "Contact", "City", "Email"]
        print(f"{headers[0].ljust(20)} | {headers[1].ljust(15)} | {headers[2].ljust(15)} | {headers[3].ljust(30)}")
        print("-" * 85)
        for row in obj:
            if len(row) == 4:
                name, contact, city, email = row
                print(f"{name.ljust(20)} | {contact.ljust(15)} | {city.ljust(15)} | {email.ljust(30)}")
            else:
                print("Error: Missing fields in one of the contact entries.")

    db.commit()

def update_name():
    sname = input("Enter the current name to update: ").title()
    if check(sname):
        new_name = input("Enter the new name: ").title()
        cursor.execute('UPDATE contact SET name = ? WHERE name = ?', (new_name, sname))
        print("Name update successful.")
    else:
        print(f"No contact exists with the name '{sname}'.")
    db.commit()

def update_number():
    sname = input("Enter the contact name to update the phone number: ").title()
    if check(sname):
        scontact = valid_no(sname)
        cursor.execute('UPDATE contact SET contact = ? WHERE name = ?', (scontact, sname))
        print("Contact number update successful.")
    else:
        print(f"No contact exists with the name '{sname}'.")
    db.commit()

def update_city():
    sname = input("Enter the contact name to update the city: ").title()
    if check(sname):
        city = input("Enter new city: ")
        cursor.execute('UPDATE contact SET city = ? WHERE name = ?', (city, sname))
        print("City update successful.")
    else:
        print(f"No contact exists with the name '{sname}'.")
    db.commit()

def update_email():
    sname = input("Enter the contact name to update the email: ").title()
    if check(sname):
        email = input("Enter new email: ")
        cursor.execute('UPDATE contact SET email = ? WHERE name = ?', (email, sname))
        print("Email update successful.")
    else:
        print(f"No contact exists with the name '{sname}'.")
    db.commit()

def search_name():
    sname = input("Enter the name to search for: ").title()
    cursor.execute('SELECT * FROM contact WHERE name = ?', (sname,))
    result = cursor.fetchone()
    if result:
        name, contact, city, email = result
        print(f"Name: {name}, Contact: {contact}, City: {city}, Email: {email}")
    else:
        print(f"No contact found with the name '{sname}'.")

def search_number():
    scontact = input("Enter the phone number to search for: ")
    cursor.execute('SELECT * FROM contact WHERE contact = ?', (scontact,))
    result = cursor.fetchone()
    if result:
        name, contact, city, email = result
        print(f"Name: {name}, Contact: {contact}, City: {city}, Email: {email}")
    else:
        print(f"No contact found with the phone number '{scontact}'.")

print("WELCOME!!")

inn = welcome()

while True:
    if inn not in ['new', 'all', 'edit', 'search', 'delete', 'exit']:
        print("Invalid input. Please choose from the options: All, New, Edit, Search, Delete, or Exit.")
        inn = input("Choose an option: All, New, Edit, Search, Delete, or Exit: ").lower()
        continue
    
    if inn == 'new':
        new()
    elif inn == 'all':
        all()
    elif inn == 'edit':
        while True:
            i = input("Edit name, number, city, or email: ").lower()
            if i in ['name', 'number', 'num', 'city', 'email']:
                if i == 'name':
                    update_name()
                elif i == 'number' or i == 'num':
                    update_number()
                elif i == 'city':
                    update_city()
                elif i == 'email':
                    update_email()
                break
            else:
                print("Invalid option. Please choose 'name', 'number', 'city', or 'email'.")
    elif inn == 'search':
        while True:
            i = input("Search by name or number: ").lower()
            if i == 'name':
                search_name()
                break
            elif i == 'number' or i == 'num':
                search_number()
                break
            else:
                print("Invalid option. Please choose 'name' or 'number'.")
    elif inn == 'delete':
        delete()
    elif inn == 'exit':
        print("VISIT AGAIN!!")
        break

    inn = input("Choose an option: All, New, Edit, Search, Delete, or Exit: ").lower()

db.close()



