import tkinter as tk
from tkinter import ttk

def calculation():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operator = operator_var.get()

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            result = num1 / num2 if num2 != 0 else "Error, you cannot divide by zero!"
        else:
            result = "Invalid operator"
        
        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Please enter in valid numbers.")

# Create the main window
root = tk.Tk()
root.title = ("Simple Calculator with GUI")

# Input fields
entry1 = tk.Entry(root, width=10)
entry1.grid(row=0, column=0, padx=5, pady=5)

entry2 = tk.Entry(root, width=10)
entry2.grid(row=0, column=2, padx=5, pady=5)

# Operator drop down menu
operator_var = tk.StringVar(value='+')
operator_menu = ttk.Combobox(root, textvariable=operator_var, values=['+', '-', '*', '/'], width=3)
operator_menu.grid(row=0, column=1, padx=5, pady=5)

# Calculate button
calc_button = tk.Button(root, text="Calculate", command=calculation)
calc_button.grid(row=1, column=0, columnspan=3, pady=10)

# Result label
result_label = tk.Label(root, text="Result: ")
result_label.grid(row=2, column=0, columnspan=3)

# Start the GUI
root.mainloop()