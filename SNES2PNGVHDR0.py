import sys
from pathlib import Path
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Frame
from tkinter.ttk import Progressbar, Style
from PIL import Image
import numpy as np

def read_png_image(file_path):
    """Read data from PNG file and return as an RGBA array."""
    try:
        with Image.open(file_path) as img:
            img = img.convert("RGBA")
            rgba_array = np.array(img)
            return rgba_array
    except IOError as e:
        raise Exception(f"Error reading file: {e}")

def process_rgba_to_snes(rgba_array):
    """Convert RGBA array to SNES-compatible hex data."""
    height, width, _ = rgba_array.shape
    snes_data = bytearray()

    for y in range(height):
        for x in range(0, width, 2):
            if x+1 < width:
                left_pixel = rgba_array[y, x]
                right_pixel = rgba_array[y, x+1]
            else:
                left_pixel = rgba_array[y, x]
                right_pixel = [0, 0, 0, 255]

            left_value = (left_pixel[0] // 85) & 1 | (((left_pixel[1] // 85) & 1) << 1)
            right_value = (right_pixel[0] // 85) & 1 | (((right_pixel[1] // 85) & 1) << 1)
            snes_data.append((left_value << 4) | right_value)

    return snes_data

def save_snes_hex(snes_data, file_path):
    """Save SNES-compatible hex data to a file."""
    try:
        with open(file_path, 'wb') as f:
            f.write(snes_data)
    except IOError as e:
        raise Exception(f"Error saving file: {e}")

def convert_png_to_snes_hex(input_file, output_file, progress_bar):
    """Convert PNG image data to SNES-compatible hex data."""
    try:
        progress_bar['value'] = 10
        root.update_idletasks()
        
        rgba_array = read_png_image(input_file)
        progress_bar['value'] = 40
        root.update_idletasks()
        
        snes_data = process_rgba_to_snes(rgba_array)
        progress_bar['value'] = 70
        root.update_idletasks()
        
        save_snes_hex(snes_data, output_file)
        progress_bar['value'] = 100
        root.update_idletasks()
        
        messagebox.showinfo("Success", "Image successfully converted and saved as SNES hex data!")
        progress_bar['value'] = 0
    except Exception as e:
        messagebox.showerror("Error", str(e))
        progress_bar['value'] = 0

def browse_file(entry):
    """Open file dialog to browse for an input file."""
    file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
    if file_path:
        entry.delete(0, 'end')
        entry.insert(0, file_path)

def save_file(entry):
    """Open file dialog to specify an output file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".hex", filetypes=[("Hex Files", "*.hex"), ("All Files", "*.*")])
    if file_path:
        entry.delete(0, 'end')
        entry.insert(0, file_path)

def create_gui():
    """Create the main GUI for PNG to SNES Hex conversion."""
    global root
    root = Tk()
    root.title("PNG to SNES Hex Converter 1.0")
    root.geometry("600x400")
    root.resizable(False, False)  # Disable maximize button

    # Create a frame to center the content
    frame = Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    Label(frame, text="PNG File:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    input_entry = Entry(frame, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=10)
    Button(frame, text="Browse", command=lambda: browse_file(input_entry), width=10).grid(row=0, column=2, padx=10, pady=10)

    Label(frame, text="Output File:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    output_entry = Entry(frame, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=10)
    Button(frame, text="Save As", command=lambda: save_file(output_entry), width=10).grid(row=1, column=2, padx=10, pady=10)

    # Progress bar
    style = Style(root)
    style.configure("TProgressbar", thickness=20)
    progress_bar = Progressbar(frame, style="TProgressbar", mode="determinate", length=400)
    progress_bar.grid(row=2, column=0, columnspan=3, pady=20)

    Button(frame, text="Convert", command=lambda: convert_png_to_snes_hex(input_entry.get(), output_entry.get(), progress_bar), width=20).grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
