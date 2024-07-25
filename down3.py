import re
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys


mod_id_list = []

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
pattern2 = re.compile(r"The server's version of (.+?) does not match the version on the Steam Workshop\. Server version: ([\d\.]+) Workshop version: ([\d\.]+)")
pattern3 = r'Reason: "([^"]+)"'

# messagebox.showinfo("Hướng dẫn", "Chọn đường dẫn đến file client_log.txt")
# Hiển thị hộp thoại để chọn file input
# input_file = filedialog.askopenfilename(title="Chọn file input", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

def process_file():
    input_file = filedialog.askopenfilename(title="Chọn file input", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    x = y = z = t = "Không tìm thấy"
    if input_file:
        try:
            #steamcmd_path = "path_to_steamcmd.exe"  # Adjust the path to your SteamCMD executable
            #output_batch_file = "download_mods.bat"
#            pattern = r"Your_regex_pattern_here"  # Adjust the regex pattern to match mod IDs in the file

            with open(input_file, 'r', encoding='utf-8') as infile:
                #with open(output_batch_file, 'w', encoding='utf-8') as batch_file:
                    # batch_file.write(f'"{steamcmd_path}" +login anonymous')
                    print("Work!!!")
                    for line in infile:
                        match = re.search(pattern, line)
                        if match:
                            mod_id = match.group(1)
                            mod_id_list.append(mod_id)
                            #batch_file.write(f' +workshop_download_item 322330 {mod_id} validate')
                            # Open the browser with the link

            with open(input_file, 'r', encoding='utf-8') as infile:
                    for line2 in infile:
                        match2 = re.search(pattern2, line2)
                        if match2:
                            x = match2.group(1)
                            y = match2.group(2)
                            z = match2.group(3)

            with open(input_file, 'r', encoding='utf-8') as infile:
                    for line3 in infile:
                        match3 = re.search(pattern3, line3)
                        if match3:
                            t = match3.group(1)
                    
                    #batch_file.write(' +quit\n')
            messagebox.showinfo("Mod Information", f"Mod bị lỗi:\nMod Name: {x}\nServer Version: {y}\nWorkshop Version: {z}\nMã lỗi: {t}")
            url = f'https://www.google.com/search?q={x}'
            webbrowser.open(url)
            # messagebox.showinfo("Thông báo", "Các mod bị lỗi đã được hiển thị trong trình duyệt.\nChạy file download_mods.bat để tự động tải về.\nFile batch đã được tạo thành công.")
        except OSError as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xử lý file: {e}")
    else:
        messagebox.showwarning("Thông báo", "Không có file nào được chọn.")

def show_options_window():
    options_window = tk.Toplevel(root)
    options_window.title("Lựa chọn")



def option1_action():
    if mod_id_list:
        for mod_id in mod_id_list:
            url = f'https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}'
            webbrowser.open(url)
    else:
        messagebox.showinfo("Lỗi", "Không tìm thấy id nào bị lỗi")

def option2_action():
    if mod_id_list:
        output_batch_file = "download_mods.bat"
        with open(output_batch_file, 'w', encoding='utf-8') as batch_file:
            batch_file.write(f'"{steamcmd_path}" +login anonymous')
            for mod_id in mod_id_list:
                batch_file.write(f' +workshop_download_item 322330 {mod_id} validate')
            batch_file.write(' +quit')
            messagebox.showinfo("Tạo Batch File", "Tạo download_mods.bat thành công")
    else:
        messagebox.showinfo("Lỗi", "Không có id nào")
def option3_action():
    for mod_id in mod_id_list:
        print(mod_id)


root = tk.Tk()
root.title("SteamCMD Mod Downloader")

process_button = tk.Button(root, text="Chọn file log", command=process_file)
process_button.pack(pady=20)


label = tk.Label(root, text="Tuỳ chọn cho các mod game không auto tải:")
label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

option1_button = tk.Button(button_frame, text="Mở Link Mod không tìm thấy", command=option1_action)
option1_button.pack(side=tk.LEFT, padx=5)

option2_button = tk.Button(button_frame, text="Tạo file download_mods", command=option2_action)
option2_button.pack(side=tk.LEFT, padx=5)

option3_button = tk.Button(button_frame, text="In list id không tìm thấy", command=option3_action)
option3_button.pack(side=tk.LEFT, padx=5)

root.mainloop()