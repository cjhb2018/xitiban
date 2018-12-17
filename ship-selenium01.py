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

#添加一下注释，测试
#再次测试一下
#第三次测试
#第四次测试
#第五次测试
#第六次测试
#第7次测试

driver = webdriver.Chrome()
wait=WebDriverWait(driver,3)

#通过selenium实现对中国船舶网的登录
def login():
    url = "http://sso.chinaports.com/authorize?urlState=shiptracker&response_type=code&redirect_uri=http%253A%252F%252Fwww.chinaports.com%252Fshiptracker%252Fshipinit.do%253Fmethod%253DgetToken&client_id=c1ebe466-1cdc-4bd3-ab69-77c3561b9dee&key=6810"
    # headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    driver.get(url)
    driver.find_element_by_name("username").send_keys("15815544173")
    driver.find_element_by_name("password").send_keys("cjhbzzrs")
    captcha=input("手动输入图像验证码：")
    driver.find_element_by_name("captcha").send_keys(captcha)

    driver.find_element_by_xpath('//*[@id="wizForm"]/div[5]/input').click()
    time.sleep(1)
    driver.save_screenshot("login.png")
    driver.find_element_by_xpath('//*[@id="link_login_1"]').click()
    # 点开船舶资料页面，并等待所有元素加载
    driver.find_element_by_xpath('//*[@id="layout_header"]/div[4]/ul/li[2]/a').click()
    # wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="my_content"]/tr[2]/td[1]')))


def get_data():
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)  # 与mongo连接
    db = client.ship  # 建立名为ship的数据库
    collection = db.chinaports  # 建立名为chinaports的collection
    #进入框架
    frame_location = driver.find_element_by_tag_name("iframe")
    driver.switch_to.frame(frame_location)
    # 获取所在页面的数据行数，根据行数来遍历数据
    index=driver.find_elements_by_xpath('//*[@id="my_content"]/tr[position()>0]')
    # print(type(index))
    print(len(index))
    driver.switch_to.default_content()

    for i in range(1,len(index)+1):
        frame_location = driver.find_element_by_tag_name("iframe")
        driver.switch_to.frame(frame_location)
        # time.sleep(1)

        Number=driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[1]').text
        EN_Name=driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[2]').text
        CN_Name=driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[3]').text
        Code=driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[4]').text
        IMO=driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[5]').text
        MMSI=driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[6]').text
        Nation=driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[7]').text

        # 打开定位信息
        driver.find_element_by_xpath('//*[@id="my_content"]/tr['+str(i)+']/td[8]/a').click()

        #退出frame框架
        driver.switch_to.default_content()

        #等待元素加载
        # time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[1]/td[2]')))
        #获取所需要信息
        Length=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[6]/td[2]').text
        Width=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[7]/td[2]').text
        Carry=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[8]/td[2]').text
        Weight=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[9]/td[2]').text
        Longitude=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[3]/td[4]').text
        Latitude=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[4]/td[4]').text
        Depth=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[8]/td[4]').text
        Update_time=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[9]/td[4]').text
        Type=driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[10]/td[4]').text

        #以字典形式获取所需要信息并传入MongoDB
        info = {
            "号码":Number,
            "英文船名": EN_Name,
            "中文船名": CN_Name,
            "呼号": Code,
            "IMO编号": IMO,
            "MMSI": MMSI,
            "国籍": Nation,
            "船长": Length,
            "船宽": Width,
            "载重吨": Carry,
            "总吨": Weight,
            "经度": Longitude,
            "纬度": Latitude,
            "吃水": Depth,
            "更新时间": Update_time,
            "船舶类型": Type,
        }
        collection.insert_one(info)
        print(info)
        #关闭定位小窗
        driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[1]/td/div/a').click()

def next_page(page_number):
    try:
        frame_location = driver.find_element_by_tag_name("iframe")
        driver.switch_to.frame(frame_location)
        # time.sleep(1)
        fanye=driver.find_element_by_xpath('//*[@id="page_div"]/a[last()]')
        fanye.click()
        time.sleep(1)
        page = driver.find_element_by_xpath('//*[@id="page_div"]/a[@class="on"]').text
        # print(type(page))
        # print(page)
        if page==str(page_number):
                print(str(page_number)+"页加载成功")
        else:
                time.sleep(1)
        driver.switch_to.default_content()
    except:
        driver.switch_to.default_content()
        next_page(page_number)

def main():
    print(datetime.datetime.now())
    begin=time.time()
    total = 2
    login()
    for i in range(1, total+1):
        if i == 1:
            get_data()
        else:
            next_page(i)
            get_data()
    print(datetime.datetime.now())
    end = time.time()
    print("跑完需要时间", (end - begin) / 60)

main()