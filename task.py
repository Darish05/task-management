from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
EMAIL_HOST = 'smtp.example.com'  # Update with your SMTP server address
EMAIL_PORT = 587  # Update with your SMTP port
EMAIL_USERNAME = 'your_email@example.com'  # Update with your email address
EMAIL_PASSWORD = 'your_email_password'  # Update with your email password

def send_email(receiver, subject, body):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        # Create message
        message = MIMEMultipart()
        message['From'] = EMAIL_USERNAME
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send email
        server.sendmail(EMAIL_USERNAME, receiver, message.as_string())
        print("Email notification sent successfully!")
    except Exception as e:
        print("Failed to send email notification:", str(e))
    finally:
        # Close connection
        server.quit()

def add_task():  
    task_string = task_field.get()  
    due_date = due_date_entry.get()
    due_time = due_time_entry.get()
    
    if len(task_string) == 0 or len(due_date) == 0 or len(due_time) == 0:
        messagebox.showinfo('Error', 'Fields are Empty.')  
    else:  
        tasks.append((task_string, due_date, due_time))  
        cursor.execute('INSERT INTO tasks (title, due_date, due_time) VALUES (%s, %s, %s)', (task_string, due_date, due_time))
        mydb.commit()
        list_update()  
        task_field.delete(0, 'end')  
        due_date_entry.delete(0, 'end')
        due_time_entry.delete(0, 'end')

def list_update():  
    clear_list()  
    
    cursor.execute('SELECT title, due_date, due_time FROM tasks')
    for task in cursor.fetchall():  
        task_listbox.insert('end', f"{task[0]} (Due: {task[1]} {task[2]})")  

def delete_task():  
    try:  
        the_value = task_listbox.get(task_listbox.curselection())  
        task_name = the_value.split(" (Due: ")[0]
        if task_name in [task[0] for task in tasks]:  
            tasks = [task for task in tasks if task[0] != task_name]
            list_update()  
            cursor.execute('DELETE FROM tasks WHERE title = %s', (task_name,))
            mydb.commit()
    except:  
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')        

def delete_all_tasks():  
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')  
    
    if message_box == True:  
        tasks.clear()
        cursor.execute('DELETE FROM tasks')
        mydb.commit()
        list_update()  

def clear_list():  
    task_listbox.delete(0, 'end')  

def close():  
    print(tasks)  
    guiWindow.destroy()  

# Function to check for tasks with due times approaching
def check_due_tasks():
    cursor.execute('SELECT title, due_date, due_time FROM tasks')
    for task in cursor.fetchall():
        task_title, due_date, due_time = task
        due_datetime = datetime.combine(due_date, due_time)
        # Check if due time is within the notification threshold (e.g., 15 minutes before)
        if due_datetime - datetime.now() <= timedelta(minutes=15):
            send_email(receiver='recipient@example.com', subject=f'Task Reminder: {task_title}', body=f'Task "{task_title}" is due soon!')

# Function to periodically check for due tasks and schedule next check
def schedule_notifications():
    check_due_tasks()
    # Schedule the next check after a certain interval (e.g., every 5 minutes)
    guiWindow.after(300000, schedule_notifications)  # 300000 milliseconds = 5 minutes

if __name__ == "__main__":  
    guiWindow = Tk()  
    guiWindow.title("Task Manager App")  
    guiWindow.geometry("700x400+550+250")  
    guiWindow.resizable(0, 0)  
    guiWindow.configure(bg="WHITE")  
    
    mydb = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )

    cursor = mydb.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title VARCHAR(255), due_date DATE, due_time TIME)')  

    tasks = []  
    
    functions_frame = Frame(guiWindow, bg="WHITE") 
    functions_frame.pack(side="top", expand=True, fill="both")  

    task_label = Label(functions_frame,text="Enter Task:", font=("arial", "14", "bold"), background="WHITE")  
    task_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  
    
    task_field = Entry(functions_frame, font=("Arial", "14"), width=30)  
    task_field.grid(row=0, column=1, padx=10, pady=10)  

    due_date_label = Label(functions_frame, text="Due Date:", font=("arial", "14", "bold"), background="WHITE")  
    due_date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")  
    
    due_date_entry = Entry(functions_frame, font=("Arial", "14"), width=15)  
    due_date_entry.grid(row=1, column=1, padx=10, pady=10)  

    due_time_label = Label(functions_frame, text="Due Time:", font=("arial", "14", "bold"), background="WHITE")  
    due_time_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")  
    
    due_time_entry = Entry(functions_frame, font=("Arial", "14"), width=15)  
    due_time_entry.grid(row=2, column=1, padx=10, pady=10)  

    add_button =Button(functions_frame, text="Add Task", width=15, bg='green', fg="white", font=("arial", "14", "bold"), command=add_task)  
    add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)  

    del_button = Button(functions_frame, text="Delete Task", width=15, bg='green', fg="white", font=("arial", "14", "bold"), command=delete_task)  
    del_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)  

    del_all_button = Button(functions_frame, text="Delete All Tasks", width=15, font=("arial", "14", "bold"), bg='green', fg="white", command=delete_all_tasks)  
    del_all_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)  

    exit_button = Button(functions_frame, text="Exit", width=52, bg='green', fg="white", font=("arial", "14", "bold"), command=close)  
    exit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)  
    
    task_listbox = Listbox(functions_frame, width=60, height=10, font=("bold", 12), selectmode='SINGLE', background="WHITE", foreground="BLACK", selectbackground="#D4AC0D", selectforeground="BLACK")  
    task_listbox.grid(row=0, column=2, rowspan=7, padx=20, pady=10, sticky="ns")  
    
    # Schedule the first notification check
    schedule_notifications()

    guiWindow.mainloop()  

    cursor.close()
    mydb.close()
