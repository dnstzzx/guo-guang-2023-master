from typing import List
import serial
from command import Command
from config import configs

ser: serial.Serial


def comm_init() -> bool:
    global ser
    ser = serial.Serial(configs.serial_port, configs.serial_baund_rate)
    if not ser.is_open():
        return False
    
    
    return True

def comm_send_str(data: str) -> bool:
    if not ser.is_open():
        print("串口发送失败: " + data)
        return False
    ser.write(data.encode())
    ser.flush()

def comm_send_cmds(cmds: List[Command]):
    s = ''.join(str(cmds))
    comm_send_str(s)
