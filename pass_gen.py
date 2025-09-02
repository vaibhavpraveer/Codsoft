import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Generator")

        self.style = ttk.Style()
        self.style.theme_use("default")

        # Layout frame
        main_frame = ttk.Frame(root, padding=20)
        main_frame.grid()

        # Password length input
        ttk.Label(main_frame, text="Password Length:").grid(row=0, column=0, sticky=tk.W)
        self.length_var = tk.IntVar(value=12)
        ttk.Entry(main_frame, textvariable=self.length_var, width=10).grid(row=0, column=1, sticky=tk.W)

        # Character type checkboxes
        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        ttk.Checkbutton(main_frame, text="Include Uppercase", variable=self.include_upper).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Include Lowercase", variable=self.include_lower).grid(row=2, column=0, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Include Digits", variable=self.include_digits).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Include Symbols", variable=self.include_symbols).grid(row=4, column=0, sticky=tk.W)

        # Generate button
        ttk.Button(main_frame, text="Generate Password", command=self.generate_password).grid(row=5, column=0, columnspan=2, pady=10)

        # Output entry
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, font=("Arial", 12), width=30)
        self.password_entry.grid(row=6, column=0, columnspan=2)

        # Copy to clipboard button
        ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=7, column=0, columnspan=2, pady=5)

        # Password strength label
        self.strength_label = ttk.Label(main_frame, text="", font=("Arial", 10, "bold"))
        self.strength_label.grid(row=8, column=0, columnspan=2, pady=5)

    def generate_password(self):
        length = self.length_var.get()
        if length < 4:
            messagebox.showwarning("Invalid Length", "Length must be at least 4 characters.")
            return

        characters = ""
        count_types = 0

        if self.include_upper.get():
            characters += string.ascii_uppercase
            count_types += 1
        if self.include_lower.get():
            characters += string.ascii_lowercase
            count_types += 1
        if self.include_digits.get():
            characters += string.digits
            count_types += 1
        if self.include_symbols.get():
            characters += string.punctuation
            count_types += 1

        if not characters:
            messagebox.showerror("No Options", "Please select at least one character type.")
            return

        password = ''.join(random.choices(characters, k=length))
        self.password_var.set(password)
        self.evaluate_strength(length, count_types)

    def evaluate_strength(self, length, types):
        if length >= 12 and types >= 3:
            strength = "Strong"
            color = "green"
        elif length >= 8 and types >= 2:
            strength = "Moderate"
            color = "orange"
        else:
            strength = "Weak"
            color = "red"
        self.strength_label.config(text=f"Strength: {strength}", foreground=color)

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Please generate a password first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
