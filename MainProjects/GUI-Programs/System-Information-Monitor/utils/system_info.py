# System info utils
import platform
import psutil
import socket
from datetime import datetime
from typing import Dict, List, Any

class SystemInfo:
    @staticmethod
    def get_basic_info() -> Dict[str, str]:
        # Get basic system info
        return {
            'os': f"{platform.system()} {platform.release()}",
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': socket.gethostname(),
            'python': platform.python_version()
        }
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        # Get cpu info
        cpu_freq = psutil.cpu_freq()
        return {
            'physical_cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'current_freq': cpu_freq.current if cpu_freq else None,
            'max_freq': cpu_freq.max if cpu_freq else None,
            'usage_percent': psutil.cpu_percent(),
            'per_core_usage': psutil.cpu_percent(percpu=True)
        }
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        # Get memory info
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            'virtual': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            },
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        }
    
    @staticmethod
    def get_disk_info() -> List[Dict[str, Any]]:
        # Get disk information for all partitions
        partitions = psutil.disk_partitions()
        disk_info = []

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': (usage.used / usage.total) * 100
                })
            except PermissionError:
                continue

        return disk_info
    
    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        # Get network info
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_io_counters()

        interface_info = {}
        for interface, addresses in interfaces.items():
            interface_info[interface] = []
            for addr in addresses:
                interface_info[interface].append({
                    'family': addr.family.name,
                    'address': addr.address
                })

        return {
            'interfaces': interface_info,
            'stats': {
                'bytes_sent': stats.bytes_sent,
                'bytes_recv': stats.bytes_recv,
                'packets_sent': stats.packets_sent,
                'packets_recv': stats.packets_recv
            }
        }
    
    @staticmethod
    def get_processes() -> List[Dict[str, Any]]:
        # Get running processes info
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        return processes
    
    @staticmethod
    def get_uptime() -> str:
        # Get system uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        return f"{uptime.days} days, {uptime.seconds//3600} hours" # One hour is 3600 seconds
    
    @staticmethod
    def bytes_to_gb(bytes_val: int) -> float:
        # Converting bytes to gb
        return bytes_val / (1024 ** 3) # Bytes -> KB -> MB (1000MB)
