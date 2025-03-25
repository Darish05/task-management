import tkinter as tk
import mysql.connector
from PIL import ImageTk, Image

# Connect to MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Darish149@5*",
  database="db"
)

# Create a cursor object
cursor = db.cursor()

# Create the tasks table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  completed BOOLEAN NOT NULL DEFAULT 0
)
""")

# Create the main window
window = tk.Tk()
window.title("Task Management")

# Create a frame for the tasks listbox
tasks_frame = tk.Frame(window)
tasks_frame.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar for the tasks listbox
scrollbar = tk.Scrollbar(tasks_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create the tasks listbox
tasks = tk.Listbox(tasks_frame, yscrollcommand=scrollbar.set)
tasks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=tasks.yview)

# Create a function to update the tasks listbox
def update_tasks():
    # Clear the current tasks
    tasks.delete(0, tk.END)

    # Get all the tasks from the database
    cursor.execute("SELECT * FROM tasks")
    tasks_list = cursor.fetchall()

    # Add each task to the listbox
    for task in tasks_list:
        tasks.insert(tk.END, f"{task[1]} - {task[2]}")

# Create a function to add a new task
def add_task():
    name = new_task_entry.get()
    if name:
        cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (name,))
        db.commit()
        update_tasks()
        new_task_entry.delete(0, tk.END)

# Create a function to mark a task as completed
def toggle_complete(index):
    # Get the task's id from the listbox
    task_id = int(tasks.get(index).split("-")[0].strip())

    # Toggle the completed status of the task
    cursor.execute("UPDATE tasks SET completed = NOT completed WHERE id = %s", (task_id,))
    db.commit()

    # Update the tasks listbox
    update_tasks()

# Create a function to delete all completed tasks
def delete_completed():
    cursor.execute("DELETE FROM tasks WHERE completed = 1")
    db.commit()
    update_tasks()

# Create a frame for the input field and buttons
input_frame = tk.Frame(window)
input_frame.pack(fill=tk.X, pady=10)

# Create a label and entry field for the new task
new_task_label = tk.Label(input_frame, text="Add a new task:")
new_task_label.pack(side=tk.LEFT)
new_task_entry = tk.Entry(input_frame, width=20)
new_task_entry.pack(side=tk.LEFT)

# Create a button to add a new task
add_task_button = tk.Button(input_frame, text="Add Task", command=add_task)
add_task_button.pack(side=tk.LEFT, padx=10)

# Create a button to delete all completed tasks
delete_button = tk.Button(input_frame, text="Delete Completed", command=delete_completed)
delete_button.pack(side=tk.LEFT)

# Start the Tkinter event loop
window.mainloop()
