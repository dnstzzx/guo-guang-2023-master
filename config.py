from dataclasses import dataclass

@dataclass
class Config():

    def __init__(self):
        self.serial_port = ''
        self.serial_baund_rate = 115200

configs = Config()