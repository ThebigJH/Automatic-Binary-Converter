import tkinter as tk
from tkinter import ttk


def convert(*args):
    value = input_var.get().strip()
    mode = mode_var.get()

    # Clear previous results
    for var in result_vars.values():
        var.set("")

    if not value:
        return

    try:
        # Convert based on the selected input format
        if mode == "Decimal":
            number = int(value, 10)
            show_number(number)

        elif mode == "Hexadecimal":
            number = int(value.removeprefix("0x").removeprefix("0X"), 16)
            show_number(number)

        elif mode == "Binary":
            number = int(value.removeprefix("0b").removeprefix("0B"), 2)
            show_number(number)

        elif mode == "ASCII":
            # Treat input as text and convert every character
            codes = [ord(char) for char in value]

            result_vars["ASCII"].set(value)
            result_vars["Decimal"].set(" ".join(str(c) for c in codes))
            result_vars["Hexadecimal"].set(
                " ".join(format(c, "02X") for c in codes)
            )
            result_vars["Binary"].set(
                " ".join(format(c, "08b") for c in codes)
            )

    except ValueError:
        result_vars["Decimal"].set("Invalid input")
        result_vars["Hexadecimal"].set("Invalid input")
        result_vars["ASCII"].set("Invalid input")
        result_vars["Binary"].set("Invalid input")


def show_number(number):
    result_vars["Decimal"].set(str(number))
    result_vars["Hexadecimal"].set(format(number, "X"))
    result_vars["Binary"].set(format(number, "b"))

    if 0 <= number <= 127:
        char = chr(number)
        if char.isprintable():
            result_vars["ASCII"].set(char)
        else:
            result_vars["ASCII"].set(
                f"Non-printable ASCII (code {number})"
            )
    else:
        result_vars["ASCII"].set("Not standard 7-bit ASCII")


# Create the window
root = tk.Tk()
root.title("Automatic Number Converter")
root.geometry("560x410")
root.resizable(False, False)

input_var = tk.StringVar()
mode_var = tk.StringVar(value="Decimal")

result_vars = {
    "Decimal": tk.StringVar(),
    "Hexadecimal": tk.StringVar(),
    "ASCII": tk.StringVar(),
    "Binary": tk.StringVar()
}

# Title
title = ttk.Label(
    root,
    text="Automatic Number System Converter",
    font=("Arial", 16, "bold")
)
title.pack(pady=15)

# Input format selector
ttk.Label(root, text="Input format:").pack()

format_box = ttk.Combobox(
    root,
    textvariable=mode_var,
    values=["Decimal", "Hexadecimal", "ASCII", "Binary"],
    state="readonly",
    width=25
)
format_box.pack(pady=5)

# Input field
ttk.Label(root, text="Enter your value:").pack(pady=(10, 0))

input_entry = ttk.Entry(
    root,
    textvariable=input_var,
    font=("Arial", 12),
    width=42
)
input_entry.pack(pady=5)

# Results
results_frame = ttk.LabelFrame(root, text="Live Conversion Results")
results_frame.pack(fill="both", expand=True, padx=20, pady=15)

for row, name in enumerate(
    ["Decimal", "Hexadecimal", "ASCII", "Binary"]
):
    ttk.Label(
        results_frame,
        text=f"{name}:",
        font=("Arial", 10, "bold"),
        width=13
    ).grid(row=row, column=0, padx=10, pady=9, sticky="w")

    ttk.Label(
        results_frame,
        textvariable=result_vars[name],
        wraplength=350
    ).grid(row=row, column=1, padx=5, pady=9, sticky="w")

# Automatically update whenever the input or format changes
input_var.trace_add("write", convert)
mode_var.trace_add("write", convert)

root.mainloop()