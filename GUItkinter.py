from tkinter import *

def on_login():
    Myusername = e1.get()
    Mypassword = e2.get()
    print(f"Username: {Myusername}, Password: {Mypassword}")

top = Tk()
top.geometry("400x300")

# Creating Labels
username = Label(top, text="Username")
username.place(x=60, y=50)

password = Label(top, text="Password")
password.place(x=60, y=90)

# Creating Entry widgets
e1 = Entry(top)
e1.place(x=160, y=50)

e2 = Entry(top, show="*")  # Adding show="*" to hide password input
e2.place(x=160, y=90)

# Creating the login button
submit = Button(top, text='Login', command=on_login)
submit.place(x=75, y=130)

top.mainloop()
