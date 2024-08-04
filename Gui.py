import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from utils import get_cpu_info, get_ram_info, get_disk_info, get_gpu_info

FONT_SIZE = 12
BAR_SIZE = 700
FRESHTIME = 50

def Process_Bar(canvas, fill_width):
    canvas.delete("progress")  # 清除之前的进度条
    canvas.create_rectangle(0, 0, BAR_SIZE, 20, fill="lightgray", outline="black", tags="progress")
    if fill_width <= (BAR_SIZE / 3):
        canvas.create_rectangle(0, 0, fill_width, 20, fill="springgreen", outline="", tags="progress")
    elif fill_width > (BAR_SIZE / 3) and fill_width <= ((2 * BAR_SIZE) / 3):
        canvas.create_rectangle(0, 0, fill_width, 20, fill="orange", outline="", tags="progress")
    else:
        canvas.create_rectangle(0, 0, fill_width, 20, fill="crimson", outline="", tags="progress")

def update_info_thread(func, *args):
    while True:
        func(*args)
        time.sleep(FRESHTIME / 1000)

def GuiMode():
    root = tk.Tk()
    root.title("Resource Monitor")
    root.geometry("820x750")
    root.configure(bg="black")

    """create frame"""
    time_frame = tk.Frame(root, bg="black", bd=2, relief=tk.GROOVE, width=770, height=40)
    time_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    cpu_frame = tk.Frame(root, bg="black", bd=2, relief=tk.GROOVE, width=770, height=60)
    cpu_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    ram_frame = tk.Frame(root, bg="black", bd=2, relief=tk.GROOVE, width=770, height=85)
    ram_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    disk_frame = tk.Frame(root, bg="black", bd=2, relief=tk.GROOVE, width=770, height=110)
    disk_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    gpu_frame = tk.Frame(root, bg="black", bd=2, relief=tk.GROOVE, width=770, height=600)
    gpu_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    """time"""
    time_label = tk.Label(time_frame, text=f"Time:", 
                                font=("Arial", FONT_SIZE, "bold"), fg='white', bg="black")
    time_label.place(x=10, y=10)
    
    def update_time():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_label.config(text=f"Time:  {current_time}")

    """cpu info"""
    cpu_label = tk.Label(cpu_frame, text="CPU infos:", 
                                font=("Arial", FONT_SIZE, "bold"), fg='tomato', bg="black")
    cpu_label.place(x=10, y=10)
    cpu_info_label = tk.Label(cpu_frame, text=f"Core_Count:      Freq:   GHZ  TEMP:  °C ", 
                                font=("Arial", FONT_SIZE, "bold"), fg='gold', bg="black")
    cpu_info_label.place(x=10, y=35)
    
    def update_cpu_info():
        cpu_info = get_cpu_info()
        core_num = cpu_info['logical_cpu_count']
        current_freq = cpu_info['cpu_freq']
        current_freq = "{:.2f}".format(current_freq)
        cpu_temp = "{:.2f}".format(cpu_info['cpu_temp'])
        cpu_util = "{:.2f}".format(cpu_info['cpu_percent'])
        cpu_info_label.config(text=f"Core_Count:  {core_num}   Freq:  {current_freq} GHZ   Used:{cpu_util} %   Temp:{cpu_temp} °C")

    """ram info"""
    ram_label = tk.Label(ram_frame, text="RAM infos:", 
                                font=("Arial", FONT_SIZE, "bold"), fg='dodgerblue', bg="black")
    ram_label.place(x=10, y=10)
    ram_info_label = tk.Label(ram_frame, text=" ", 
                                font=("Arial", FONT_SIZE, "bold"), fg='coral', bg="black")
    ram_info_label.place(x=10, y=35)
    ram_used_label = tk.Label(ram_frame, text=" ", 
                                font=("Arial", FONT_SIZE, "bold"), fg='yellow', bg="black")
    ram_used_label.place(x=710, y=60)
    ram_canvas = tk.Canvas(ram_frame, width=BAR_SIZE, height=20)
    ram_canvas.place(x=10, y=60)
    
    def update_ram_info():
        ram_info = get_ram_info()
        ram_mem_total = ram_info["total"]
        ram_mem_used = ram_info["used"]
        ram_scale = ram_mem_used / ram_mem_total
        fill_width = BAR_SIZE * ram_scale
        Process_Bar(ram_canvas, fill_width)
        used_p = (ram_mem_used / ram_mem_total) * 100
        ram_mem_total = "{:.1f}".format(ram_mem_total)
        ram_mem_used = "{:.1f}".format(ram_mem_used)
        used_p = "{:.2f}".format(used_p)
        ram_info_label.config(text=f'ram used: {ram_mem_used}GB / {ram_mem_total}GB')
        ram_used_label.config(text=f' {used_p}%')

    """block info"""
    disk_label = tk.Label(disk_frame, text="DISK infos:", 
                                font=("Arial", FONT_SIZE, "bold"), fg='lime', bg="black")
    disk_label.place(x=10, y=10)
    disk_info_label = tk.Label(disk_frame, text=" ", 
                                font=("Arial", FONT_SIZE, "bold"), fg='deeppink', bg="black")
    disk_info_label.place(x=10, y=35)
    disk_mem_label = tk.Label(disk_frame, text=" ", 
                                font=("Arial", FONT_SIZE, "bold"), fg='hotpink', bg="black")
    disk_mem_label.place(x=10, y=60)
    disk_mem_used_label = tk.Label(disk_frame, text=" ", 
                                font=("Arial", FONT_SIZE, "bold"), fg='yellow', bg="black")
    disk_mem_used_label.place(x=710, y=85)
    disk_canvas = tk.Canvas(disk_frame, width=BAR_SIZE, height=20)
    disk_canvas.place(x=10, y=85)
    
    def update_disk_info():
        disk_infos = get_disk_info()
        for disk_info in disk_infos:
            if disk_info['mountpoint'] == '/home':
                disk_mount_point = disk_info['mountpoint']
                disk_device = disk_info["device"]
                disk_fstype = disk_info['fstype']
                disk_total = disk_info['total'] / (1024**3)
                disk_used = disk_info['used'] / (1024**3)
        disk_scale = disk_used / disk_total
        fill_width = BAR_SIZE * disk_scale
        Process_Bar(disk_canvas, fill_width)
        disk_used_p = "{:.2f}".format((disk_used / disk_total) * 100)
        disk_used = "{:.2f}".format(disk_used)
        disk_total = "{:.2f}".format(disk_total)
        disk_info_label.config(text=f'Mountpoint : {disk_mount_point}  FileSys : {disk_fstype}')
        disk_mem_label.config(text=f'mem used : {disk_used}GB / {disk_total}GB')
        disk_mem_used_label.config(text=f' {disk_used_p} %')

    """GPU info"""
    gpu_info_labels = []
    gpu_mem_labels = []
    gpu_mem_used_labels = []
    gpu_mem_canvases = []
    gpu_power_used_labels = []
    gpu_consum_canvases = []
    gpu_power_used_label_ps = []

    def create_gpu_ui(gpu_idx):
        gpu_label = tk.Label(gpu_frame, text=f"GPU {gpu_idx} infos:", 
                                    font=("Arial", FONT_SIZE, "bold"), fg='magenta', bg="black")
        gpu_label.place(x=10, y=10 + gpu_idx * 160)
        gpu_info_label = tk.Label(gpu_frame, text="ID :", 
                                    font=("Arial", FONT_SIZE, "bold"), fg='deeppink', bg="black")
        gpu_info_label.place(x=10, y=35 + gpu_idx * 160)
        gpu_mem_label = tk.Label(gpu_frame, text=f"MEM:  ", 
                                    font=("Arial", FONT_SIZE, "bold"), fg='orange', bg="black")
        gpu_mem_label.place(x=10, y=60 + gpu_idx * 160)
        gpu_mem_used_label = tk.Label(gpu_frame, text=f"", 
                                    font=("Arial", FONT_SIZE, "bold"), fg='orange', bg="black")
        gpu_mem_used_label.place(x=710, y=60 + gpu_idx * 160)
        gpu_mem_canvas = tk.Canvas(gpu_frame, width=BAR_SIZE, height=20)
        gpu_mem_canvas.place(x=10, y=85 + gpu_idx * 160)
        gpu_power_used_label = tk.Label(gpu_frame, text=f"", 
                                        font=("Arial", FONT_SIZE, "bold"), fg='orange', bg="black")
        gpu_power_used_label.place(x=10, y=110 + gpu_idx * 160)
        gpu_consum_canvas = tk.Canvas(gpu_frame, width=BAR_SIZE, height=20)
        gpu_consum_canvas.place(x=10, y=135 + gpu_idx * 160)
        gpu_power_used_label_p = tk.Label(gpu_frame, text=f"", 
                                          font=("Arial", FONT_SIZE, "bold"), fg='orange', bg="black")
        gpu_power_used_label_p.place(x=710, y=135 + gpu_idx * 160)

        gpu_info_labels.append(gpu_info_label)
        gpu_mem_labels.append(gpu_mem_label)
        gpu_mem_used_labels.append(gpu_mem_used_label)
        gpu_mem_canvases.append(gpu_mem_canvas)
        gpu_power_used_labels.append(gpu_power_used_label)
        gpu_consum_canvases.append(gpu_consum_canvas)
        gpu_power_used_label_ps.append(gpu_power_used_label_p)

    def update_gpu_info():
        gpu_info = get_gpu_info()
        for idx in range(len(gpu_info)):  # 假设有多个 GPU
            if idx >= len(gpu_info_labels):
                create_gpu_ui(idx)

            gpu_id = gpu_info[idx]["id"]
            gpu_name = gpu_info[idx]["name"]
            gpu_temp = gpu_info[idx]["temperature"]
            gpu_memory_total = gpu_info[idx]["memory_total"]
            gpu_memory_used = gpu_info[idx]["memory_used"]
            gpu_power_c = gpu_info[idx]["gpu_power_c"]
            gpu_power_r = gpu_info[idx]["gpu_power_r"]
            gpu_mem_used_p = (gpu_memory_used / gpu_memory_total) * 100
            gpu_mem_scale = gpu_memory_used / gpu_memory_total
            """GPU mem bar"""
            fill_width = BAR_SIZE * gpu_mem_scale
            Process_Bar(gpu_mem_canvases[idx], fill_width)
            gpu_memory_used = "{:.2f}".format(gpu_memory_used)
            gpu_memory_total = "{:.2f}".format(gpu_memory_total)
            gpu_mem_used_p = "{:.2f}".format(gpu_mem_used_p)
            gpu_info_labels[idx].config(text=f'ID:{gpu_id}  Name: {gpu_name}  Temp: {gpu_temp} °C ')
            gpu_mem_labels[idx].config(text=f'mem used:  {gpu_memory_used} GB / {gpu_memory_total} GB')
            gpu_mem_used_labels[idx].config(text=f' {gpu_mem_used_p} %')
            gpu_power_used_labels[idx].config(text=f'power consum {gpu_power_c} W / {gpu_power_r} W')
            power_p = "{:.2f}".format((gpu_power_c / gpu_power_r) * 100)
            gpu_power_used_label_ps[idx].config(text=f' {power_p} %')
            gpu_consum_scale = gpu_power_c / gpu_power_r

            """GPU power bar"""
            fill_width = BAR_SIZE * gpu_consum_scale
            Process_Bar(gpu_consum_canvases[idx], fill_width)

    """create and start threads"""
    time_thread = threading.Thread(target=update_info_thread, args=(update_time,))
    cpu_thread = threading.Thread(target=update_info_thread, args=(update_cpu_info,))
    ram_thread = threading.Thread(target=update_info_thread, args=(update_ram_info,))
    disk_thread = threading.Thread(target=update_info_thread, args=(update_disk_info,))
    gpu_thread = threading.Thread(target=update_info_thread, args=(update_gpu_info,))

    time_thread.start()
    cpu_thread.start()
    ram_thread.start()
    disk_thread.start()
    gpu_thread.start()

    # 运行主循环
    root.mainloop()

GuiMode()
