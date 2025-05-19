import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import shutil
import os
import zipfile
from datetime import datetime

# Log file name
log_file = "backup_log.txt"

# Function to log backup and recovery actions
def log_action(action, src, dest):
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action} from {src} to {dest}\n")

# Function to back up a file or folder as a ZIP
def backup_data():
    file_or_folder = filedialog.askopenfilename(title="Select File") or filedialog.askdirectory(title="Or Select Folder")
    if not file_or_folder:
        return

    destination = filedialog.askdirectory(title="Select Backup Destination")
    if not destination:
        return

    try:
        base_name = os.path.basename(file_or_folder.rstrip(os.sep))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_name = f"{base_name}_backup_{timestamp}.zip"
        zip_path = os.path.join(destination, zip_name)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isdir(file_or_folder):
                for root, dirs, files in os.walk(file_or_folder):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, os.path.dirname(file_or_folder))
                        zipf.write(full_path, arcname=rel_path)
            else:
                zipf.write(file_or_folder, arcname=base_name)

        log_action("Backup", file_or_folder, zip_path)
        messagebox.showinfo("Success", f"Backup created at:\n{zip_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Backup failed:\n{str(e)}")

# Function to recover files/folders from ZIP backup
def recover_data():
    zip_file = filedialog.askopenfilename(
        title="Select Backup ZIP File", filetypes=[("ZIP Files", "*.zip")]
    )
    if not zip_file:
        return

    destination = filedialog.askdirectory(title="Select Recovery Destination")
    if not destination:
        return

    try:
        with zipfile.ZipFile(zip_file, 'r') as zipf:
            zipf.extractall(destination)
            recovered_files = zipf.namelist()

        log_action("Recovery", zip_file, destination)
        messagebox.showinfo("Success", f"Recovered {len(recovered_files)} items to:\n{destination}")
    except Exception as e:
        messagebox.showerror("Error", f"Recovery failed:\n{str(e)}")

# Function to view the backup/recovery log
def show_log():
    if os.path.exists(log_file):
        log_window = tk.Toplevel(root)
        log_window.title("Backup and Recovery Log")
        log_window.geometry("600x400")

        text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("Arial", 10))
        with open(log_file, "r") as f:
            content = f.read()
        text_area.insert(tk.END, content)
        text_area.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showinfo("Log Not Found", "No log file found yet.")

# GUI Setup
root = tk.Tk()
root.title("Advanced Data Backup & Recovery")
root.geometry("480x320")
root.configure(bg="#f0f0f0")

tk.Label(root, text="🗂️ Data Backup & Recovery Tool", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)
tk.Button(root, text="📁 Backup File or Folder (ZIP)", command=backup_data, width=30, bg="lightblue").pack(pady=10)
tk.Button(root, text="♻️ Recover from ZIP", command=recover_data, width=30, bg="lightgreen").pack(pady=10)
tk.Button(root, text="📄 View Backup Log", command=show_log, width=30, bg="lightgray").pack(pady=10)

root.mainloop()
