import os
import sys
import time
from prettytable import PrettyTable
from utils import get_cpu_info,get_ram_info,get_disk_info,get_gpu_info
FRSHTIME=1

def print_table(cpu_info,ram_info,disk_info,gpu_info):
    os.system('cls' if os.name == 'nt' else 'clear')  # 清空终端显示
    table = PrettyTable()
    header = ["GPU ID", "Name", "Memory Total (MB)", "Memory Used (MB)", "Memory Free (MB)", "Temperature (°C)"]
    table.field_names = header
    for gpu in gpu_info:
        table.add_row([gpu['id'], gpu['name'], gpu['memory_total'], gpu['memory_used'], gpu['memory_free'], gpu['temperature']])
    print(table)
def ConsoleMode():
    while True:
            cpu_info = get_cpu_info()
            ram_info=get_ram_info()
            disk_info=get_disk_info()
            gpu_info = get_gpu_info()
            print_table(cpu_info,ram_info,disk_info,gpu_info)
            time.sleep(FRSHTIME) 