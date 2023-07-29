import threading
from typing import Union
import time
from typing import List
import serial
from command import Command
from config import configs
from promise import Promise
import report

ser: serial.Serial

def process_raw_rpt(l) -> Union[report.Report, None]:
    if '<<<' in l and '>>>' in l:
        try:
            raw = l.split('<<<')[1].split('>>>')[0]
        except Exception:
            return None
        segs = raw.split(':')
        name = segs[0]
        args = segs[1:] if len(segs) > 1 else []
        rpt = report.Report(name, args)
        report.on_report_recv(rpt)

def comm_recv_task():
    while True:
        l = ser.readline().decode()
        process_raw_rpt(l)

def mock_input_task():
    while True:
        l = input()
        process_raw_rpt(f"<<<{l.replace(' ', ':')}>>>")

def comm_init() -> bool:
    global ser
    threading.Thread(target=mock_input_task).start()
    if configs.mock_mode:
        return True
    try:
        ser = serial.Serial(configs.serial_port, configs.serial_baund_rate)
        if not ser.is_open:
            return False
    except Exception as ex:
        print(ex)
        return False
    threading.Thread(target=comm_recv_task).start()
    return True

def comm_send_str(data: str) -> bool:
    if not configs.mock_mode:
        if not ser.is_open:
            print("串口发送失败: " + data)
            return False
        ser.write(data.encode())
        ser.flush()
    print('sent command: ' + data)

def comm_send_cmds(cmds: List[Command]):
    s = ''.join([str(cmd) for cmd in cmds])
    comm_send_str(s)


snd_count = 0
# returns 是否成功，False即认为返回起点
def comm_send_cmds_and_wait(cmds: List[Command]) -> bool:
    global snd_count
    snd_count += 1
    echo_cmd = Command('ECHO', ['CPLT', str(snd_count)])
    p_cplt = Promise()
    p_locked = Promise()
    report.add_report_promise('CPLT', p_cplt)
    report.add_report_promise('LOCKED', p_locked)
    comm_send_cmds(cmds + [echo_cmd])
    while (not p_cplt.is_done) and (not p_locked.is_done):
        time.sleep(0.001)
    return not p_locked.is_done
    
    
    