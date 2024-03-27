import tkinter as tk
import os
import sys
import time
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
        cpu_info = get_cpu_info()
        ram_info=get_ram_info()
        disk_info=get_disk_info()
        gpu_info = get_gpu_info()
        cpu_count_label = tk.Label(root, text=f"Hardware status:{cpu_info['logical_cpu_count']}", 
                                   font=("Arial", 10),fg='red')
        cpu_count_label.place(x=20,y=20)
        # 运行主循环
        root.mainloop() 
    else:
        print("please select console mode or GUI mode")

if __name__ == "__main__":
    main()
    

