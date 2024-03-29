import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from utils import get_cpu_info,get_ram_info,get_disk_info,get_gpu_info
FONT_SIZE=12
BAR_SIZE=700

def get_label_position(label):
    x = label.winfo_x()  # 获取控件相对于父容器的 x 坐标
    y = label.winfo_y()  # 获取控件相对于父容器的 y 坐标
    return x+20,y+20

def GuiMode():
    root = tk.Tk()
    root.title("Hardware Monitor")
    root.geometry("800x600")
    root.configure(bg="black")
    """time"""
    def update_time():
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_label.config(text=f"Time:  {current_time}")
        root.after(500, update_time)
        
    time_label =tk.Label(root, text=f"Time:  ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='white',bg="black")
    time_label.place(x=20,y=20)
    """cpu info"""
    cpu_label =tk.Label(root, text="CPU INFO:", 
                                font=("Arial", FONT_SIZE,"bold"),fg='red',bg="black")
    x_p,y_p=get_label_position(time_label)
    cpu_label.place(x=(x_p),y=(y_p+25))
    def updata_cpu_info():
        cpu_info = get_cpu_info()
        core_num=cpu_info['logical_cpu_count']
        current_freq=cpu_info['cpu_freq']
        current_freq="{:.2f}".format(current_freq)
        cpu_temp="{:.2f}".format(cpu_info['cpu_temp'])
        cpu_util="{:.2f}".format(cpu_info['cpu_percent'])
        cpu_info_label.config(text=f"Core_Count:  {core_num}   Freq:  {current_freq} GHZ   Used:{cpu_util} %   Temp:{cpu_temp} °C")
        root.after(500,updata_cpu_info)
    cpu_info_label = tk.Label(root, text=f"Core_Count:      Freq:   GHZ  TEMP:  °C ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='yellow',bg="black")
    x_p,y_p=get_label_position(cpu_label)
    cpu_info_label.place(x=20,y=70)
    """ram info"""
    ram_label =tk.Label(root, text="RAM INFO:", 
                                font=("Arial", FONT_SIZE,"bold"),fg='dodgerblue',bg="black")
    ram_label.place(x=20,y=95)
    ram_info_label =tk.Label(root, text=" ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='cyan',bg="black")
    ram_info_label.place(x=20,y=120)
    ram_used_label =tk.Label(root, text=" ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='cyan',bg="black")
    ram_used_label.place(x=720,y=145)
    ram_progress_bar = ttk.Progressbar(root, orient="horizontal", length=BAR_SIZE, mode="indeterminate")
    ram_progress_bar.place(x=20,y=145)
    def update_ram_info():
        ram_info=get_ram_info()
        ram_mem_total=ram_info["total"]
        ram_mem_used=ram_info["used"]
        scale=BAR_SIZE/ram_mem_total
        ram_progress_bar['value'] = 0
        ram_progress_bar.step(ram_mem_used*scale)
        used_p=(ram_mem_used/ram_mem_total)*100
        ram_mem_total="{:.1f}".format(ram_mem_total)
        ram_mem_used="{:.1f}".format(ram_mem_used)
        used_p="{:.2f}".format(used_p)
        ram_info_label.config(text=f'ram used: {ram_mem_used}GB/{ram_mem_total}GB')
        ram_used_label.config(text=f' {used_p}%')
        root.after(500, update_gpu_mem)
    """block info"""
    disk_label =tk.Label(root, text="DISK INFO:", 
                                font=("Arial", FONT_SIZE,"bold"),fg='magenta',bg="black")
    disk_label.place(x=20,y=170)
    disk_info_label =tk.Label(root, text=" ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='magenta',bg="black")
    disk_info_label.place(x=20,y=195)
    disk_mem_label =tk.Label(root, text=" ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='magenta',bg="black")
    disk_mem_label.place(x=20,y=220)
    disk_mem_used_label =tk.Label(root, text=" ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='magenta',bg="black")
    disk_mem_used_label.place(x=720,y=245)
    disk_progress_bar = ttk.Progressbar(root, orient="horizontal", length=BAR_SIZE, mode="indeterminate")
    disk_progress_bar.place(x=20,y=245)
    def update_disk_info():
        disk_infos=get_disk_info()
        for disk_info in disk_infos:
            if disk_info['mountpoint']=='/home':
                disk_mount_point=disk_info['mountpoint']
                disk_device=disk_info["device"]
                disk_fstype=disk_info['fstype']
                disk_total=disk_info['total']/(1024**3)
                disk_used=disk_info['used']/(1024**3)
        scale=BAR_SIZE/disk_total
        progress_bar['value'] = 0
        progress_bar.step(disk_used*scale)
        disk_used_p="{:.2f}".format((disk_used/disk_total)*100)
        disk_used="{:.2f}".format(disk_used)
        disk_total="{:.2f}".format(disk_total)
        disk_info_label.config(text=f'Mountpoint : {disk_mount_point}  FileSys : {disk_fstype}')
        disk_mem_label.config(text=f'mem used : {disk_used}GB / {disk_total}GB')
        disk_mem_used_label.config(text=f' {disk_used_p} %')

    """创建GPU显存进度条"""
    gpu_label =tk.Label(root, text="GPU INFO:", 
                                font=("Arial", FONT_SIZE,"bold"),fg='magenta',bg="black")
    gpu_label.place(x=20,y=270)
    gpu_info_label =tk.Label(root, text="ID :", 
                                font=("Arial", FONT_SIZE,"bold"),fg='deeppink',bg="black")
    gpu_info_label.place(x=20,y=295)
    gpu_mem_label = tk.Label(root, text=f"MEM:  ", 
                                font=("Arial", FONT_SIZE,"bold"),fg='orange',bg="black")
    gpu_mem_label.place(x=20,y=320)
    gpu_mem_used_label = tk.Label(root, text=f"", 
                                font=("Arial", FONT_SIZE,"bold"),fg='orange',bg="black")
    gpu_mem_used_label.place(x=720,y=345)
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=BAR_SIZE, mode="indeterminate")
    progress_bar.place(x=20,y=345)
    gpu_pwower_used_label = tk.Label(root, text=f"", 
                                font=("Arial", FONT_SIZE,"bold"),fg='orange',bg="black")
    gpu_pwower_used_label.place(x=20,y=370)
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=BAR_SIZE, mode="indeterminate")
    progress_bar.place(x=20,y=395)
    def update_gpu_mem():
        gpu_info = get_gpu_info()
        gpu_id=gpu_info[0]["id"]
        gpu_name=gpu_info[0]["name"]
        gpu_temp=gpu_info[0]["temperature"]
        gpu_memory_total=gpu_info[0]["memory_total"]
        gpu_memory_used=gpu_info[0]["memory_used"]
        gpu_mem_used_p=(gpu_memory_used/gpu_memory_total)*100
        scale=BAR_SIZE/gpu_memory_total
        gpu_memory_used="{:.2f}".format(gpu_memory_used)
        gpu_memory_total="{:.2f}".format(gpu_memory_total)
        gpu_mem_used_p="{:.2f}".format(gpu_mem_used_p)
        gpu_power_c=gpu_info[0]["gpu_power_c"]
        gpu_power_r=gpu_info[0]["gpu_power_r"]
        gpu_info_label.config(text=f'ID:{gpu_id}  Name: {gpu_name}  Temp: {gpu_temp} °C ')
        gpu_mem_label.config(text=f'mem used:  {gpu_memory_used} GB/{gpu_memory_total} GB')
        gpu_mem_used_label.config(text=f' {gpu_mem_used_p} %')
        progress_bar['value'] = 0
        progress_bar.step((gpu_info[0]["memory_used"])*scale)
        gpu_pwower_used_label.config(text=f'power consum {gpu_power_c} W/ {gpu_power_r} W')
        root.after(500, update_gpu_mem)

    """updata info"""
    update_time()
    updata_cpu_info()
    update_ram_info()
    update_disk_info()
    update_gpu_mem()
    # 运行主循环
    root.mainloop() 