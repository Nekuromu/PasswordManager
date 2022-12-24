from tkinter import *
from tkinter import messagebox
from random import choice
from string import ascii_letters, digits, punctuation
import pyperclip
import json

DEFAULT_EMAIL = "nekuromu.nm@gmail.com"
PASSWORD_LENGTH = 16


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """
        Generate a random password composed of letters, digits, and punctuation characters,
        and copy it to the clipboard. The password has a fixed length specified by the PASSWORD_LENGTH constant.
        The generated password is also inserted into the 'password_entry' widget. Uses the 'pyperclip' module
        to copy the password to the clipboard.
    """
    password_chars = ascii_letters + digits + punctuation
    password = "".join(choice(password_chars) for _ in range(PASSWORD_LENGTH))
    password_entry.delete(0, END)
    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_information():
    """Saves website information (name, email, and password) to a JSON file,
     and clears the website name and password entry widgets."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }}

    if not website or not password:
        messagebox.showwarning(title="Error",
                               message="An entry line has been left blank.")
        return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else:
        data.update(new_data)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# --------------------------Search Function ----------------------------#

def search_information():
    """Searches for information (email and password) related to a website in a JSON file. If the website is found,
     the information is displayed and the password is copied to the clipboard."""
    search_term = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="File Not Found", message="data.json not found.")
    else:
        if search_term in data:
            email = data[search_term]["email"]
            password = data[search_term]["password"]
            messagebox.showinfo(title="Info Found",
                                message=f"Website: {search_term}\nEmail: {email}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showwarning(title="Not Found", message=f"No website was found matching '{search_term}'.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
logo_canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file='logo.png')
logo_canvas.create_image(100, 100, image=logo_img)
logo_canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky="e")

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2, sticky="e")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3, sticky="e")

# Entries
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2, sticky="w", padx=5)

email_entry = Entry(width=42)
email_entry.insert(0, DEFAULT_EMAIL)
email_entry.grid(column=1, row=2, columnspan=2, sticky="w", padx=5)

password_entry = Entry(width=24)
password_entry.grid(column=1, row=3, sticky="w", padx=5)

# Buttons
genpass_button = Button(text="Generate Password", command=generate_password)
genpass_button.grid(column=1, row=3, sticky="e", columnspan=2)

add_button = Button(text="Add", width=36, command=save_information)
add_button.grid(column=1, row=4, columnspan=2, sticky="w")

search_button = Button(text="Search", command=search_information)
search_button.grid(column=1, row=1, columnspan=2, sticky="e")

window.mainloop()
