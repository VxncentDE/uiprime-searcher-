import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import math

def generate_primes(reqammount, file_path, progress_var):
    try:
        ammount = 1  # Starting with 2 as the first prime number
        i = 3
        primes = [2]  # Initialize with the first prime
        with open(file_path, "w") as file:
            file.write("2,")  # Write the first prime
            progress_var.set((ammount / reqammount) * 100)
            
            while ammount < reqammount:
                is_prime = True
                limit = int(math.sqrt(i)) + 1
                for p in primes:
                    if p > limit:
                        break
                    if i % p == 0:
                        is_prime = False
                        break
                
                if is_prime:
                    primes.append(i)
                    result = f"{i},"
                    file.write(result)
                    ammount += 1
                    # Update progress bar
                    progress_var.set((ammount / reqammount) * 100)
                
                i += 2  # Only check odd numbers
        messagebox.showinfo("Completed", f"Prime generation completed. {ammount} primes saved.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        # Reset progress bar after completion
        progress_var.set(0)

def start_program():
    try:
        req_amount = int(req_amount_entry.get())
        file_path = file_path_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file path.")
            return
        # Run prime generation in a separate thread to keep UI responsive
        threading.Thread(target=generate_primes, args=(req_amount, file_path, progress_var)).start()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for required primes.")

def select_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def open_results():
    file_path = file_path_entry.get()
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()
                results_window = tk.Toplevel()
                results_window.title("Results")
                results_text = tk.Text(results_window, wrap="word")
                results_text.insert(tk.END, content)
                results_text.pack(expand=True, fill="both")
                results_text.config(state="disabled")
        except FileNotFoundError:
            messagebox.showerror("Error", "Results file not found.")
    else:
        messagebox.showerror("Error", "Please select a file path.")

# Set up the main GUI
root = tk.Tk()
root.title("Prime Number Generator")

# Input for required amount of primes
tk.Label(root, text="Required Number of Primes:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
req_amount_entry = tk.Entry(root)
req_amount_entry.grid(row=0, column=1, padx=10, pady=10)
req_amount_entry.insert(0, "500")  # Default value

# Input for file path
tk.Label(root, text="Save Results To:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
file_path_entry = tk.Entry(root, width=40)
file_path_entry.grid(row=1, column=1, padx=10, pady=10)
file_path_button = tk.Button(root, text="Browse", command=select_file)
file_path_button.grid(row=1, column=2, padx=10, pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="we")

# Start program button
start_button = tk.Button(root, text="Start Program", command=start_program)
start_button.grid(row=3, column=0, columnspan=3, pady=10)

# Open results button
open_button = tk.Button(root, text="Open Results", command=open_results)
open_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
