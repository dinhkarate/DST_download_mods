import re
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Function to get the path of the script or executable
def get_script_path():
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        return os.path.dirname(sys.executable)
    else:
        # Running in normal Python environment
        return os.path.dirname(os.path.abspath(__file__))

# Đường dẫn tới thư mục chứa file script hoặc executable
script_dir = get_script_path()
steamcmd_path = os.path.join(script_dir, 'steamcmd.exe')

# Đường dẫn tới file batch để tạo
output_batch_file = os.path.join(script_dir, 'download_mods.bat')

# Mẫu biểu thức chính quy để trích xuất ID
pattern = r"Failed to find mod workshop-(\d+)"

# Khởi tạo tk và ẩn cửa sổ chính
root = tk.Tk()
root.withdraw()

# Hiển thị hộp thoại để chọn file input
input_file = filedialog.askopenfilename(title="Chọn file input", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

if input_file:
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            with open(output_batch_file, 'w', encoding='utf-8') as batch_file:
                batch_file.write(f'"{steamcmd_path}" +login anonymous')
                
                for line in infile:
                    match = re.search(pattern, line)
                    if match:
                        mod_id = match.group(1)
                        batch_file.write(f' +workshop_download_item 322330 {mod_id} validate')
                        # Mở trình duyệt với liên kết
                        url = f'https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}'
                        webbrowser.open(url)
                        
                batch_file.write(' +quit\n')
        messagebox.showinfo("Thông báo", "Các mod bị lỗi đã được hiển thị trong trình duyệt.\nChạy file download_mods.bat để tự động tải về.\nFile batch đã được tạo thành công.")
    except OSError as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xử lý file: {e}")
else:
    messagebox.showwarning("Thông báo", "Không có file nào được chọn.")
