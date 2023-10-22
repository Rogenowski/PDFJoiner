import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PyPDF2 import PdfMerger
import zipfile
from tkinter import ttk

selected_files = []

def join_pdfs():
    if not selected_files:
        result_label.config(text="No selected files.")
        return

    pdf_merger = PdfMerger()

    for file in selected_files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Convert images to PDF
            pdf_from_image = Image.open(file)
            pdf_from_image.save("temporary.pdf")
            file = "temporary.pdf"

        try:
            pdf_merger.append(file)
        except FileNotFoundError:
            result_label.config(text=f"File '{file}' does not exist.")

    output_file = output_entry.get()
    base_name, file_extension = os.path.splitext(output_file)
    if not file_extension:
        output_file += '.pdf'

    pdf_merger.write(output_file)
    pdf_merger.close()
    os.remove("temporary.pdf")
    result_label.config(text=f"PDF files were merged and saved.")

def add_files():
    files = filedialog.askopenfilenames(title="Select PDF, PNG, or JPG files", filetypes=[("PDF", "*.pdf"), ("PNG", "*.png"), ("JPG", "*.jpg *.jpeg")])
    selected_files.extend(files)
    for file in files:
        selected_files_listbox.insert(tk.END, os.path.basename(file))

def remove_selected_files():
    selected_indices = selected_files_listbox.curselection()
    for i in selected_indices:
        selected_files_listbox.delete(i)
        selected_files.pop(i)

def move_file_up():
    selected_index = selected_files_listbox.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        if selected_index > 0:
            selected_files_listbox.delete(selected_index)
            selected_files_listbox.insert(selected_index - 1, os.path.basename(selected_files[selected_index]))
            selected_files.insert(selected_index - 1, selected_files.pop(selected_index))

def move_file_down():
    selected_index = selected_files_listbox.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        if selected_index < len(selected_files) - 1:
            selected_files_listbox.delete(selected_index)
            selected_files_listbox.insert(selected_index + 1, os.path.basename(selected_files[selected_index]))
            selected_files.insert(selected_index + 1, selected_files.pop(selected_index))

def zip_and_combine():
    if not selected_files:
        result_label.config(text="No selected files.")
        return

    output_file = output_entry.get()
    base_name, file_extension = os.path.splitext(output_file)
    if not file_extension:
        output_file += '.pdf'

    zip_filename = base_name + '.zip'

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        pdf_merger = PdfMerger()

        for file in selected_files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Convert images to PDF
                pdf_from_image = Image.open(file)
                pdf_from_image.save("temporary.pdf")
                file = "temporary.pdf"

            try:
                pdf_merger.append(file)
            except FileNotFoundError:
                result_label.config(text=f"File '{file}' does not exist.")

        pdf_merger.write(output_file)
        zipf.write(output_file, os.path.basename(output_file))
        os.remove(output_file)

    result_label.config(text=f"PDF file was merged and zipped: {zip_filename}")

def remove_all_files():
    global selected_files
    selected_files = []
    selected_files_listbox.delete(0, tk.END)

def move_file_to_top():
    selected_indices = selected_files_listbox.curselection()
    for i in selected_indices:
        selected_index = int(i)
        if selected_index > 0:
            selected_files_listbox.delete(selected_index)
            selected_files_listbox.insert(0, os.path.basename(selected_files[selected_index]))
            selected_files.insert(0, selected_files.pop(selected_index))

def move_file_to_bottom():
    selected_indices = selected_files_listbox.curselection()
    for i in selected_indices:
        selected_index = int(i)
        if selected_index < len(selected_files) - 1:
            selected_files_listbox.delete(selected_index)
            selected_files_listbox.insert(tk.END, os.path.basename(selected_files[selected_index]))
            selected_files.append(selected_files.pop(selected_index))

root = tk.Tk()
root.title("PDF Joining App")

add_files_button = tk.Button(root, text="Add Files", command=add_files)
add_files_button.pack(pady=5)

files_label = tk.Label(root, text="Selected Files:")
files_label.pack()

selected_files_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=0, width=50, height=10)
selected_files_listbox.pack()

button_frame = tk.Frame(root)
button_frame_top = tk.Frame(button_frame)
button_frame_bottom = tk.Frame(button_frame)

style = ttk.Style()
style.configure("EqualSize.TButton", width=15, height=40)

remove_selected_button = ttk.Button(button_frame_top, text="Remove Selected", command=remove_selected_files, style="EqualSize.TButton")
remove_selected_button.pack(side=tk.LEFT, padx=5)
move_up_button = ttk.Button(button_frame_top, text="Move Up", command=move_file_up, style="EqualSize.TButton")
move_up_button.pack(side=tk.LEFT, padx=5)
move_down_button = ttk.Button(button_frame_top, text="Move Down", command=move_file_down, style="EqualSize.TButton")
move_down_button.pack(side=tk.LEFT, padx=5)
remove_all_button = ttk.Button(button_frame_bottom, text="Remove All", command=remove_all_files, style="EqualSize.TButton")
remove_all_button.pack(side=tk.LEFT, padx=5)
move_to_top_button = ttk.Button(button_frame_bottom, text="Move to Top", command=move_file_to_top, style="EqualSize.TButton")
move_to_top_button.pack(side=tk.LEFT, padx=5)
move_to_bottom_button = ttk.Button(button_frame_bottom, text="Move to Bottom", command=move_file_to_bottom, style="EqualSize.TButton")
move_to_bottom_button.pack(side=tk.LEFT, padx=5)

button_frame_top.pack()
button_frame_bottom.pack()
button_frame.pack(pady=5)

output_label = tk.Label(root, text="Output File Name:")
output_label.pack()
output_entry = tk.Entry(root, width=40)
output_entry.pack()

join_button = tk.Button(root, text="Join PDF", command=join_pdfs)
join_button.pack(pady=5)

zip_and_combine_button = tk.Button(root, text="Join and Zip", command=zip_and_combine)
zip_and_combine_button.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
