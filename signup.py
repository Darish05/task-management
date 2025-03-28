from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector

def clear():
    emailentry.delete(0, END)
    usernameentry.delete(0, END)
    pswentry.delete(0, END)
    conpswentry.delete(0, END)

def signin_page():
    signup_win.destroy()
    import signin

def connect_database():
    if (emailentry.get() == '' or 
        usernameentry.get() == '' or 
        pswentry.get() == '' or 
        conpswentry.get() == ''):
        messagebox.showerror("Error", "All fields are required")
        return

    if pswentry.get() != conpswentry.get():
        messagebox.showerror("Error", "Password Mismatch!!!")
        return

    try:
        con = mysql.connector.connect(host='localhost', user='root', password='Darish149@5*')
        mycursor = con.cursor()
    except mysql.connector.Error as e:
        messagebox.showerror('Error', f"Database connectivity issue: {e}")
        return

    try:
        # Create database and table if not exist
        mycursor.execute('CREATE DATABASE IF NOT EXISTS userdata')
        mycursor.execute('USE userdata')
        mycursor.execute('''CREATE TABLE IF NOT EXISTS data (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(50) NOT NULL,
                                username VARCHAR(100) NOT NULL,
                                password VARCHAR(20) NOT NULL)''')
        
        # Insert data
        query = 'INSERT INTO data (email, username, password) VALUES (%s, %s, %s)'
        mycursor.execute(query, (emailentry.get(), usernameentry.get(), pswentry.get()))
        con.commit()

        messagebox.showinfo('Success', 'Registration successful')
        clear()
        signup_win.destroy()
        import signin
    except mysql.connector.Error as e:
        messagebox.showerror('Error', f"SQL execution error: {e}")
    finally:
        if con:
            con.close()

# GUI Setup
signup_win = Tk()
signup_win.title('Signup Page')
signup_win.geometry("1239x660")
signup_win.resizable(False, False)

background = ImageTk.PhotoImage(file='img.png')
Label(signup_win, image=background).grid()

frame = Frame(signup_win)
frame.place(x=68, y=100)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Helvetica 16 bold italic', 18, 'bold'), bg='#9b5de5', fg='white')
heading.place(x=80, y=85)

Label(frame, text='Email', font=('Helvetica 16 bold italic', 12), width=10, bg='#9b5de5').place(x=150, y=140)
emailentry = Entry(frame, width=25, font=('Helvetica 16 bold italic', 12))
emailentry.place(x=85, y=175, anchor='w')

Label(frame, text='User Name', font=('Helvetica 16 bold italic', 12), width=10, bg='#9b5de5').place(x=150, y=215)
usernameentry = Entry(frame, width=25, font=('Helvetica 16 bold italic', 12))
usernameentry.place(x=85, y=265, anchor='w')

Label(frame, text='Password', font=('Helvetica 16 bold italic', 12), width=10, bg='#9b5de5').place(x=150, y=305)
pswentry = Entry(frame, width=25, font=('Helvetica 16 bold italic', 12), show="*")
pswentry.place(x=85, y=345, anchor='w')

Label(frame, text='Confirm Password', font=('Helvetica 16 bold italic', 12), width=20, bg='#9b5de5').place(x=120, y=385)
conpswentry = Entry(frame, width=25, font=('Helvetica 16 bold italic', 12), show="*")
conpswentry.place(x=85, y=425, anchor='w')

Button(frame, text='Signup', font=('Helvetica 16 bold italic', 12), width=10, bg='firebrick1', command=connect_database).place(x=145, y=465)
Label(frame, text='Already have an account?', font=('Helvetica 16 bold italic', 12), bg='#9b5de5').place(x=85, y=510)

loginbutton = Button(frame, text='LogIn', font=('Helvetica 16 bold italic', 9, 'bold underline'), bg='#9b5de5', fg='blue', bd=0, activebackground='white', activeforeground='blue', command=signin_page)
loginbutton.place(x=290, y=510)

signup_win.mainloop()
