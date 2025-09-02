import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

TASKS_FILE = "tasks_gui_advanced.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do List")

        self.tasks = self.load_tasks()

        # Entry Frame
        entry_frame = ttk.Frame(root, padding=10)
        entry_frame.pack(fill=tk.X)

        ttk.Label(entry_frame, text="Task:").pack(side=tk.LEFT)
        self.task_entry = ttk.Entry(entry_frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(entry_frame, text="Deadline (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.deadline_entry = ttk.Entry(entry_frame, width=15)
        self.deadline_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(entry_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)

        # Task List
        self.tree = ttk.Treeview(root, columns=("Title", "Deadline", "Status"), show="headings", height=10)
        self.tree.heading("Title", text="Task")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Status", text="Status")
        self.tree.column("Title", width=200)
        self.tree.column("Deadline", width=100)
        self.tree.column("Status", width=80)
        self.tree.pack(pady=10, padx=10)

        # Buttons
        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Mark Completed", command=self.mark_completed).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)

        self.populate_tasks()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        title = self.task_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        if not title:
            messagebox.showwarning("Input Error", "Task title is required.")
            return
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Date Format Error", "Deadline must be YYYY-MM-DD.")
                return
        self.tasks.append({
            "title": title,
            "deadline": deadline,
            "completed": False
        })
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.populate_tasks()

    def populate_tasks(self):
        self.tree.delete(*self.tree.get_children())
        for task in self.tasks:
            status = "✔️" if task["completed"] else "❌"
            deadline = task["deadline"]
            row_color = ""
            if deadline and not task["completed"]:
                try:
                    if datetime.strptime(deadline, "%Y-%m-%d") < datetime.today():
                        row_color = "red"
                except:
                    pass
            self.tree.insert("", tk.END, values=(task["title"], deadline, status), tags=(row_color,))
        self.tree.tag_configure("red", background="#fdd")

    def mark_completed(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Select a task to mark completed.")
            return
        index = self.tree.index(selected[0])
        self.tasks[index]["completed"] = True
        self.populate_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Select a task to delete.")
            return
        index = self.tree.index(selected[0])
        del self.tasks[index]
        self.populate_tasks()

    def on_close(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    app = ToDoApp(root)
    root.mainloop()
