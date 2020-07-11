# -*- encoding=utf8 -*-
__author__ = "rbforelle"

from airtest.core.api import *
from airtest.report.report import simple_report
import time
import os
from pathlib import Path

HOME_DIR = os.path.split(os.path.realpath(__file__))[0].replace('\\','/') 
SNAPSHOT_DIR = HOME_DIR + '/log/截图'
print(SNAPSHOT_DIR)

#FIXME 这里的interval应该用绝对时间还是相对时间？
def wait_for_multi_pics(pics, timeout, interval):
    '''
    检测多张图片是否匹配成功，若匹配到任意一张，则中断返回位置
    '''
    time_start = int(time.time())
    time_end = time_start + timeout
    print("start: ", time_start)
    print("end:   ", time_end)
    
    while int(time.time()) <= time_end:
        # print("current_time: ",current_timetime_now)
        for pic_index, pic in enumerate(pics):
            pos = exists(pic)
            if pos is not False:
                return pic_index, pos
        sleep(interval)
    return False, False


def snapshot_with_current_time(SNAPSHOT_DIR, msg=""):
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
    snapshot_file = SNAPSHOT_DIR + '/' + time_stamp + '_' + msg + '.jpg'
    snapshot(filename = snapshot_file, msg=msg)

    
def start_mission():
    if exists(Template(r"resources/tpl1573508654681.png", record_pos=(0.392, 0.181), resolution=(1920, 1080))) is False:
        touch(Template(r"resources/tpl1573508769278.png", record_pos=(0.393, 0.182), resolution=(1920, 1080)))  # 如果没勾代理指挥，勾上
    touch(Template(r"resources/tpl1575440458919.png", record_pos=(0.418, 0.232), resolution=(1920, 1080)))

    touch(Template(r"resources/tpl1573427476434.png", record_pos=(0.361, 0.129), resolution=(1920, 1080))) 


def check_if_mission_finished(timeout_s):
    # 第一个计时器，等待游戏结束，20分钟
    time_start = int(time.time())

    while int(time.time()) < time_start + timeout_s:
        # print("current_time: ",current_timetime_now)
        if exists(Template(r"resources/tpl1576996835970.png", record_pos=(-0.106, -0.256), resolution=(1920, 1080))) is False:
            return True
        sleep(5)

    return False


def save_result_and_exit_mission(timeout_s):
    pics = [Template(r"resources/tpl1573427570782.png", record_pos=(-0.329, 0.21), resolution=(1920, 1080)),
                Template(r"resources/tpl1573438126181.png", record_pos=(0.091, -0.006), resolution=(1920, 1080)),
                Template(r"resources/tpl1576995675273.png", record_pos=(-0.009, 0.021), resolution=(1920, 1080)),
    ]
    msgs = ["行动奖励",
            "等级提升",
            "Warning"]

    # 第二个计时器，如果30秒内不退出程序，则说明出现错误
    time_start = int(time.time())
    max_click_count = 10
    click_count = 0

    while int(time.time()) < time_start + timeout_s:
        if click_count > max_click_count:
            # 如果多次重复点击仍然不能退到外面
            # 返回error
            snapshot_with_current_time(SNAPSHOT_DIR, "Error")  
            break

        for pic,msg in zip(pics, msgs):
            pos = exists(pic)
            if pos is not False:
                sleep(2.0)  # 等待画面稳定
                snapshot_with_current_time(SNAPSHOT_DIR, msg)
                touch(pos)
                click_count+=1
                break
        sleep(2.0)  # 等待跳转
        if exists(Template(r"resources/tpl1575440458919.png", record_pos=(0.418, 0.232), resolution=(1920, 1080))) is not False:
            break
    
def auto_arknights(run_times):
    for i in range(run_times):
        start_mission()
        sleep(60.0)  # 最小延时，至少等待60s才可能任务结束
        check_if_mission_finished(1200)  # 检查任务是否结束，timeout 20分钟，剿灭最多也就这么久
        save_result_and_exit_mission(30)  # 截图保存结果，退出到任务选择界面
            

auto_arknights(10)





