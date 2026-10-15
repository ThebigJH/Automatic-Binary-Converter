
import tkinter as tk
from tkinter import ttk

BASES = {
    "Decimal": 10,
    "Binary": 2,
    "Octal": 8,
    "Hexadecimal": 16,
}

DIGITS = {
    2: "01",
    8: "01234567",
    10: "0123456789",
    16: "0123456789ABCDEF",
}


def parse_number(value, mode):
    """Turn the user's input into a Python integer."""
    value = value.strip()

    if mode == "ASCII / Text":
        raise ValueError("Text is not a numeric input.")

    # int() with base 0 recognizes prefixes such as 0b, 0o, 0x.
    # Otherwise, use the base selected by the user.
    if value.lower().startswith(("0b", "0o", "0x")):
        return int(value, 0)

    return int(value, BASES[mode])


def convert_base(number, base):
    """Convert an integer to a base without using bin/oct/hex."""
    if number == 0:
        return "0"

    sign = "-" if number < 0 else ""
    number = abs(number)
    digits = []

    while number > 0:
        remainder = number % base
        digits.append(DIGITS[base][remainder])
        number //= base

    return sign + "".join(reversed(digits))


def explain_conversion(number, base):
    """Build a step-by-step explanation of a conversion."""
    if number < 0:
        return (
            "Negative numbers are converted by converting their "
            "absolute value, then adding a minus sign.\n\n"
            + explain_conversion(-number, base)
        )

    if number == 0:
        return "Zero is represented as 0 in every number system."

    original = number
    steps = []

    if base == 2:
        steps.append(
            f"Convert decimal {original} to binary by repeatedly "
            "dividing by 2 and recording each remainder."
        )
    elif base == 8:
        steps.append(
            f"Convert decimal {original} to octal by repeatedly "
            "dividing by 8 and recording each remainder."
        )
    elif base == 16:
        steps.append(
            f"Convert decimal {original} to hexadecimal by repeatedly "
            "dividing by 16. Values 10–15 become A–F."
        )
    else:
        return f"{original} is already a decimal number."

    steps.append("")

    n = original
    remainders = []

    while n > 0:
        remainder = n % base
        quotient = n // base
        remainders.append(remainder)

        digit = DIGITS[base][remainder]
        steps.append(
            f"{n} ÷ {base} = {quotient}, remainder {remainder}"
            + (f" ({digit})" if base == 16 else "")
        )
        n = quotient

    steps.append("")
    steps.append(
        "Read the remainders from bottom to top: "
        + convert_base(original, base)
    )

    # Show the positional-value calculation too.
    if base in (2, 8, 16):
        digits = convert_base(original, base)
        place_values = []

        for power, digit in enumerate(reversed(digits)):
            digit_value = int(digit, 16)
            if digit_value:
                place_values.append(
                    f"{digit_value} × {base}^{power}"
                    f" = {digit_value * (base ** power)}"
                )

        steps.append("")
        steps.append("Check using place values:")
        steps.append(" + ".join(place_values))
        steps.append(f" = {original}")

    return "\n".join(steps)

def update_results(*args):
    value = input_var.get().strip()
    mode = mode_var.get()

    for var in result_vars.values():
        var.set("")

    explanation_text.config(state="normal")
    explanation_text.delete("1.0", tk.END)

    if not value:
        status_var.set("Enter a value to begin.")
        explanation_text.insert(
            "1.0",
            "Your conversion steps will appear here."
        )
        explanation_text.config(state="disabled")
        return

    try:
        if mode == "ASCII / Text":
            # This mode treats input as text, not as a number.
            characters = list(value)

            result_vars["ASCII / Text"].set(value)
            result_vars["Decimal"].set(
                " ".join(str(ord(c)) for c in characters)
            )
            result_vars["Binary"].set(
                " ".join(format(ord(c), "b") for c in characters)
            )
            result_vars["Octal"].set(
                " ".join(format(ord(c), "o") for c in characters)
            )
            result_vars["Hexadecimal"].set(
                " ".join(format(ord(c), "X") for c in characters)
            )

            explanation = (
                "Text mode converts each Unicode character into its "
                "code point.\n\n"
                "For each character, ord(character) returns its "
                "Unicode code point.\n\n"
                "Note: Unicode code points are not always the same "
                "as ASCII codes or UTF-8 bytes."
            )
            status_var.set(
                f"Converted {len(characters)} character(s)."
            )

        else:
            number = parse_number(value, mode)

            result_vars["Decimal"].set(str(number))
            result_vars["Binary"].set(convert_base(number, 2))
            result_vars["Octal"].set(convert_base(number, 8))
            result_vars["Hexadecimal"].set(
                convert_base(number, 16)
            )

            # Show a printable ASCII character only for valid
            # standard 7-bit ASCII values.
            if 0 <= number <= 127:
                char = chr(number)
                if char.isprintable():
                    result_vars["ASCII / Text"].set(char)
                else:
                    result_vars["ASCII / Text"].set(
                        f"Control character (code {number})"
                    )
            else:
                result_vars["ASCII / Text"].set(
                    "Not standard 7-bit ASCII"
                )

            explanation = explain_conversion(number, 2)

            if mode == "Decimal":
                explanation = (
                    f"Input: {number} (decimal)\n\n"
                    + explain_conversion(number, 2)
                    + "\n\nOCTAL CONVERSION\n\n"
                    + explain_conversion(number, 8)
                )
            elif mode == "Binary":
                explanation = (
                    f"Input: {value} (binary)\n"
                    f"Decimal value: {number}\n\n"
                    "Binary place values are powers of 2.\n\n"
                    + " + ".join(
                        f"{digit} × 2^{power}"
                        for power, digit in enumerate(
                            reversed(convert_base(abs(number), 2))
                        )
                        if digit == "1"
                    )
                    + f"\n\nResult: {number}"
                )
            elif mode == "Octal":
                explanation = explain_conversion(number, 8)
            elif mode == "Hexadecimal":
                explanation = explain_conversion(number, 16)

            status_var.set(
                f"Successfully converted integer: {number}"
            )

        explanation_text.insert("1.0", explanation)

    except ValueError:
        status_var.set(
            f"Invalid {mode.lower()} input. Check your digits and prefix."
        )
        explanation_text.insert(
            "1.0",
            "The input could not be converted.\n\n"
            "Examples:\n"
            "Decimal: 42\n"
            "Binary: 101010 or 0b101010\n"
            "Octal: 52 or 0o52\n"
            "Hexadecimal: 2A or 0x2A\n"
            "ASCII / Text: Hello"
        )

    explanation_text.config(state="disabled")


def copy_result(name):
    """Copy a selected result to the clipboard."""
    value = result_vars[name].get()

    if value:
        root.clipboard_clear()
        root.clipboard_append(value)
        status_var.set(f"{name} result copied to clipboard.")


def clear_all():
    input_var.set("")
    mode_var.set("Decimal")
    input_entry.focus_set()

root = tk.Tk()
root.title("Number System Workbench")
root.geometry("790x720")
root.minsize(680, 600)

style = ttk.Style(root)
if "clam" in style.theme_names():
    style.theme_use("clam")

style.configure("Title.TLabel", font=("Arial", 18, "bold"))
style.configure("Heading.TLabel", font=("Arial", 10, "bold"))
style.configure("Result.TLabel", font=("Consolas", 11))

input_var = tk.StringVar()
mode_var = tk.StringVar(value="Decimal")
status_var = tk.StringVar(value="Ready")

result_vars = {
    "Decimal": tk.StringVar(),
    "Binary": tk.StringVar(),
    "Octal": tk.StringVar(),
    "Hexadecimal": tk.StringVar(),
    "ASCII / Text": tk.StringVar(),
}

# Main container
main = ttk.Frame(root, padding=18)
main.pack(fill="both", expand=True)

ttk.Label(
    main,
    text="Number System Workbench",
    style="Title.TLabel"
).pack(anchor="w")

ttk.Label(
    main,
    text="Convert, inspect, learn, and copy — all in one place."
).pack(anchor="w", pady=(3, 16))

# Input controls
input_frame = ttk.LabelFrame(main, text="Input", padding=12)
input_frame.pack(fill="x", pady=(0, 12))

ttk.Label(input_frame, text="Interpret input as:").grid(
    row=0, column=0, sticky="w", padx=(0, 10), pady=5
)

format_box = ttk.Combobox(
    input_frame,
    textvariable=mode_var,
    values=[
        "Decimal",
        "Binary",
        "Octal",
        "Hexadecimal",
        "ASCII / Text",
    ],
    state="readonly",
    width=20,
)
format_box.grid(row=0, column=1, sticky="w", pady=5)

ttk.Label(input_frame, text="Value:").grid(
    row=1, column=0, sticky="w", padx=(0, 10), pady=5
)

input_entry = ttk.Entry(
    input_frame,
    textvariable=input_var,
    font=("Consolas", 12),
)
input_entry.grid(row=1, column=1, sticky="ew", pady=5)
input_frame.columnconfigure(1, weight=1)

ttk.Button(
    input_frame,
    text="Clear",
    command=clear_all,
).grid(row=1, column=2, padx=(10, 0), pady=5)

# Conversion results
results_frame = ttk.LabelFrame(
    main, text="Live conversion results", padding=10
)
results_frame.pack(fill="x", pady=(0, 12))

for row, name in enumerate(result_vars):
    ttk.Label(
        results_frame,
        text=f"{name}:",
        style="Heading.TLabel",
        width=15,
    ).grid(row=row, column=0, sticky="w", padx=5, pady=5)

    ttk.Label(
        results_frame,
        textvariable=result_vars[name],
        style="Result.TLabel",
        wraplength=410,
    ).grid(row=row, column=1, sticky="w", padx=5, pady=5)

    ttk.Button(
        results_frame,
        text="Copy",
        command=lambda n=name: copy_result(n),
        width=8,
    ).grid(row=row, column=2, padx=5, pady=3)

results_frame.columnconfigure(1, weight=1)

# Learning panel
learn_frame = ttk.LabelFrame(
    main, text="How does it work?", padding=10
)
learn_frame.pack(fill="both", expand=True, pady=(0, 10))

explanation_text = tk.Text(
    learn_frame,
    height=9,
    wrap="word",
    font=("Consolas", 10),
    relief="flat",
    padx=8,
    pady=8,
)
explanation_text.pack(fill="both", expand=True)
explanation_text.insert(
    "1.0",
    "Enter a number above to see how the conversion works."
)
explanation_text.config(state="disabled")

ttk.Label(
    main,
    textvariable=status_var,
    anchor="w",
).pack(fill="x")

# Live updates whenever the input or mode changes
input_var.trace_add("write", update_results)
mode_var.trace_add("write", update_results)

input_entry.focus_set()
root.mainloop()

# yall better pay me for this, i spent soooo much time on it instead of studying for my test.