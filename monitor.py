import os
import GPUtil
import time
from prettytable import PrettyTable

def get_gpu_info():
    gpu_info = []
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_info.append({
            "id": gpu.id,
            "name": gpu.name,
            "memory_total": gpu.memoryTotal,
            "memory_used": gpu.memoryUsed,
            "memory_free": gpu.memoryFree,
            "temperature": gpu.temperature
        })
    return gpu_info

def print_gpu_table(gpu_info):
    os.system('cls' if os.name == 'nt' else 'clear')  # 清空终端显示
    table = PrettyTable()
    header = ["GPU ID", "Name", "Memory Total (MB)", "Memory Used (MB)", "Memory Free (MB)", "Temperature (°C)"]
    table.field_names = header
    for gpu in gpu_info:
        table.add_row([gpu['id'], gpu['name'], gpu['memory_total'], gpu['memory_used'], gpu['memory_free'], gpu['temperature']])
    print(table)

if __name__ == "__main__":
    while True:
        gpu_info = get_gpu_info()
        print_gpu_table(gpu_info)
        time.sleep(1)  # 1 秒钟刷新一次







# import psutil
# import GPUtil

# def get_cpu_info():
#     cpu_info = {
#         "cpu_count": psutil.cpu_count(),
#         "cpu_percent": psutil.cpu_percent(interval=1),
#         "cpu_temp": None
#     }
#     try:
#         temps = psutil.sensors_temperatures()
#         cpu_temp = temps['coretemp'][0].current  # Assuming 'coretemp' is the name of CPU temperature sensor
#         cpu_info['cpu_temp'] = cpu_temp
#     except Exception as e:
#         print("Failed to retrieve CPU temperature:", e)
#     return cpu_info

# def get_gpu_info():
#     gpu_info = []
#     gpus = GPUtil.getGPUs()
#     for gpu in gpus:
#         gpu_info.append({
#             "id": gpu.id,
#             "name": gpu.name,
#             "memory_total": gpu.memoryTotal,
#             "memory_used": gpu.memoryUsed,
#             "memory_free": gpu.memoryFree,
#             "temperature": gpu.temperature
#         })
#     return gpu_info

# if __name__ == "__main__":
#     while True:
#         cpu_info = get_cpu_info()
#         print("CPU Info:")
#         print(f"CPU Count: {cpu_info['cpu_count']}")
#         print(f"CPU Usage: {cpu_info['cpu_percent']}%")
#         print(f"CPU Temperature: {cpu_info['cpu_temp']}°C")

#         gpu_info = get_gpu_info()
#         print("\nGPU Info:")
#         for gpu in gpu_info:
#             print(f"GPU {gpu['id']} - {gpu['name']}")
#             print(f"  Memory Total: {gpu['memory_total']} MB")
#             print(f"  Memory Used: {gpu['memory_used']} MB")
#             print(f"  Memory Free: {gpu['memory_free']} MB")
#             print(f"  Temperature: {gpu['temperature']}°C")

