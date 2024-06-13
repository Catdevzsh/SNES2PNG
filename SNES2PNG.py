import sys
from pathlib import Path
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar
from tkinter.ttk import Progressbar, Style
from PIL import Image

def read_snes_image(file_path):
    """Read data from file and return as bytearray."""
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except IOError as e:
        raise Exception(f"Error reading file: {e}")

def process_snes_to_rgba(snes_data):
    """Convert byte pairs in SNES data to an RGBA pixel array."""
    rgba_pixel_array = []
    for i in range(0, len(snes_data), 2):
        byte_pair = snes_data[i:i + 2]
        for bit_pos in range(7, -1, -1):
            pixel_1 = ((byte_pair[0] >> bit_pos) & 1) | (((byte_pair[1] >> bit_pos) & 1) << 1)
            rgba_pixel_array.append((pixel_1 * 85, pixel_1 * 85, pixel_1 * 85, 255))
    return rgba_pixel_array

def save_rgba_image(rgba_pixel_array, file_path, width, height):
    """Save RGBA pixel array to a PNG file."""
    try:
        image = Image.new('RGBA', (width, height))
        image.putdata(rgba_pixel_array)
        image.save(file_path)
    except IOError as e:
        raise Exception(f"Error saving image: {e}")

def convert_snes_to_png(input_file, output_file, width, progress_bar):
    """Convert SNES image data to a PNG file."""
    try:
        progress_bar['value'] = 10
        root.update_idletasks()
        
        snes_data = read_snes_image(input_file)
        progress_bar['value'] = 40
        root.update_idletasks()
        
        rgba_pixel_array = process_snes_to_rgba(snes_data)
        progress_bar['value'] = 70
        root.update_idletasks()
        
        height = len(rgba_pixel_array) // width
        save_rgba_image(rgba_pixel_array, output_file, width, height)
        progress_bar['value'] = 100
        root.update_idletasks()
        
        messagebox.showinfo("Success", "Image successfully converted and saved!")
        progress_bar['value'] = 0
    except Exception as e:
        messagebox.showerror("Error", str(e))
        progress_bar['value'] = 0

def browse_file(entry):
    """Open file dialog to browse for an input file."""
    file_path = filedialog.askopenfilename(filetypes=[("SNES Files", "*.sfc;*.smc"), ("All Files", "*.*")])
    if file_path:
        entry.delete(0, 'end')
        entry.insert(0, file_path)

def save_file(entry):
    """Open file dialog to specify an output file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
    if file_path:
        entry.delete(0, 'end')
        entry.insert(0, file_path)

def create_gui():
    """Create the main GUI for SNES2PNG 1.0."""
    global root
    root = Tk()
    root.title("SNES2PNG 1.0")
    root.geometry("600x400")
    root.resizable(False, False)  # Disable maximize button

    Label(root, text="SNES File:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    input_entry = Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=10)
    Button(root, text="Browse", command=lambda: browse_file(input_entry)).grid(row=0, column=2, padx=10, pady=10)

    Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    output_entry = Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=10)
    Button(root, text="Save As", command=lambda: save_file(output_entry)).grid(row=1, column=2, padx=10, pady=10)

    Label(root, text="Width:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    width_entry = Entry(root, width=10)
    width_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
    width_entry.insert(0, "256")  # Default width

    # Progress bar
    style = Style(root)
    style.configure("TProgressbar", thickness=20)
    progress_bar = Progressbar(root, style="TProgressbar", mode="determinate", length=400)
    progress_bar.grid(row=3, column=0, columnspan=3, pady=20)

    Button(root, text="Convert", command=lambda: convert_snes_to_png(input_entry.get(), output_entry.get(), int(width_entry.get()), progress_bar)).grid(row=4, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
