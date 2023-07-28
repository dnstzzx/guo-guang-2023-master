from typing import List, Tuple
import cv2
from cv2 import namedWindow
from comm import comm_init
from config import configs
from input import btn_mid, btn_set, btn_res
import time
from path import path_to_commands
from promise import Promise
from vision import deep
import treasure
import data
import dijkstra

from vision.camera import camera_init, get_camera_img

def main():
    # 建立通信

    # while not comm_init():
    #     print(f"串口{configs.serial_port}通信失败, 等待重试")
    #     time.sleep(2)


    # 启动相机
    while not camera_init():
        print("相机初始化失败,按MID重试")
        btn_mid.wait_for_released()

    # 初始化模型
    print("正在预热模型")
    try:
        img = cv2.imread('vision/sample.jpg')
        deep.recognize_treasure_map(img)
    except Exception as ex:
        print(ex)

    # 识图
    while True:
        rec_result: List[Tuple[int]] = []

        # 预览
        print("按下MID开始识别")
        cv2.namedWindow('识图预览')
        pms = Promise()
        btn_mid.add_released_promise(pms)
        while not pms.is_done:
            img = get_camera_img()
            rst = deep.recognize_treasure_map(img)
            points = rst.points if rst.check()[0] else []
            for x, y in points:
                pass
            cv2.imshow('识图预览', img)
            cv2.waitKey(34)

        # 尝试识图
        for _ in range(5):
            img = get_camera_img()
            try:
                rst = deep.recognize_treasure_map(img)
            except Exception:
                continue
            succ, msg = rst.check()
            if not succ:
                print('识别结果错误: ' + msg)
                continue
            rec_result = rst.points
            break

        if len(rec_result) == 0:
            continue

        # 确认结果
        print("识别结果为: " + str(rec_result))
        print("按下SET确认结果, 按下RESET重新识图")
        p_set = Promise()
        p_res = Promise()
        btn_set.add_released_promise(p_set)
        btn_res.add_released_promise(p_res)
        while (not p_set.is_done) and (not p_res.is_done):
            time.sleep(0.01)
        
        if p_res.is_done:
            print("识图结果已重置")
            continue

        # 保存宝藏信息
        treasure.treasures.clear()
        for i, j in rec_result:
            treasure.treasures[(i, j)] = treasure.Treasure(data.current_map.cell_of(i, j))
        break


    # 计算初始路径
    print("正在计算初始路径")
    curr_state = data.entry_point
    target = treasure.determine_treasure_order(curr_state, data.exit_point)[0]
    path = dijkstra.calc_path(curr_state, target)
    
    cmds =  path_to_commands(path)

    print(f"目标点: ({target.pos.x}, {target.pos.y})")
    print("按下MID出发")
    btn_mid.wait_for_released()
    print("出发")

    



if __name__ == '__main__':
    main()
