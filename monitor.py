import tkinter as tk
from tkinter import ttk
import os
import sys
import time
from datetime import datetime
from prettytable import PrettyTable
from utils import get_cpu_info,get_ram_info,get_disk_info,get_gpu_info
os.chdir(sys.path[0])
FRSHTIME=1

def print_table(cpu_info,ram_info,disk_info,gpu_info):
    os.system('cls' if os.name == 'nt' else 'clear')  # 清空终端显示
    table = PrettyTable()
    header = ["GPU ID", "Name", "Memory Total (MB)", "Memory Used (MB)", "Memory Free (MB)", "Temperature (°C)"]
    table.field_names = header
    for gpu in gpu_info:
        table.add_row([gpu['id'], gpu['name'], gpu['memory_total'], gpu['memory_used'], gpu['memory_free'], gpu['temperature']])
    print(table)

def main():
    if len(sys.argv) != 2:
        print("Usage: python monitor.py arg(1-console 2-GUI) ")
        sys.exit(1)
    # 获取参数值
    arg = sys.argv[1]
    if arg=='1':
        while True:
            cpu_info = get_cpu_info()
            ram_info=get_ram_info()
            disk_info=get_disk_info()
            gpu_info = get_gpu_info()
            print_table(cpu_info,ram_info,disk_info,gpu_info)
            time.sleep(FRSHTIME) 
    elif arg=='2':
        root = tk.Tk()
        root.title("Hardware Monitor")
        root.geometry("800x600")
        root.configure(bg="black")
        ram_info=get_ram_info()
        disk_info=get_disk_info()
        gpu_info = get_gpu_info()
        """time"""
        def update_time():
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_label.config(text=f"Time:  {current_time}")
            root.after(500, update_time)
            
        time_label =tk.Label(root, text=f"Time:  ", 
                                   font=("Arial", 10,"bold"),fg='white',bg="black")
        time_label.place(x=20,y=20)
        """cpu info"""
        cpu_label =tk.Label(root, text="CPU INFO:", 
                                   font=("Arial", 10,"bold"),fg='green',bg="black")
        cpu_label.place(x=20,y=45)
        def updata_cpu_info():
            cpu_info = get_cpu_info()
            core_num=cpu_info['logical_cpu_count']
            current_freq="{:.2f}".format(cpu_info['cpu_freq'].current)
            cpu_temp="{:.2f}".format(cpu_info['cpu_temp'])
            cpu_util="{:.2f}".format(cpu_info['cpu_percent'])
            cpu_count_label.config(text=f"Core_Count:  {core_num}   Freq:  {current_freq} GHZ  TEMP:{cpu_temp} °C   USE:{cpu_util} %")
            root.after(500,updata_cpu_info)

        cpu_count_label = tk.Label(root, text=f"Core_Count:      Freq:   GHZ  TEMP:  °C ", 
                                   font=("Arial", 10,"bold"),fg='green',bg="black")
        cpu_count_label.place(x=20,y=70)

        # 创建GPU显存进度条
        gpu_mem_label = tk.Label(root, text=f"GPU MEM:  ", 
                                   font=("Arial", 10,"bold"),fg='red',bg="black")
        gpu_mem_label.place(x=20,y=95)
        gpu_memory_total=gpu_info[0]["memory_total"]
        scale=600/gpu_memory_total
        progress_bar = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
        progress_bar.place(x=120,y=95)

        def update_progress():
            progress_bar['value'] = 0
            progress_bar.step((gpu_info[0]["memory_used"])*scale)
            root.after(1000, update_progress)
        """updata info"""
        update_time()
        updata_cpu_info()
        update_progress()
        # 运行主循环
        root.mainloop() 
    else:
        print("please select console mode or GUI mode")

if __name__ == "__main__":
    main()
    

