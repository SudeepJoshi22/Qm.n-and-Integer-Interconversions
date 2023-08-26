import tkinter as tk
from tkinter import messagebox

def convertFloat2Fixed():
    try:
        a = float(entry.get())
        q1 = 4  # Modify as needed
        q2 = 29  # Modify as needed

        if (a < 0):
            negFlag = 1
        else:
            negFlag = 0

        numberStr = str(a)
        pointIdx = numberStr.find('.')

        mantissa = numberStr[0:pointIdx]
        ordinate = '0.' + numberStr[pointIdx + 1:]

        bMantissa = str(bin(int(mantissa)))
        fOrdinate = float(ordinate)

        bMantissa = bMantissa[bMantissa.find('b') + 1:]

        while len(bMantissa) < q1:
            bMantissa = '0' + bMantissa

        bMantissa = bMantissa[-q1:]

        bOrdinate = ''
        for _ in range(q2):
            k = 2 * fOrdinate
            digit = int(k)
            bOrdinate = bOrdinate + str(digit)
            fOrdinate = k - int(k)

        if negFlag:
            bMantissa, bOrdinate = twosComplement(bMantissa, bOrdinate, q1, q2)
            result_label.config(text=f"The binary is {bMantissa}.{bOrdinate}")
        else:
            result_label.config(text=f"The binary is {bMantissa}.{bOrdinate}")

        # Save data to conversion log file
        log_entry = f"decimal = {a}, binary = {bMantissa}.{bOrdinate}\n"
        with open("decimal_to_binary_log.txt", "a") as log_file:
            log_file.write(log_entry)

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid decimal number.")

def twosComplement(bMantissa, bOrdinate, q1, q2):
    bString = list(bMantissa + bOrdinate)

    for i in range(len(bString) - 1, -1, -1):
        if (bString[i] == '0'):
            bString[i] = '1'
        elif (bString[i] == '1'):
            bString[i] = '0'

    carry = '1'
    for i in range(len(bString) - 1, -1, -1):
        if carry == '0':
            break
        elif bString[i] == '0':
            bString[i] = carry
            carry = '0'
        elif bString[i] == '1':
            bString[i] = '0'

    return ''.join(bString[0:q1]), ''.join(bString[q1:])

def convertBinaryToDecimal():
    bin_str = binary_entry.get()
    dot = bin_str.find('.')
    sign = 0
    
    if bin_str[0] == '1':
        sign = 1
        bin_str = bin_str.replace('.', '')
        bin_str = twosComplement(bin_str, '0' * len(bin_str), len(bin_str), 0)
        bin_str = ''.join(bin_str)
        bin_str = bin_str[:dot] + "." + bin_str[dot:]
        bin_str = tuple(bin_str)
    
    dec_size = len(bin_str[:dot])
    frac_size = len(bin_str[dot + 1:])
    dec = 0

    for bit in bin_str[:dot]:
        dec_size = dec_size - 1
        dec = dec + int(bit) * (2**(dec_size))

    i = -1
    for bit in bin_str[dot + 1:]:
        dec = dec + int(bit) * (2**(i))
        i = i - 1

    return dec, sign

def binary_to_decimal_conversion():
    try:
        result, sign = convertBinaryToDecimal()
        if sign == 1:
            result_label_binary.config(text=f"Decimal value: -{result}")
        else:
            result_label_binary.config(text=f"Decimal value: {result}")

        # Save data to binary to decimal log file
        if sign == 1:
            log_entry = f"binary = {binary_entry.get()}, decimal = -{result}\n"
        else:
            log_entry = f"binary = {binary_entry.get()}, decimal = {result}\n"
        with open("binary_to_decimal_log.txt", "a") as log_file:
            log_file.write(log_entry)

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid binary number.")

app = tk.Tk()
app.title("Conversion Tool")

# Float to Fixed Conversion
label = tk.Label(app, text="Float to Fixed Conversion")
decimal_label = tk.Label(app, text="Enter a decimal number:")
entry = tk.Entry(app)
convert_button = tk.Button(app, text="Convert", command=convertFloat2Fixed)
result_label = tk.Label(app, text="Result will be shown here")

# Binary to Decimal Conversion
label_binary = tk.Label(app, text="Binary to Decimal Conversion")
binary_label = tk.Label(app, text="Enter a binary number:")
binary_entry = tk.Entry(app)
convert_button_binary = tk.Button(app, text="Convert", command=binary_to_decimal_conversion)
result_label_binary = tk.Label(app, text="Decimal value will be shown here")

# Arrange elements using grid layout
decimal_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry.grid(row=0, column=1, padx=10, pady=5)
convert_button.grid(row=0, column=2, padx=10, pady=5)
result_label.grid(row=1, columnspan=3, padx=10, pady=5)

binary_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
binary_entry.grid(row=2, column=1, padx=10, pady=5)
convert_button_binary.grid(row=2, column=2, padx=10, pady=5)
result_label_binary.grid(row=3, columnspan=3, padx=10, pady=5)

app.mainloop()

