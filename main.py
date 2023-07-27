from comm import comm_init
from config import configs
import time

# 建立通信

while not comm_init():
    print(f"串口{configs.serial_port}通信失败, 等待重试")
    time.sleep(2000)


# 加载模型


