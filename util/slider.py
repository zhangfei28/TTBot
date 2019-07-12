#coding:utf-8

import os
import requests
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains

#参考 jquery.easing 的源码 实现了三种 easeOut 缓动 函数
def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)

def ease_out_quart(x):
    return 1 - pow(1 - x, 4)

def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)

def get_tracks(distance, seconds, ease_func):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = eval(ease_func)
        offset = round(ease(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return offsets, tracks

def drag_and_drop(browser, offset,slider_btn_class_name,total_time=12,easing_func='ease_out_expo'):
    knob = browser.find_element_by_class_name(slider_btn_class_name)
    offsets, tracks = get_tracks(offset, total_time,easing_func)
    ActionChains(browser).click_and_hold(knob).perform()
    for x in tracks:
        ActionChains(browser).move_by_offset(x, 0).perform()
    ActionChains(browser).pause(0.5).release().perform()

def download_img(src,save_path):
    response = requests.get(src)
    with open(save_path,'wb') as f:
        f.write(response.content)

def save_cookie(path,content,mode='w'):
    with open(path,mode) as f:
        f.write(content)