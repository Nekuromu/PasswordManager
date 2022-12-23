from tkinter import *
from tkinter import messagebox
from random import choice
from string import ascii_letters, digits, punctuation
import pyperclip

DEFAULT_EMAIL = "nekuromu.nm@gmail.com"
PASSWORD_LENGTH = 16


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_chars = ascii_letters + digits + punctuation
    password = "".join(choice(password_chars) for i in range(PASSWORD_LENGTH))
    password_entry.delete(0, END)
    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_information():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Error",
                               message="An entry line has been left blank.")
        return

    is_ok = messagebox.askyesno(title="Is this Correct?",
                                message=f"Website: {website}\nEmail: {email}\nPassword: {password}")

    if is_ok:
        with open("data.txt", "a") as data_file:
            data_file.write(f"{website} | {email} | {password}\n")
            website_entry.delete(0, END)
            password_entry.delete(0, END)


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

search_button = Button(text="Search")
search_button.grid(column=1, row=1, columnspan=2, sticky="e")

window.mainloop()
