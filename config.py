from dataclasses import dataclass

@dataclass
class Config():

    def __init__(self):
        self.serial_port = '/dev/ttyUSB0'
        self.serial_baund_rate = 115200
        self.mock_mode = True   # 虚空调试
        self.we_are_red = True  # 红蓝队

configs = Config()