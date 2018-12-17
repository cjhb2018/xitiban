from selenium import webdriver
import requests
import re
import random
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pymongo
import datetime
from selenium.webdriver.chrome.options import Options
import itchat
import tesserocr
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import os

options = webdriver.ChromeOptions()
options.add_argument('--kiosk')
driver = webdriver.Chrome(options=options)
wait=WebDriverWait(driver,3,0.5)

#调整验证码格式并输入识别文本
def captcha_adjust():
    captcha=Image.open(r"C:\Users\lingrundong\Downloads\kaptcha.png")

    #转为灰度图，二值化去掉干扰线
    lim=captcha.convert("L")
    threshold = 165
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    bim = lim.point(table, '1')
    bim.save(r"C:\Users\lingrundong\Downloads\kaptcha02.png")
    time.sleep(1)

    # 去除干扰线
    im = Image.open(r"C:\Users\lingrundong\Downloads\kaptcha02.png")
    # 图像二值化
    data = im.getdata()
    w, h = im.size
    black_point = 0

    # 二值化去掉周围黑色点
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]

                # 判断上下左右的黑色像素点总个数
                if top_pixel < 10:
                    black_point += 1
                if left_pixel < 10:
                    black_point += 1
                if down_pixel < 10:
                    black_point += 1
                if right_pixel < 10:
                    black_point += 1
                if black_point < 1:
                    im.putpixel((x, y), 255)
                # print(black_point)
                black_point = 0

    im.save(r"C:\Users\lingrundong\Downloads\kaptcha03.png")
    time.sleep(1)

    #对边框上黑色像素点进行消除
    im = Image.open(r"C:\Users\lingrundong\Downloads\kaptcha03.png")
    # 图像二值化
    data = im.getdata()
    w, h = im.size
    black_point = 0

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if x < 2 or y < 2:
                im.putpixel((x - 1, y - 1), 255)
            if x > w - 3 or y > h - 3:
                im.putpixel((x + 1, y + 1), 255)

    im.save(r"C:\Users\lingrundong\Downloads\kaptcha04.png")


    captcha_adjusted=Image.open(r"C:\Users\lingrundong\Downloads\kaptcha04.png")
    time.sleep(1)

    #识别验证码文本并输出
    x=tesserocr.image_to_text(captcha_adjusted)
    print(x)
    return x

#截屏获取验证码
def captcha_screenshot():
    driver.get("http://sso.chinaports.com/authorize?urlState=shiptracker&response_type=code&redirect_uri=http%253A%252F%252Fwww.chinaports.com%252Fshiptracker%252Fshipinit.do%253Fmethod%253DgetToken&client_id=c1ebe466-1cdc-4bd3-ab69-77c3561b9dee&key=6810")
    driver.find_element_by_name("username").send_keys("15815544173")
    driver.find_element_by_name("password").send_keys("cjhbzzrs")
    driver.save_screenshot(r'C:\Users\lingrundong\Downloads\fullscreen.png')
    time.sleep(1)
    captcha = driver.find_element_by_xpath('//*[@id="img_captcha"]')

    left = captcha.location['x']
    top = captcha.location['y']
    captchaWidth = captcha.location['x'] + captcha.size['width']
    captchaHeight = captcha.location['y'] + captcha.size['height']

    picture = Image.open(r'C:\Users\lingrundong\Downloads\fullscreen.png')
    picture = picture.crop((left, top, captchaWidth, captchaHeight))
    picture.save(r'C:\Users\lingrundong\Downloads\kaptcha.png')


#反复尝试下载并输入尝试结果，如果没有正确，反复尝试
def main():
    try:
        captcha_screenshot()
        time.sleep(1)
        captcha_text=captcha_adjust()
        time.sleep(1)
        print(captcha_text)
        # captcha_mannual= input("手动输入图像验证码：")
        driver.find_element_by_name("captcha").send_keys(captcha_text)
        driver.find_element_by_xpath('//*[@id="wizForm"]/div[5]/input').click()
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout_header"]/div[4]/ul/li[2]/a')))
    except:
        driver.find_element_by_name("captcha").clear()
        os.remove(r'C:\Users\lingrundong\Downloads\fullscreen.png')
        os.remove(r'C:\Users\lingrundong\Downloads\kaptcha.png')
        os.remove(r'C:\Users\lingrundong\Downloads\kaptcha02.png')
        os.remove(r'C:\Users\lingrundong\Downloads\kaptcha03.png')
        os.remove(r'C:\Users\lingrundong\Downloads\kaptcha04.png')
        time.sleep(5)
        main()

main()