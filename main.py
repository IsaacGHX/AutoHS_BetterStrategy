import tkinter as tk
import os
import keyboard
from FSM_action import system_exit, AutoHS_automata
from log_state import check_name
from FSM_action import init
from autohs_logger import logger_init
from tkinter import messagebox
from constants.constants import *
from config import *
from get_screen import test_hs_available, test_battlenet_available
from json_op import JSON_LAST_MODIFIED_TIME

ABNORMAL_WIDTH_HEIGHT_LIST = [(1707, 960), (2048, 1152), (1306, 720), (1536, 864)]

def is_integer(s):
    try:
        num = int(s)
        return num
    except ValueError:
        messagebox.showinfo("Warning", "请输入整数")
        return None

def check_hearthstone_path(path):
    if not os.path.exists(path):
        messagebox.showinfo("Warning", "炉石安装路径不存在")
        return False

    if not os.path.exists(os.path.join(path, "Hearthstone.exe")):
        messagebox.showinfo("Warning", "安装路径下未找到Hearthstone.exe")
        return False

    if not os.path.exists(os.path.join(path, "logs")):
        messagebox.showinfo("Warning", "安装路径下未找到logs文件夹")
        return False

    return True

def update_width(event):
    num = is_integer(entry_width.get())
    if num is not None:
        autohs_config.width = num

def update_height(event):
    num = is_integer(entry_height.get())
    if num is not None:
        autohs_config.height = num

def update_max_play_time(event):
    num = is_integer(entry_max_play_time.get())
    if num is not None:
        autohs_config.max_play_time = num

def update_max_win_count(event):
    num = is_integer(entry_max_win_count.get())
    if num is not None:
        autohs_config.max_win_count = num

def update_install_path(event):
    path = entry_path.get()
    if (check_hearthstone_path(path)):
        autohs_config.hearthstone_install_path = entry_path.get()

def update_player_name(event):
    autohs_config.player_name = entry_player_name.get()

def update_all():
    update_width(None)
    update_height(None)
    update_max_play_time(None)
    update_max_win_count(None)
    update_install_path(None)
    update_player_name(None)

def start_function():
    autohs_config.is_running = True

    check_name()
    init()
    AutoHS_automata()

def mock_start_function():
    # 创建一个隐藏的主窗口
    autohs_config.is_running = True

    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 弹出提示框
    messagebox.showinfo("Mock Function", "Mock function called. No actual functionality executed")

    # 销毁主窗口
    root.destroy()

def close_gui():
    root.quit()
    root.destroy()
    if autohs_config.is_running:
        system_exit()

def check_before_start():
    if autohs_config.is_running:
        messagebox.showinfo("Warning", "程序已在运行中，请勿重复启动。")
        return False

    if autohs_config.hearthstone_install_path == "":
        messagebox.showinfo("Warning", "请先设置炉石安装路径")
        return False

    if not check_hearthstone_path(autohs_config.hearthstone_install_path):
        return False

    if (autohs_config.width == 0 or autohs_config.height == 0):
        messagebox.showinfo("Warning", "请先设置屏幕分辨率")
        return False

    if (autohs_config.player_name == ""):
        messagebox.showinfo("Warning", "请先设置玩家名")
        return False

    if not test_hs_available() and not test_battlenet_available():
        messagebox.showinfo("Warning", "未找到炉石传说或战网，请至少打开一个")
        return False

    if autohs_config.max_win_count == 0 and autohs_config.max_play_time == 0:
        messagebox.showinfo("Warning", "警告：程序将无限制运行，可能导致账号被封。")

    mock_start_function()
    # start_function()

def add_label_and_entry(root, label_text, entry_text, bind_func):
    if not hasattr(add_label_and_entry, "row"):
        add_label_and_entry.row = 0
    else:
        add_label_and_entry.row += 1

    label = tk.Label(root, text=label_text)
    label.grid(row=add_label_and_entry.row, column=0, padx=10, pady=5, sticky="ew")
    entry = tk.Entry(root, width=20)
    entry.grid(row=add_label_and_entry.row, column=1, padx=10, pady=5, sticky="ew")
    entry.insert(0, entry_text)
    entry.bind("<Leave>", bind_func)
    entry.bind("<Return>", bind_func)

    return entry

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", close_gui)

    logger_init()

    autohs_config = AutoHSConfig()
    autohs_config.load_config()
    if autohs_config.width == 0:
        autohs_config.width = WIDTH
    if autohs_config.height == 0:
        autohs_config.height = HEIGHT

    root = tk.Tk()
    root.title("AutoHS GUI")
    root.geometry("500x340")
    root.protocol("WM_DELETE_WINDOW", close_gui)

    entry_width = add_label_and_entry(root, "游戏水平像素数：", autohs_config.width, update_width)
    entry_height = add_label_and_entry(root, "游戏垂直像素数：", autohs_config.height, update_height)
    entry_max_play_time = add_label_and_entry(root, "最大游戏时间(分钟)：", autohs_config.max_play_time, update_max_play_time)
    entry_max_win_count = add_label_and_entry(root, "最大胜利场次：", autohs_config.max_win_count, update_max_win_count)
    entry_path = add_label_and_entry(root, "炉石安装路径：\n(例：D:\\Hearthstone)", autohs_config.hearthstone_install_path, update_install_path)
    entry_player_name = add_label_and_entry(root, "玩家名：", autohs_config.player_name, update_player_name)

    start_button = tk.Button(root, text="开始", command=lambda: (update_all(), check_before_start()), width=20, height=1)
    start_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    exit_button = tk.Button(root, text="退出", command=close_gui, width=20, height=1)
    exit_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    save_button = tk.Button(root, text="保存配置", command=lambda: (update_all(), autohs_config.save_config()), width=20, height=1)
    save_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    if (WIDTH, HEIGHT) in ABNORMAL_WIDTH_HEIGHT_LIST:
        warning_label = tk.Label(root, text="警告：屏幕缩放比例疑似不为100%，\n可能导致程序异常", fg="red")
        warning_label.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

    hint_label = tk.Label(root, text="按Ctrl+Q可退出程序", fg="gray")
    hint_label.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

    modified_time_label = tk.Label(root, text=f"cards.json最后更新时间：\n{JSON_LAST_MODIFIED_TIME}", fg="gray")
    modified_time_label.grid(row=5, column=2, padx=10, pady=5, sticky="ew")

    root.mainloop()