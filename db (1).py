import tkinter as tk
import sqlite3
from tkinter import messagebox, simpledialog
import datetime

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        open_main_window()
    elif username == "customer" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Customer!")
        root.destroy()  # Close login window
        open_customer_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_window():
    # Close login window
    root.destroy()

    # Create main window
    main_window = tk.Tk()
    main_window.title("Main Page")

    # Get screen width and height
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    # Set background color
    main_window.configure(bg="#3498db")

    # Create Add Product button
    add_product_button = tk.Button(main_window, text="Add Product", command=open_add_product_window, bg="#2ecc71", fg="white", font=("Arial", 14))
    add_product_button.place(relx=0.5, rely=0.4, anchor="center")

    # Create Remove Product button
    remove_product_button = tk.Button(main_window, text="Remove Product", command=open_remove_product_window, bg="#e74c3c", fg="white", font=("Arial", 14))
    remove_product_button.place(relx=0.5, rely=0.5, anchor="center")

    # Centering the window
    main_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Run the application
    main_window.mainloop()

def add_product_to_database(product_details):
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS item
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      brand TEXT NOT NULL,
                      price REAL NOT NULL,
                      category TEXT NOT NULL,
                      admin_id TEXT NOT NULL,
                      quantity INTEGER NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS stock
                     (id INTEGER,
                      quantity INTEGER NOT NULL,
                      FOREIGN KEY (id) REFERENCES item(id))''')
        print('''INSERT INTO item (name, brand, price, category, admin_id, quantity) VALUES''', product_details)
        c.execute('''INSERT INTO item (name, brand, price, category, admin_id, quantity)
                     VALUES (?, ?, ?, ?, ?, ?)''', product_details)
        item_id = c.lastrowid
        print('''INSERT INTO stock (id, quantity) VALUES''', (item_id, product_details[5]))
        c.execute('''INSERT INTO stock VALUES (?, ?)''', (item_id, product_details[5]))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to add product to database: " + str(e))
    finally:
        conn.close()

# Function to handle Add button click
def add_product():
    # Get product details from entry fields
    product_name = entry_fields[0].get()
    brand = entry_fields[1].get()
    price = float(entry_fields[2].get())
    category = entry_fields[3].get()
    admin_id = entry_fields[4].get()
    quantity = int(entry_fields[5].get())
    
    # Add product to database
    product_details = (product_name, brand, price, category, admin_id, quantity)
    add_product_to_database(product_details)

# Function to open add product window
def open_add_product_window():
    # Create add product window
    add_product_window = tk.Tk()
    add_product_window.title("Add Product")

    # Get screen width and height
    screen_width = add_product_window.winfo_screenwidth()
    screen_height = add_product_window.winfo_screenheight()

    # Set background color
    add_product_window.configure(bg="#3498db")

    # Create input fields
    labels = ["Product Name", "Brand", "Price", "Category", "Admin ID", "Quantity"]
    global entry_fields
    entry_fields = []
    for i, label_text in enumerate(labels):
        label = tk.Label(add_product_window, text=label_text + ":", bg="#3498db", fg="white", font=("Arial", 14))
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(add_product_window, font=("Arial", 14))
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry_fields.append(entry)

    # Create Add button
    add_button = tk.Button(add_product_window, text="Add", command=add_product, bg="#2ecc71", fg="white", font=("Arial", 14))
    add_button.grid(row=len(labels), columnspan=2, padx=10, pady=10)

    # Centering the window
    add_product_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Run the application
    add_product_window.mainloop()

def get_products_from_database():
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM item''')
        products = c.fetchall()
        return products
    except Exception as e:
        messagebox.showerror("Error", "Failed to retrieve products from database: " + str(e))
    finally:
        conn.close()

def remove_product_from_database(product_id):
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute('''DELETE FROM item WHERE id=?''', (product_id,))
        print('''DELETE FROM item WHERE id=''', product_id)
        conn.commit()
        messagebox.showinfo("Success", "Product removed successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to remove product from database: " + str(e))
    finally:
        conn.close()

# Function to handle Remove button click
def remove_product(product_id):
    remove_product_from_database(product_id)
    # Refresh the window after removal
    open_remove_product_window()

# Function to open the Remove Product window
def open_remove_product_window():
    # Create remove product window
    remove_product_window = tk.Tk()
    remove_product_window.title("Remove Product")

    # Get screen width and height
    screen_width = remove_product_window.winfo_screenwidth()
    screen_height = remove_product_window.winfo_screenheight()

    # Set background color
    remove_product_window.configure(bg="#3498db")

    # Get products from database
    products = get_products_from_database()

    # Display products
    for i, product in enumerate(products):
        product_str = ", ".join(map(str, product))
        label = tk.Label(remove_product_window, text=product_str, bg="#3498db", fg="white", font=("Arial", 14))
        label.grid(row=i, column=0, padx=10, pady=5)
        remove_button = tk.Button(remove_product_window, text="Remove", command=lambda product_id=product[0]: remove_product(product_id), bg="#e74c3c", fg="white", font=("Arial", 14))
        remove_button.grid(row=i, column=1, padx=10, pady=5)

    # Centering the window
    remove_product_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Run the application
    remove_product_window.mainloop()

cus_id=101
# Function to handle Buy button click
def buy_product(product_id):
    quantity_to_buy = simpledialog.askinteger("Quantity", "Enter the quantity you want to buy:")
    if quantity_to_buy is None:
        return  # User clicked Cancel
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute('''SELECT quantity FROM stock WHERE id=?''', (product_id,))
        print('''SELECT quantity FROM stock WHERE id=''', product_id)
        current_quantity = c.fetchone()[0]
        if quantity_to_buy <= current_quantity:
            c.execute('''CREATE TABLE IF NOT EXISTS sales
                     (sales_id INTEGER NOT NULL,
                      id INTEGER NOT NULL,
                      quantity INTEGER NOT NULL,
                      date DATE,
                      FOREIGN KEY (id) REFERENCES item(id))''')
            c.execute('''CREATE TABLE IF NOT EXISTS trans
                     (t_id INTEGER NOT NULL,
                      sales_id INTEGER NOT NULL,
                      customer_id INTEGER,
                      FOREIGN KEY (sales_id) REFERENCES sales(sales_id))''')
            new_quantity = current_quantity - quantity_to_buy
            c.execute('''UPDATE stock SET quantity=? WHERE id=?''', (new_quantity, product_id))  # Here we provide arguments to execute method
            c.execute('''UPDATE item SET quantity=? WHERE id=?''', (new_quantity, product_id))
            c.execute('''INSERT INTO sales VALUES(?, ?, ?, ?)''', (salesid, product_id, quantity_to_buy, datetime.date.today().strftime('%Y-%m-%d')))
            c.execute('''INSERT INTO trans VALUES(?, ?,? )''', (1, salesid, cus_id,))
            print('INSERT INTO sales VALUES', (salesid, product_id, quantity_to_buy, datetime.date.today().strftime('%Y-%m-%d')))
            print('UPDATE stock SET quantity=', new_quantity,' WHERE id=', product_id)
            print('UPDATE item SET quantity=', new_quantity,' WHERE id=', product_id)
            print('''INSERT INTO trans VALUES''', (salesid, cus_id)) 
            conn.commit()
            messagebox.showinfo("Success", f"{quantity_to_buy} item(s) bought successfully!")
        else:
            messagebox.showerror("Error", "Not enough stock available!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to buy product: " + str(e))
    finally:
        conn.close()


# Function to open the Customer window
salesid = 1000
def open_customer_window():
    global salesid
    # Create customer window
    customer_window = tk.Tk()
    customer_window.title("Customer Page")

    # Get screen width and height
    screen_width = customer_window.winfo_screenwidth()
    screen_height = customer_window.winfo_screenheight()

    # Set background color
    customer_window.configure(bg="#3498db")

    # Get products from database
    products = get_products_from_database()
    salesid += 1
    # Display products
    for i, product in enumerate(products):
        product_str = ", ".join(map(str, product))
        label = tk.Label(customer_window, text=product_str, bg="#3498db", fg="white", font=("Arial", 14))
        label.grid(row=i, column=0, padx=10, pady=5)
        buy_button = tk.Button(customer_window, text="Buy", command=lambda product_id=product[0]: buy_product(product_id), bg="#2ecc71", fg="white", font=("Arial", 14))
        buy_button.grid(row=i, column=1, padx=10, pady=5)

    # Centering the window
    customer_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Run the application
    customer_window.mainloop()

# Function to validate customer login
def validate_customer_login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password are correct
    if username == "customer" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Customer!")
        root.destroy()  # Close login window
        open_customer_window()  # Open customer window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def print_table_details(table_name):
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        # Execute SELECT query to fetch all rows from the table
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        # Print column names
        column_names = [description[0] for description in c.description]
        print("Column Names:", column_names)
        # Print rows
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()

root = tk.Tk()
root.title("Login Page")
print_table_details('trans')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.configure(bg="#3498db")

username_label = tk.Label(root, text="Username:", bg="#3498db", fg="white", font=("Arial", 14))
username_label.place(relx=0.4, rely=0.4, anchor="center")
username_entry = tk.Entry(root, font=("Arial", 14))
username_entry.place(relx=0.6, rely=0.4, anchor="center")

password_label = tk.Label(root, text="Password:", bg="#3498db", fg="white", font=("Arial", 14))
password_label.place(relx=0.4, rely=0.5, anchor="center")
password_entry = tk.Entry(root, show="*", font=("Arial", 14))
password_entry.place(relx=0.6, rely=0.5, anchor="center")

login_button = tk.Button(root, text="Login", command=validate_login, bg="#2ecc71", fg="white", font=("Arial", 14))
login_button.place(relx=0.5, rely=0.6, anchor="center")

# Centering the windo
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Run the application
root.mainloop()
