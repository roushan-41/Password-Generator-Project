import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultra-Secure Password Gen")
        self.root.geometry("450x550")
        self.root.resizable(False, False)

        # UI Elements
        tk.Label(self.root, text="Password Length (Min 12 for Strength):", font=('Arial', 10, 'bold')).pack(pady=10)
        self.length_entry = tk.Entry(self.root, font=('Arial', 14), width=10)
        self.length_entry.insert(0, "12") # Default strong length
        self.length_entry.pack(pady=5)

        # Options
        self.uppercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.uppercase_var).pack()
        
        self.lowercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.lowercase_var).pack()
        
        self.digits_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Digits", variable=self.digits_var).pack()
        
        self.symbols_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var).pack()

        # Uniqueness Toggle
        self.unique_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.root, text="Ensure Unique Characters (No Repeats)", variable=self.unique_var, fg="blue").pack(pady=5)

        self.generate_btn = tk.Button(self.root, text="Generate Strong Password", font=('Arial', 12, 'bold'), 
                                      bg="#4CAF50", fg="white", command=self.generate_password)
        self.generate_btn.pack(pady=15)

        self.password_display = tk.Entry(self.root, font=('Arial', 12), bd=2, state='readonly', justify='center', width=30)
        self.password_display.pack(pady=5)

        self.copy_btn = tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=10)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for length.")
            return

        # CRITERIA 1: Strength Validation:
        selected_types = sum([self.uppercase_var.get(), self.lowercase_var.get(), 
                              self.digits_var.get(), self.symbols_var.get()])

        if length < 12:
            messagebox.showwarning("Weak Password", "Length should be at least 12 for a 'Strong' rating.")
        
        if selected_types < 3:
            messagebox.showwarning("Low Diversity", "Select at least 3 character types for better security.")

        # Character Sets
        char_map = []
        if self.uppercase_var.get(): char_map.append(string.ascii_uppercase)
        if self.lowercase_var.get(): char_map.append(string.ascii_lowercase)
        if self.digits_var.get(): char_map.append(string.digits)
        if self.symbols_var.get(): char_map.append(string.punctuation)

        if not char_map:
            messagebox.showerror("Error", "Select at least one character type.")
            return

        full_pool = "".join(char_map)

        #CRITERIA 2: Uniqueness Logic:
        if self.unique_var.get() and length > len(full_pool):
            messagebox.showerror("Error", f"Pool only has {len(full_pool)} unique characters. Decrease length or disable 'Unique'.")
            return

        # Step 1: Guarantee one from each selected type
        password_list = [random.choice(s) for s in char_map]

        # Step 2: Fill the rest
        remaining = length - len(password_list)
        if self.unique_var.get():
            # Use random.sample to ensure NO repetitions from the pool
            available_pool = list(set(full_pool) - set(password_list))
            password_list += random.sample(available_pool, remaining)
        else:
            # Use random.choice (allows repetitions)
            password_list += [random.choice(full_pool) for _ in range(remaining)]

        # Step 3: Final Shuffle for unpredictability
        random.shuffle(password_list)
        final_password = "".join(password_list)
        
        self.password_display.config(state='normal')
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, final_password)
        self.password_display.config(state='readonly')

    def copy_to_clipboard(self):
        password = self.password_display.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
