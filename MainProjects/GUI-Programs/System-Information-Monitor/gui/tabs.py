# Individual tab classes for displaying system info
from PyQt5.QtWidgets import QTextEdit, QPushButton, QVBoxLayout, QFrame
from PyQt5.QtGui import QFont
from gui.base_tab import BaseTab
from gui.components import ComponentFactory
from utils.system_info import SystemInfo

class OverviewTab(BaseTab):
    def __init__(self):
        super().__init__("Overview")
        self.setup_static_content()
        self.quick_stats_layout = None

    def setup_static_content(self):
        # System info
        self.add_section("System Information")
        system_info = SystemInfo.get_basic_info()

        for key, value in system_info.items():
            self.add_info_row(key.replace('-', ' ').title(), value)
        
        # Quick stats section
        self.add_section("Quick Stats")
        self.quick_stats_layout = QVBoxLayout()
        self.content_layout.addLayout(self.quick_stats_layout)

    def update_content(self):
        if self.quick_stats_layout:
            ComponentFactory.clear_layout(self.quick_stats_layout)

            # Cpu usage
            cpu_info = SystemInfo.get_cpu_info()
            cpu_bar = ComponentFactory.create_progress_bar("CPU Usage", cpu_info['usage_percent'])
            self.quick_stats_layout.addWidget(cpu_bar)

            # Memory usage
            memory_info = SystemInfo.get_memory_info()
            memory_bar = ComponentFactory.create_progress_bar("Memory Usage", memory_info['virtual']['percent'])
            self.quick_stats_layout.addWidget(memory_bar)

            # System uptime
            uptime_row = ComponentFactory.create_info_row("Uptime", SystemInfo.get_uptime())
            self.quick_stats_layout.addWidget(uptime_row)

class CPUTab(BaseTab):
    def __init__(self):
        super().__init__("CPU")
        self.setup_static_content()
        self.cpu_usage_layout = None

    def setup_static_content(self):
        # CPU Information
        self.add_section("CPU Information")
        cpu_info = SystemInfo.get_cpu_info()

        self.add_info_row("Physical Cores", str(cpu_info['physical_cores']))
        self.add_info_row("Logical Cores", str(cpu_info['logical_cores']))

        if cpu_info['current_freq']:
            self.add_info_row("Base Frequency", f"{cpu_info['current_freq']:.2f} MHz")
        if cpu_info['max_freq']:
            self.add_info_row("Max Frequency", f"{cpu_info['max_freq']:.2f} MHz")

        # CPU Usage section
        self.add_section("CPU Usage")
        self.cpu_usage_layout = QVBoxLayout()
        self.content_layout.addLayout(self.cpu_usage_layout)

    def update_content(self):
        if self.cpu_usage_layout:
            ComponentFactory.clear_layout(self.cpu_usage_layout)

            cpu_info = SystemInfo.get_cpu_info()

            # Overall CPU usage
            overall_bar = ComponentFactory.create_progress_bar("Overall CPU", cpu_info['usage_percent'])
            self.cpu_usage_layout.addWidget(overall_bar)

            # Per-core usage
            for i, percent in enumerate(cpu_info['per_core_usage']):
                core_bar = ComponentFactory.create_progress_bar(f"Core {i+1}", percent)
                self.cpu_usage_layout.addWidget(core_bar)

class MemoryTab(BaseTab):
    def __init__(self):
        super().__init__("Memory")
        self.memory_layout = None
        self.swap_layout = None
        self.setup_content()

    def setup_content(self):
        # Memory info
        self.add_section("Memory Information")
        self.memory_layout = QVBoxLayout()
        self.content_layout.addLayout(self.memory_layout)

        # Swap info
        self.add_section("Swap Information")
        self.swap_layout = QVBoxLayout()
        self.content_layout.addLayout(self.swap_layout)

    def update_content(self):
        if self.memory_layout and self.swap_layout:
            ComponentFactory.clear_layout(self.memory_layout)
            ComponentFactory.clear_layout(self.swap_layout)

            memory_info = SystemInfo.get_memory_info()

            # Memory info
            memory = memory_info['virtual']
            self.memory_layout.addWidget(ComponentFactory.create_info_row("Total", f"{SystemInfo.bytes_to_gb(memory['total']):.2f} GB"))
            self.memory_layout.addWidget(ComponentFactory.create_info_row("Available", f"{SystemInfo.bytes_to_gb(memory['available']):.2f} GB"))
            self.memory_layout.addWidget(ComponentFactory.create_info_row("Used", f"{SystemInfo.bytes_to_gb(memory['used']):.2f} GB"))
            self.memory_layout.addWidget(ComponentFactory.create_progress_bar("Usage", memory['percent']))

            # Swap info
            swap = memory_info['swap']
            self.swap_layout.addWidget(ComponentFactory.create_info_row("Total", f"{SystemInfo.bytes_to_gb(swap['total']):.2f} GB"))
            self.swap_layout.addWidget(ComponentFactory.create_info_row("Used", f"{SystemInfo.bytes_to_gb(swap['used']):.2f} GB"))
            self.swap_layout.addWidget(ComponentFactory.create_info_row("Free", f"{SystemInfo.bytes_to_gb(swap['free']):.2f} GB"))
            if swap['total'] > 0:
                self.swap_layout.addWidget(ComponentFactory.create_progress_bar("Usage", swap['percent']))

class DiskTab(BaseTab):
    def __init__(self):
        super().__init__("Desk")
        self.disk_layout = None
        self.setup_content()

    def setup_content(self):
        self.add_section("Disk Usage")
        self.disk_layout = QVBoxLayout()
        self.content_layout.addLayout(self.disk_layout)

    def update_content(self):
        if self.disk_layout:
            ComponentFactory.clear_layout(self.disk_layout)

            disk_info = SystemInfo.get_disk_info()

            for disk in disk_info:
                frame, frame_layout = ComponentFactory.create_info_frame("")

                frame_layout.addWidget(ComponentFactory.create_info_row("Device", disk['device']))
                frame_layout.addWidget(ComponentFactory.create_info_row("Mountpoint", disk['mountpoint']))
                frame_layout.addWidget(ComponentFactory.create_info_row("File System", disk['fstype']))
                frame_layout.addWidget(ComponentFactory.create_info_row("Total", f"{SystemInfo.bytes_to_gb(disk['total']):.2f} GB"))
                frame_layout.addWidget(ComponentFactory.create_info_row("Used", f"{SystemInfo.bytes_to_gb(disk['used']):.2f} GB"))
                frame_layout.addWidget(ComponentFactory.create_info_row("Free", f"{SystemInfo.bytes_to_gb(disk['free']):.2f} GB"))
                frame_layout.addWidget(ComponentFactory.create_progress_bar("Usage", disk['percent']))

                self.disk_layout.addWidget(frame)

class NetworkTab(BaseTab):
    def __init__(self):
        super().__init__("Network")
        self.network_layout = None
        self.network_stats_layout = None
        self.setup_content()

    def setup_content(self):
        # Network interfaces
        self.add_section("Network Interfaces")
        self.network_layout = QVBoxLayout()
        self.content_layout.addLayout(self.network_layout)

        # Network statistics
        self.add_section("Network Statistics")
        self.network_stats_layout = QVBoxLayout()
        self.content_layout.addLayout(self.network_stats_layout)

    def update_content(self):
        if self.network_layout and self.network_stats_layout:
            ComponentFactory.clear_layout(self.network_layout)
            ComponentFactory.clear_layout(self.network_stats_layout)

            network_info = SystemInfo.get_network_info()

            # Network interfaces
            for interface, addresses in network_info['interfaces'].items():
                frame, frame_layout = ComponentFactory.create_info_frame(f"Interface: {interface}")

                for addr in addresses:
                    frame_layout.addWidget(ComponentFactory.create_info_row(addr['family'], addr['address']))

                self.network_layout.addWidget(frame)

            # Network statistics
            stats = network_info['stats']
            self.network_stats_layout.addWidget(ComponentFactory.create_info_row("Bytes Sent", f"{SystemInfo.bytes_to_gb(stats['bytes_sent']):.2f} GB"))
            self.network_stats_layout.addWidget(ComponentFactory.create_info_row("Bytes Received", f"{SystemInfo.bytes_to_gb(stats['bytes_recv']):.2f} GB"))
            self.network_stats_layout.addWidget(ComponentFactory.create_info_row("Packets Sent", f"{stats['packets_sent']:,}"))
            self.network_stats_layout.addWidget(ComponentFactory.create_info_row("Packets Received", f"{stats['packets_recv']:,}"))

class ProcessesTab(BaseTab):
    def __init__(self):
        super().__init__("Processes")
        self.setup_content()

    def setup_content(self):
        # Override the base setup to use regular layout and not scroll !
        self.setLayout(QVBoxLayout())

        # Refresh button
        refresh_btn = QPushButton("Refresh Processes")
        refresh_btn.clicked.connect(self.update_content)
        self.layout().addWidget(refresh_btn)

        # Process info
        self.process_text = QTextEdit()
        self.process_text.setReadOnly(True)
        self.process_text.setFont(QFont("Courier New", 10))
        self.layout().addWidget(self.process_text)

        # Initial update
        self.update_content()

    def update_content(self):
        processes = SystemInfo.get_processes()

        # Format output
        text = f"{'PID':<8} {'Name':<25} {'CPU%':<8} {'Memory%':<8}\n"
        text += "=" * 60 + "\n"

        for proc in processes[:50]:   # Show the 50 top processes
            text += f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['cpu_percent'] or 0:<8.1f} {proc['memory_percent'] or 0:<8.1f}\n"

        self.process_text.setText(text)
