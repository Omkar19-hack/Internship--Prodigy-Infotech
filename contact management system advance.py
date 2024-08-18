import sqlite3
import re

# Connect to SQLite database (or create it)
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# Create the contacts table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   phone TEXT NOT NULL,
                   email TEXT NOT NULL)''')
conn.commit()

# Validate phone number (basic validation for demonstration)
def validate_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'  # E.164 format
    return re.match(pattern, phone)

# Validate email address
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

# Add a new contact
def add_contact():
    name = input("Enter contact name: ")
    phone = input("Enter contact phone number: ")
    email = input("Enter contact email address: ")

    if not validate_phone(phone):
        print("Invalid phone number format. Please use a valid format.")
        return
    if not validate_email(email):
        print("Invalid email address format. Please use a valid format.")
        return

    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    print(f"Contact '{name}' added successfully.")

# View all contacts
def view_contacts():
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    if contacts:
        for contact in contacts:
            print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}")
    else:
        print("No contacts found.")

# Search for a contact by name
def search_contact():
    search_term = input("Enter the name to search for: ")
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + search_term + '%',))
    results = cursor.fetchall()
    if results:
        for contact in results:
            print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}")
    else:
        print("No matching contacts found.")

# Edit an existing contact
def edit_contact():
    contact_id = input("Enter the ID of the contact to edit: ")
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = cursor.fetchone()
    
    if contact:
        print(f"Editing Contact - ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}")
        name = input("Enter new name (or press Enter to keep current): ") or contact[1]
        phone = input("Enter new phone number (or press Enter to keep current): ") or contact[2]
        email = input("Enter new email address (or press Enter to keep current): ") or contact[3]

        if not validate_phone(phone):
            print("Invalid phone number format. Please use a valid format.")
            return
        if not validate_email(email):
            print("Invalid email address format. Please use a valid format.")
            return

        cursor.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?", (name, phone, email, contact_id))
        conn.commit()
        print("Contact updated successfully.")
    else:
        print("Contact not found.")

# Delete a contact
def delete_contact():
    contact_id = input("Enter the ID of the contact to delete: ")
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = cursor.fetchone()

    if contact:
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")

# Main program loop
def main():
    while True:
        print("\nAdvanced Contact Management System")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_contact()
        elif choice == '2':
            view_contacts()
        elif choice == '3':
            search_contact()
        elif choice == '4':
            edit_contact()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close the database connection when the program exits
conn.close()
