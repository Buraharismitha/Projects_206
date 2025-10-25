from tkinter import *
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
import datetime
import pickle

# Global Variables
global filename
blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)

# Function to open main page after login
def open_main_page():
    login.destroy()  # Close the login window
    main = Tk()
    main.title("Authentication of Product & Counterfeits Elimination Using Blockchain")
    main.geometry("1300x800")
    main.configure(bg="#2C3E50")
    

    # Function definitions for product operations
    def addProduct():
        global filename
        text_output.delete('1.0', END)
        filename = askopenfilename(initialdir="original_barcodes")
        with open(filename, "rb") as f:
            bytes = f.read()
        pid = tf1.get()
        name = tf2.get()
        user = tf3.get()
        address = tf4.get()
        if pid and name and user and address:
            current_time = datetime.datetime.now()
            digital_signature = sha256(bytes).hexdigest()
            data = pid + "#" + name + "#" + user + "#" + address + "#" + str(current_time) + "#" + digital_signature
            blockchain.add_new_transaction(data)
            blockchain.mine()
            b = blockchain.chain[-1]
            text_output.insert(END, f"Blockchain Previous Hash: {b.previous_hash}\nBlock No: {b.index}\nCurrent Hash: {b.hash}\n")
            text_output.insert(END, f"Barcode Blockchain Digital Signature: {digital_signature}\n\n")
            blockchain.save_object(blockchain, 'blockchain_contract.txt')
            clearInputs()
        else:
            text_output.insert(END, "Please enter all details")

    def authenticateProduct():
        text_output.delete('1.0', END)
        filename = askopenfilename(initialdir="original_barcodes")
        with open(filename, "rb") as f:
            bytes = f.read()
        digital_signature = sha256(bytes).hexdigest()
        flag = True
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[5] == digital_signature:
                    text_output.insert(END, "Uploaded Product Barcode Authentication Successful\n")
                    text_output.insert(END, "Details extracted from Blockchain after Validation\n\n")
                    text_output.insert(END, f"Product ID: {arr[0]}\nProduct Name: {arr[1]}\nCompany/User: {arr[2]}\nAddress: {arr[3]}\nScan Date: {arr[4]}\nDigital Signature: {arr[5]}\n")
                    flag = False
                    break
        if flag:
            text_output.insert(END, "Uploaded Product Barcode Authentication Failed")

    def searchProduct():
        text_output.delete('1.0', END)
        pid = tf1.get()
        flag = True
        if pid:
            for i in range(len(blockchain.chain)):
                if i > 0:
                    b = blockchain.chain[i]
                    data = b.transactions[0]
                    arr = data.split("#")
                    if arr[0] == pid:
                        text_output.insert(END, f"Product Details for ID {pid}:\n")
                        text_output.insert(END, f"Product ID: {arr[0]}\nProduct Name: {arr[1]}\nCompany/User: {arr[2]}\nAddress: {arr[3]}\nScan Date: {arr[4]}\nDigital Signature: {arr[5]}\n")
                        flag = False
                        break
        if flag:
            text_output.insert(END, "Given product ID does not exist")

    def viewBlockchainInfo():
        text_output.delete('1.0', END)
        if len(blockchain.chain) > 1:  # Exclude the genesis block
            for i in range(1, len(blockchain.chain)):
                b = blockchain.chain[i]
                text_output.insert(END, f"Block {b.index}:\n")
                text_output.insert(END, f"Previous Hash: {b.previous_hash}\n")
                text_output.insert(END, f"Current Hash: {b.hash}\n")
                text_output.insert(END, f"Transactions: {b.transactions}\n")
                text_output.insert(END, "------------------------\n")
        else:
            text_output.insert(END, "No blocks available in the blockchain (except the genesis block).")

    def clearInputs():
        tf1.delete(0, END)
        tf2.delete(0, END)
        tf3.delete(0, END)
        tf4.delete(0, END)

    # Project Title
    title_frame = Frame(main, bg="#34495E", pady=10)
    title_frame.pack(fill=X)
    title_label = Label(title_frame, text="Authentication of Product & Counterfeits Elimination Using Blockchain", 
                        font=('Arial', 24, 'bold'), bg="#34495E", fg="white")
    title_label.pack()

    # Navigation Bar
    menu_bar = Menu(main)
    product_menu = Menu(menu_bar, tearoff=0)
    product_menu.add_command(label="Add Product", command=addProduct)
    product_menu.add_command(label="Authenticate Product", command=authenticateProduct)
    product_menu.add_command(label="Search Product", command=searchProduct)
    product_menu.add_command(label="View Blockchain Info", command=viewBlockchainInfo)  # New Option
    menu_bar.add_cascade(label="Product Operations", menu=product_menu)
    main.config(menu=menu_bar)

    # Input Frame
    input_frame = Frame(main, bg="#2C3E50", padx=20, pady=20)
    input_frame.pack(fill=X)

    Label(input_frame, text="Product ID:", font=('Arial', 12), bg="#2C3E50", fg="white").grid(row=0, column=0, padx=10, pady=5)
    tf1 = Entry(input_frame, font=('Arial', 12), width=30)
    tf1.grid(row=0, column=1, padx=10, pady=5)

    Label(input_frame, text="Product Name:", font=('Arial', 12), bg="#2C3E50", fg="white").grid(row=1, column=0, padx=10, pady=5)
    tf2 = Entry(input_frame, font=('Arial', 12), width=30)
    tf2.grid(row=1, column=1, padx=10, pady=5)

    Label(input_frame, text="Company/User Details:", font=('Arial', 12), bg="#2C3E50", fg="white").grid(row=2, column=0, padx=10, pady=5)
    tf3 = Entry(input_frame, font=('Arial', 12), width=50)
    tf3.grid(row=2, column=1, padx=10, pady=5)

    Label(input_frame, text="Address Details:", font=('Arial', 12), bg="#2C3E50", fg="white").grid(row=3, column=0, padx=10, pady=5)
    tf4 = Entry(input_frame, font=('Arial', 12), width=50)
    tf4.grid(row=3, column=1, padx=10, pady=5)

    # Output Frame
    output_frame = Frame(main, bg="white", padx=10, pady=10)
    output_frame.pack(fill=BOTH, expand=True)

    text_output = Text(output_frame, wrap=WORD, font=('Arial', 12), height=20, bg='#ECF0F1', fg='#2C3E50')
    text_output.pack(fill=BOTH, expand=True)

    main.mainloop()

# Admin Login Page
def login_check():
    if username_entry.get() == "admin" and password_entry.get() == "admin":
        open_main_page()
    else:
        error_label.config(text="Invalid Username or Password", fg="red")

login = Tk()
login.title("Admin Login")
login.geometry("1300x800")
login.configure(bg="#2C3E50")

Label(login, text="Admin Login", font=("Arial", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=20)

Label(login, text="Username", font=("Arial", 12), bg="#2C3E50", fg="white").pack(pady=5)
username_entry = Entry(login, font=("Arial", 12))
username_entry.pack(pady=5)

Label(login, text="Password", font=("Arial", 12), bg="#2C3E50", fg="white").pack(pady=5)
password_entry = Entry(login, font=("Arial", 12), show="*")
password_entry.pack(pady=5)

login_button = Button(login, text="Login", font=("Arial", 12, "bold"), bg="#34495E", fg="white", command=login_check)
login_button.pack(pady=20)

error_label = Label(login, text="", font=("Arial", 12), bg="#2C3E50", fg="white")
error_label.pack()

login.mainloop()
