import re
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import subprocess
import zipfile
import requests
import threading

#print(steamapps)
#print(steamapps_mod)
steamapps_log = []



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

mod_id_list = []

# messagebox.showinfo("Chọn đường dẫn Steam", "Chọn đường dẫn Steam")
steamapps = ""
steamapps_2 = None
# steamapps = filedialog.askdirectory(title = "Chọn đường dẫn Steam")
mod_dir = "steamapps/workshop/content/322330"

steamapps_mod = f'{steamapps}/{mod_dir}'
# Đường dẫn tới file batch để tạo
output_batch_file = os.path.join(script_dir, 'download_mods.bat')

# Mẫu biểu thức chính quy để trích xuất ID
pattern = r"Failed to find mod workshop-(\d+)"
pattern2 = re.compile(r"The server's version of (.+?) does not match the version on the Steam Workshop\. Server version: ([\d\.]+) Workshop version: ([\d\.]+)")
pattern3 = r'Reason: "([^"]+)"'

pattern4 = r"[A-Z]:\\.*?\\steamapps\\"

# messagebox.showinfo("Hướng dẫn", "Chọn đường dẫn đến file client_log.txt")
# Hiển thị hộp thoại để chọn file input
# input_file = filedialog.askopenfilename(title="Chọn file input", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

def process_file():
    input_file = filedialog.askopenfilename(title="Chọn file input", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    x = y = z = t = "Không tìm thấy"
    global steamapps_2
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

            with open(input_file, 'r', encoding='utf-8') as infile:
                    flag = 1
                    for line4 in infile:
                        match4 = re.search(pattern4, line4)
                        if match4 and flag:
                            base_path = match4.group(0)
                            #print(base_path)
                            # base_path = re.search(r"[^ ]*\\steamapps\\", path).group(0)
                            new_path = base_path.replace("\steamapps", "")

                            steamapps_2 = new_path
                            flag = 0
                            break

                    #batch_file.write(' +quit\n')
            # messagebox.showinfo("Mod Information", f"Mod bị lỗi:\nMod Name: {x}\nServer Version: {y}\nWorkshop Version: {z}\nMã lỗi: {t}")
            # url = f'https://www.google.com/search?q={x}'
            # webbrowser.open(url)
            print(steamapps_2)
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

def execute_command(command):
    """Thực thi lệnh và hiển thị đầu ra trong thời gian thực."""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            print(line, end='')  # In mỗi dòng đầu ra khi nó được sản xuất
        process.stdout.close()
        process.wait()
        print("Đã chạy xong!!!")
        
        if process.returncode == 0:
            # Hiển thị thông báo thành công
            messagebox.showinfo("Tải Mod", "Tải Mod xong")
        else:
            # Capture and print any error output
            error_output = process.stderr.read()
            print("Error output:", error_output)
            # Hiển thị thông báo lỗi
            messagebox.showinfo("Lỗi", "Có lỗi xảy ra khi thực thi lệnh 1")

    except subprocess.CalledProcessError as e:
        # Handle errors in the called executable
        print("An error occurred:", e)
        print("Error output:", e.stderr)
        # Hiển thị thông báo lỗi
        messagebox.showinfo("Lỗi", "Có lỗi xảy ra khi thực thi lệnh 2")

def option2_action():
    # Lấy đường dẫn thư mục hiện tại
    current_dir = os.getcwd()
    
    # Đường dẫn thư mục steamcmd
    steamcmd_dir = os.path.join(current_dir, 'steamcmd')
    
    # Đường dẫn tệp steamcmd.exe
    steamcmd_exe = os.path.join(steamcmd_dir, 'steamcmd.exe')
    global steamapps_2
    global mod_id_list

    if mod_id_list:
        print("Đây là steamapps_2")
        print(steamapps_2)
        print("Đây là steamcmd_path\n")
        print(steamcmd_path)

        # Kiểm tra xem steamcmd.exe có tồn tại không
        if not os.path.isfile(steamcmd_exe):
            messagebox.showinfo("steamcmd.exe", "steamcmd.exe không tồn tại.\nĐang tải về...")
            print("steamcmd.exe không tồn tại. Đang tải về...")
            download_url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
            extract_to = os.path.join(os.getcwd(), 'steamcmd')
            download_and_extract_steamcmd(download_url, extract_to)
            print("Đã tải về và giải nén steamcmd.exe.")

        # Construct the command to execute as a list
        command = [
            steamcmd_exe,
            "+force_install_dir", steamapps_2,
            "+login", "anonymous"
        ]

        print(command)

        for mod_id in mod_id_list:
            command.extend(["+workshop_download_item", "322330", mod_id, "validate"])

        command.append("+quit")

        # Chạy lệnh trong một luồng riêng biệt
        threading.Thread(target=execute_command, args=(command,)).start()
    else:
        # Hiển thị thông báo lỗi
        messagebox.showinfo("Lỗi", "Không có id nào")

def option3_action():
    popup = tk.Toplevel(root)
    popup.geometry("300x200")
    popup.title("Thêm ID mod")

    label1 = tk.Label(popup, text="Nhập ID mod:")
    label1.pack(pady=5)
    
    entry1 = tk.Entry(popup)
    entry1.pack(pady=5)

    def xacnhan_button():
        id_mod = entry1.get()
        mod_id_list.append(id_mod)
        popup.destroy()

    xacnhan = tk.Button(popup, text="Xác nhận", command=xacnhan_button)
    xacnhan.pack(pady=10)

def download_steamcmd():
    url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    webbrowser.open(url)
    messagebox.showinfo("", "Tải về xong giải nén vào thư mục chứa script rồi\nSau đó chạy steamcmd để nó cài đặt")

def choose_steam_dir():
    steamapps = filedialog.askdirectory(title = "Chọn đường dẫn Steam")
    if steamapps:
        steamapps_mod = f'"{steamapps}/{mod_dir}"'
        messagebox.showinfo("Đường dẫn tải mod", steamapps_mod)
    else:
        messagebox.showinfo("Đường dẫn tải mod", "Bạn chưa chọn đường dẫn")

root = tk.Tk()
root.title("SteamCMD Mod Downloader")
root.iconbitmap('down3.ico')

process_button = tk.Button(root, text="Chọn file log", command=process_file)
process_button.pack(pady=10)

process_button1 = tk.Button(root, text="Tải steamcmd", command=download_steamcmd)
process_button1.pack(pady=10)

process_button2 = tk.Button(root, text="Chọn lại đường dẫn Steam", command=choose_steam_dir)
process_button2.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

option1_button = tk.Button(button_frame, text="Mở Link Mod không tìm thấy", command=option1_action)
option1_button.pack(side=tk.LEFT, padx=5)

option2_button = tk.Button(button_frame, text="Tải Mod", command=option2_action)
option2_button.pack(side=tk.LEFT, padx=5)

option3_button = tk.Button(button_frame, text="Thêm Mod", command=option3_action)
option3_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
