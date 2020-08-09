# 使用 requests 或 Selenium 模拟登录石墨文档 https://shimo.im

from selenium import webdriver
import time


try:
    browser = webdriver.Chrome()
    browser.get('https://shimo.im')
    time.sleep(1)

    btm1 = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    btm1.click()
    time.sleep(1)


    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys("username")  #用户改成实际用户
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys("password")  #密码改成实际密码
    time.sleep(1)

    login_btn_2 =browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
    login_btn_2.click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
except Exception as e:
    print (e)
finally:
    browser.close()
    # pass


