import tkinter as tk
import sqlite3
from tkinter import messagebox, simpledialog
import datetime

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
    main_window.configure(bg="#0e3246")

    # Create Add Product button
    add_product_button = tk.Button(main_window, text="Add Product", command=open_add_product_window, bg="#2ecc71", fg="white", font=("Arial", 14))
    add_product_button.place(relx=0.5, rely=0.4, anchor="center")

    # Create Remove Product button
    remove_product_button = tk.Button(main_window, text="Remove Product", command=open_remove_product_window, bg="#e74c3c", fg="white", font=("Arial", 14))
    remove_product_button.place(relx=0.5, rely=0.5, anchor="center")

    # Create Logout button
    logout_button = tk.Button(main_window, text="Logout", command=lambda: logout(main_window), bg="#e67e22", fg="white", font=("Arial", 14))
    logout_button.place(relx=0.95, rely=0.05, anchor="ne")  # Top right corner

    # Centering the window
    main_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Run the application
    main_window.mainloop()

def logout(current_window):
    current_window.destroy()  # Close the current window
    open_login_page()

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
    add_product_window.configure(bg="#0e3246")

    # Create input fields
    labels = ["Product Name", "Brand", "Price", "Category", "Admin ID", "Quantity"]
    global entry_fields
    entry_fields = []
    for i, label_text in enumerate(labels):
        label = tk.Label(add_product_window, text=label_text + ":", bg="#0e3246", fg="white", font=("Arial", 14))
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

def remove_product(product_id):
    remove_product_from_database(product_id)
    open_remove_product_window()

def open_remove_product_window():
    remove_product_window = tk.Tk()
    remove_product_window.title("Remove Product")

    screen_width = remove_product_window.winfo_screenwidth()
    screen_height = remove_product_window.winfo_screenheight()

    remove_product_window.configure(bg="#0e3246")

    products = get_products_from_database()

    for i, product in enumerate(products):
        product_str = ", ".join(map(str, product))
        label = tk.Label(remove_product_window, text=product_str, bg="#0e3246", fg="white", font=("Arial", 14))
        label.grid(row=i, column=0, padx=10, pady=5)
        remove_button = tk.Button(remove_product_window, text="Remove", command=lambda product_id=product[0]: remove_product(product_id), bg="#e74c3c", fg="white", font=("Arial", 14))
        remove_button.grid(row=i, column=1, padx=10, pady=5)

    remove_product_window.geometry(f"{screen_width}x{screen_height}+0+0")

    remove_product_window.mainloop()

cus_id=101

def buy_product(product_id, label):
    quantity_to_buy = simpledialog.askinteger("Quantity", "Enter the quantity you want to buy:")
    if quantity_to_buy is None:
        return
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute('''SELECT name, brand, price, category, admin_id, quantity FROM item WHERE id=?''', (product_id,))
        product = c.fetchone()
        product_name = product[0]  # Assuming the first column is the product name
        brand = product[1]
        price = product[2]
        category = product[3]
        admin_id = product[4]
        current_quantity = product[5]  # Assuming the second column is the current quantity

        if quantity_to_buy <= current_quantity:
            # Create tables if they do not exist
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
            
            # Update quantity in stock and item tables
            new_quantity = current_quantity - quantity_to_buy
            c.execute('''UPDATE stock SET quantity=? WHERE id=?''', (new_quantity, product_id))
            c.execute('''UPDATE item SET quantity=? WHERE id=?''', (new_quantity, product_id))
            c.execute('''INSERT INTO sales VALUES(?, ?, ?, ?)''', (salesid, product_id, quantity_to_buy, datetime.date.today().strftime('%Y-%m-%d')))
            c.execute('''INSERT INTO trans VALUES(?, ?,? )''', (1, salesid, cus_id,))
            conn.commit()

            # Update the product label with the new details
            updated_product_str = f"{product_id}, {product_name}, {brand}, {price}, {category}, {admin_id}, {new_quantity}"  # Include all details
            label.config(text=updated_product_str)

            messagebox.showinfo("Success", f"{quantity_to_buy} item(s) bought successfully!")
        else:
            messagebox.showerror("Error", "Not enough stock available!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to buy product: " + str(e))
    finally:
        conn.close()

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
    customer_window.configure(bg="#0e3246")

    # Get products from database
    products = get_products_from_database()
    salesid += 1
    
    # Display products
    for i, product in enumerate(products):
        product_str = ", ".join(map(str, product))
        label = tk.Label(customer_window, text=product_str, bg="#0e3246", fg="white", font=("Arial", 14))
        label.grid(row=i, column=0, padx=10, pady=5)

        # Pass label as argument to update quantity dynamically
        buy_button = tk.Button(customer_window, text="Buy", command=lambda product_id=product[0], lbl=label: buy_product(product_id, lbl), bg="#2ecc71", fg="white", font=("Arial", 14))
        buy_button.grid(row=i, column=1, padx=10, pady=5)

    # Create Logout button
    logout_button = tk.Button(customer_window, text="Logout", command=lambda: logout(customer_window), bg="#e67e22", fg="white", font=("Arial", 14))
    logout_button.place(relx=0.95, rely=0.05, anchor="ne")  # Top right corner

    # Centering the window
    customer_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Run the application
    customer_window.mainloop()

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "shopowner" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        open_main_window()
    elif username == "customer" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Customer!")
        root.destroy()  # Close login window
        open_customer_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

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
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        column_names = [description[0] for description in c.description]
        print("Column Names:", column_names)
        # Print rows
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()


def on_enter(e):
    e.widget['background'] = '#27ae60'

def on_leave(e):
    e.widget['background'] = '#2ecc71'

def open_login_page():
    global root
    root = tk.Tk()
    root.title("Login")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.configure(bg="#0e3246")
    root.geometry(f"400x300")
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

    # Create a frame to center content
    frame = tk.Frame(root, bg="#0e3246")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text="Username:", bg="#0e3246", fg="white", font=("Arial", 16)).pack(pady=5)
    global username_entry
    username_entry = tk.Entry(frame, font=("Arial", 16))
    username_entry.pack(pady=10)
    tk.Label(frame, text="Password:", bg="#0e3246", fg="white", font=("Arial", 16)).pack(pady=5)
    global password_entry
    password_entry = tk.Entry(frame, show='*', font=("Arial", 16))
    password_entry.pack(pady=10)
    login_button = tk.Button(frame, text="Login", command=validate_login, bg="#2ecc71", fg="white", font=("Arial", 14))
    login_button.pack(pady=20)
    root.mainloop()


open_login_page()