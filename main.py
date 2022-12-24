from tkinter import *
from tkinter import messagebox
from random import choice
from string import ascii_letters, digits, punctuation
# import pyperclip
import json
import configparser
import os

DEFAULT_EMAIL = ""
PASSWORD_LENGTH = 16

if not os.path.exists('resources/data'):
    os.makedirs('resources/data')

# ---------------------------- Settings.ini Works --------------------------------- #

config = configparser.ConfigParser()

if not os.path.isfile("settings.ini"):
    config["defaults"] = {}
    config["defaults"]["default_email"] = ""
    with open("settings.ini", "w") as settings_file:
        config.write(settings_file)
else:
    config.read("settings.ini")
    DEFAULT_EMAIL = config["defaults"]["default_email"]


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
    # pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_information():
    """Saves website information (name, email, and password) to a JSON file,
     and clears the website name and password entry widgets."""
    website = website_entry.get().title()
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
        with open("resources/data/data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open("resources/data/data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else:
        data.update(new_data)

        with open("resources/data/data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# --------------------------Search Function ----------------------------#

def search_information():
    """Searches for information (email and password) related to a website in a JSON file. If the website is found,
     the information is displayed and the password is copied to the clipboard."""
    search_term = website_entry.get().title()

    try:
        with open("resources/data/data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="File Not Found", message="data.json not found.")
    else:
        if search_term in data:
            email = data[search_term]["email"]
            password = data[search_term]["password"]
            messagebox.showinfo(title="Info Found",
                                message=f"Website: {search_term}\nEmail: {email}\nPassword: {password}")
            # pyperclip.copy(password)
        else:
            messagebox.showwarning(title="Not Found", message=f"No website was found matching '{search_term}'.")


# -------------------------- Settings UI SETUP ----------------------------- #


def open_settings_window():
    settings_window = Tk()
    settings_window.title("Settings")

    # Nested Functions
    def close_window():
        settings_window.destroy()

    def save_settings():
        if df_email_entry.get():
            config["defaults"]["default_email"] = df_email_entry.get()
            with open("settings.ini", "w") as settings_file:
                config.write(settings_file)
            email_entry.delete(0, END)
            email_entry.insert(0, df_email_entry.get())
        close_window()

    # Labels
    df_email_label = Label(master=settings_window, text="Default Email:")
    df_email_label.grid(column=1, row=1, pady=20)

    # Entries
    df_email_entry = Entry(master=settings_window)
    df_email_entry.grid(column=2, row=1, pady=20)

    # Buttons
    cancel_button = Button(master=settings_window, text="Cancel", command=close_window)
    cancel_button.grid(column=0, row=3, sticky="sw", pady=1, padx=1)

    save_button = Button(master=settings_window, text="Save", command=save_settings)
    save_button.grid(column=3, row=3, sticky="se", pady=1, padx=1)

    settings_window.mainloop()


# ---------------------------- Main UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
logo_canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file='resources/images/logo.png')
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

settings_button = Button(text="Settings", command=open_settings_window)
settings_button.grid(column=0, row=4, sticky="e", padx=4)

window.mainloop()
