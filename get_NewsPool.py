import os
import re
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from selenium import webdriver    # Selenium是一种自动化测试工具，爬虫中主要用来解决JavaScript渲染问题
from selenium.webdriver.chrome.options import Options    # 需要安装浏览器驱动，并将其加入环境变量

# 根据关键字获取新闻的url，返回url_list
# 关键字既可以是人，也可以是病毒
def get_NewsList_PengPai(keyword):
    start_time = time.time()
    chrome_options=Options()
    #设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    # 进入澎湃新闻搜索界面
    url = 'https://www.thepaper.cn/searchResult.jsp'
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(2)

    # 定位搜索框传入关键字
    # 定位到搜索框 //*[@id="hds_inp"]，并传入关键字
    
    driver.find_element_by_xpath('/html/body/div[7]/div[1]/div/div[1]/form/input[1]').send_keys(keyword)
    #  找到搜索按钮 //*[@id="search_key"]，并点击
    driver.find_element_by_xpath('/html/body/div[7]/div[1]/div/div[1]/form/input[5]').click()
    time.sleep(4)
    
    # 通过循环模拟下拉加载全部新闻并返回url_list
    curr_url_list_len = 0
    url_attribute_list = []
    for i in range(20):
        # i += 1
        time.sleep(3)
        
        # 定位到所有的搜索结果
        url_list = driver.find_elements_by_xpath('//div[@class="search_res"]/h2/a')
        if len(url_list) == curr_url_list_len:
            url_attribute_list = [url.get_attribute('href') for url in url_list]
            break
        else:
            curr_url_list_len = len(url_list)

        # 执行下滑操作（执行js操作，js注入）
        # js = 'scrollTo(0,document.body.scrollHeight)'
        js = 'scrollTo(0,{})'.format((i+1)*8000)
        driver.execute_script(js)

    # 关闭界面
    driver.quit()
    
    # 计算程序运行时间
    end_time = time.time()
    print('获取"{}"相关新闻{}条，耗时{}秒'.format(keyword, str(len(url_attribute_list)), str(end_time-start_time)))
    
    return url_attribute_list

def get_NewsList_Sina(keyword):
    start_time = time.time()
    chrome_options=Options()
    #设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # 进入新浪新闻搜索界面
    url = 'https://search.sina.com.cn/?t=news'
    driver.get(url)
    time.sleep(2)

    # 定位到搜索框，并传入关键字
    driver.find_element_by_xpath('//*[@id="tabc02"]/form/div/input[1]').send_keys(keyword)
    #  找到搜索按钮，并点击
    driver.find_element_by_xpath('//*[@id="tabc02"]/form/div/input[4]').click()
    
    # 通过循环模拟下拉加载全部新闻并返回url_list
    url_attribute_list = []
    for i in range(20):
        time.sleep(2)
        #定位到所有的搜索结果
        url_list = driver.find_elements_by_xpath('//*[@id="result"]//h2/a')
        url_attribute_list.extend([url.get_attribute('href') for url in url_list])
        
        # 下一页
        try:
            driver.find_element_by_xpath('//*[@id="_function_code_page"]/a[@title="下一页"]').click()
        except:
            break
    
    # 关闭浏览器
    driver.close()
    # 关闭webdriver进程
    driver.quit()
    # 计算程序运行时间
    end_time = time.time()
    print('获取"{}"相关新闻{}条，耗时{}秒'.format(keyword, str(len(url_attribute_list)), str(end_time-start_time)))
    
    return url_attribute_list

def get_NewsList_Baidu(keyword):
    start_time = time.time()
    chrome_options=Options()
    #设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    # 通过循环模拟下拉加载全部新闻并返回url_list
    url_attribute_list = []
    for i in range(20):
        time.sleep(2)
        # 下一页
        driver.get(f'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word={keyword}&pn={i*10}')
        #定位到所有的搜索结果
        #url_list = tree.xpath('/html/body/div/div[3]/div[1]/div[4]/div[2]/div/div/h3/a')
        url_list = driver.find_elements_by_xpath('/html/body/div/div[3]/div[1]/div[4]/div/div/h3/a')
        url_attribute_list.extend([url.get_attribute('href') for url in url_list])
        if(len(url_list)<8):
            break
    
    # 关闭浏览器
    driver.close()
    # 关闭webdriver进程
    driver.quit()
    # 计算程序运行时间
    end_time = time.time()
    print('获取"{}"相关新闻{}条，耗时{}秒'.format(keyword, str(len(url_attribute_list)), str(end_time-start_time)))
    
    return url_attribute_list

def get_NewsList(keyword, source):
    if source not in ['pengpai', 'sina', 'baidu']: return
    if source == 'pengpai':
        return get_NewsList_PengPai(keyword)
    elif source == 'sina':
        return get_NewsList_Sina(keyword)
    elif source == 'baidu':
        return get_NewsList_Baidu(keyword)