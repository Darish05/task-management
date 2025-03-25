from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector

def signin():
    if usernameE.get() == '' or pwE.get() == '':
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        con = mysql.connector.connect(host='localhost', user='root', password='Darish149@5*', database='userdata')
        mycursor = con.cursor()
    except mysql.connector.Error as e:
        messagebox.showerror('Error', f"Database connectivity issue: {e}")
        return

    query = 'SELECT * FROM data WHERE username = %s AND password = %s'
    mycursor.execute(query, (usernameE.get(), pwE.get()))
    row = mycursor.fetchone()

    if row:
        messagebox.showinfo('Success', 'Login successful')
        ob.destroy()
    else:
        messagebox.showerror('Error', 'Invalid username or password')

    con.close()

def signup_page():
    ob.destroy()
    import signup

# GUI Setup
ob = Tk()
ob.resizable(0, 0)
ob.title('Login Page')

bgimg = ImageTk.PhotoImage(file='img.png')
bglable = Label(ob, image=bgimg)
bglable.grid()

frame = Frame(ob)
frame.place(x=68, y=100)

heading = Label(frame, text='LOGIN', font=('Helvetica 16 bold italic', 18, 'bold'), bg='#9b5de5', fg='white')
heading.place(x=80, y=85)

Label(frame, text='Username', font=('Helvetica 16 bold italic', 12), width=10, bg='#9b5de5').place(x=150, y=140)
usernameE = Entry(frame, width=25, font=('Helvetica 16 bold italic', 12))
usernameE.place(x=85, y=175, anchor='w')

Label(frame, text='Password', font=('Helvetica 16 bold italic', 12), width=10, bg='#9b5de5').place(x=150, y=215)
pwE = Entry(frame, width=25, font=('Helvetica 16 bold italic', 12), show='*')
pwE.place(x=85, y=265, anchor='w')

Button(frame, text='Login', font=('Helvetica 16 bold italic', 12), width=10, bg='firebrick1', command=signin).place(x=145, y=305)
Label(frame, text="Don't have an account?", font=('Helvetica 16 bold italic', 12), bg='#9b5de5').place(x=85, y=350)

signupbutton = Button(frame, text='Signup', font=('Helvetica 16 bold italic', 9, 'bold underline'), bg='#9b5de5', fg='blue', bd=0, activebackground='white', activeforeground='blue', command=signup_page)
signupbutton.place(x=290, y=350)

ob.mainloop()
