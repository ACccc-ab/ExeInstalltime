import os
import subprocess
import time
import tkinter as tk
from tkinter import messagebox
import ctypes
import sys


def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            # 使用 Windows API 调用以管理员权限运行应用程序
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except ctypes.WinError:
            # 用户拒绝提升权限或发生其他错误
            # 在此处处理错误情况
            sys.exit(0)
    else:
        # 在非 Windows 系统上运行，无法提升权限
        # 在此处给出适当的错误处理或提示
        sys.exit(0)


# 检查是否以管理员权限运行
if not ctypes.windll.shell32.IsUserAnAdmin():
    # 如果不是管理员权限，则以管理员方式重新运行
    run_as_admin()
    sys.exit(0)  # 添加这个之后就不会运行两个主要功能的代码逻辑了，以管理员方式重新运行，当前进程退出


def get_app_list(folder_path):
    if not os.path.exists(folder_path):
        return []
    return [f for f in os.listdir(folder_path) if f.endswith('.exe')]


def install_exe():
    exe_path = os.path.join(app_list_folder, selected_app.get())
    silent_install_arg = "/S"  # 静默安装参数，减少因为人为点击导致的时间误差

    if not os.path.exists(exe_path):
        messagebox.showerror("错误", "找不到指定的exe文件。请检查路径是否正确。")
        return

    start_time = time.time()
    try:
        subprocess.run([exe_path, silent_install_arg], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"安装过程中出现错误: {e}")
        return

    # 原理：安装结束的时间-安装开始的时间=安装所耗费的时间
    end_time = time.time()
    elapsed_time = end_time - start_time
    messagebox.showinfo("安装完成", f"安装已完成，耗时：{elapsed_time:.2f}秒")


def main():
    global app_list_folder, selected_app

    app_list_folder = os.path.join(os.path.expanduser("~"), "Desktop", "applist")
    app_list = get_app_list(app_list_folder)

    if not app_list:
        messagebox.showerror("错误", "在桌面创建一个名为applist的文件夹，测试程序从该文件夹中获取")
        return

    window = tk.Tk()
    window.title("安装耗时测试")

    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="在桌面创建一个名为applist的文件夹，测试程序从该文件夹中获取", relief=tk.SUNKEN,anchor=tk.W)
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
