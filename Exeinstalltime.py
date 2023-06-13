import os
import subprocess
import time
import tkinter as tk
from tkinter import messagebox

def get_app_list(folder_path):
    if not os.path.exists(folder_path):
        return []
    return [f for f in os.listdir(folder_path) if f.endswith('.exe')]

def install_exe():
    exe_path = os.path.join(app_list_folder, selected_app.get())
    silent_install_arg = "/S"  # 请将此参数替换为您的安装程序支持的静默安装参数

    if not os.path.exists(exe_path):
        messagebox.showerror("错误", "找不到指定的exe文件。请检查路径是否正确。")
        return

    start_time = time.time()
    try:
        subprocess.run([exe_path, silent_install_arg], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"安装过程中出现错误: {e}")
        return

    end_time = time.time()
    elapsed_time = end_time - start_time
    messagebox.showinfo("安装完成", f"安装已完成，耗时：{elapsed_time:.2f}秒")

def main():
    global app_list_folder, selected_app

    app_list_folder = os.path.join(os.path.expanduser("~"), "Desktop", "applist")
    app_list = get_app_list(app_list_folder)

    if not app_list:
        messagebox.showerror("错误", "找不到可用的安装包。请确保applist文件夹存在并包含exe文件。")
        return

    window = tk.Tk()
    window.title("安装程序")


    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="在桌面创建一个名为applist的文件夹，文件从该文件夹中提取", relief=tk.SUNKEN, anchor=tk.W)
    label.pack(side=tk.BOTTOM, fill=tk.X)

    selected_app = tk.StringVar(window)
    selected_app.set(app_list[0])

    option_menu = tk.OptionMenu(frame, selected_app, *app_list)
    option_menu.pack()

    install_button = tk.Button(frame, text="开始安装", command=install_exe)
    install_button.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
