import GPUtil
import psutil
import subprocess

FRSHTIME=1

def get_cpu_info():
    # 获取每个逻辑CPU核心的使用率
    cpu_temp = psutil.sensors_temperatures()
    if 'coretemp' in cpu_temp:
        core_temp = cpu_temp['coretemp']
        # 计算总的 CPU 温度
        per_cpu_temp = sum(sensor.current for sensor in core_temp) / len(core_temp)
    cpu_percents=psutil.cpu_percent(percpu=True,interval=FRSHTIME)
    per_cpu_util=sum(cpu_percent*10 for cpu_percent in cpu_percents)/len(cpu_percents)
    cpu_freq=psutil.cpu_freq().current
    cpu_info = {
            "logical_cpu_count": psutil.cpu_count(logical=False),
            "cpu_freq":cpu_freq/1000,
            "cpu_percent": per_cpu_util,
            "cpu_temp": per_cpu_temp
        }
    return cpu_info

def get_ram_info():
    # 获取系统内存信息
    mem_info = psutil.virtual_memory()
    ram_info = {
        "total": mem_info.total/(1024*1024*1024),    # 总内存
        "available": mem_info.available,  # 可用内存
        "percent": mem_info.percent,      # 内存使用百分比
        "used": mem_info.used/(1024*1024*1024),            # 已使用内存
        "free": mem_info.free             # 空闲内存
    }
    return ram_info

def get_disk_info():
    disk_info = []
    # 获取所有磁盘分区的信息
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        # 获取磁盘分区的使用情况
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            "device": partition.device,            # 设备名称
            "mountpoint": partition.mountpoint,    # 挂载点
            "fstype": partition.fstype,            # 文件系统类型
            "total": usage.total,                  # 总容量
            "used": usage.used,                    # 已使用容量
            "free": usage.free,                    # 可用容量
            "percent": usage.percent               # 使用百分比
        })
    return disk_info

def get_gpu_power_c():
    try:
        current_p = subprocess.check_output(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'])
        gpu_power_c = float(current_p.strip())
        return gpu_power_c
    except Exception as e:
        print("Error while getting GPU power:", e)
        return None
def get_gpu_power_r():
    try:
        current_p = subprocess.check_output(['nvidia-smi', '--query-gpu=power.limit', '--format=csv,noheader,nounits'])
        gpu_power_c = float(current_p.strip())
        return gpu_power_c
    except Exception as e:
        print("Error while getting GPU power:", e)
        return None
    
def get_gpu_info():
    gpu_info = []
    gpus = GPUtil.getGPUs()
    gpu_power_c=get_gpu_power_c()
    gpu_power_r=get_gpu_power_r()
    if gpu_power_c > gpu_power_r:
            gpu_power_c=gpu_power_r
    for gpu in gpus:
        gpu_info.append({
            "id": gpu.id,
            "name": gpu.name,
            "driver": gpu.driver,
            "memory_total": gpu.memoryTotal/1024,
            "memory_used": gpu.memoryUsed/1024,
            "memory_free": gpu.memoryFree/1024,
            "temperature": gpu.temperature,
            "gpu_power_c":gpu_power_c,
            "gpu_power_r":gpu_power_r
        })
    return gpu_info