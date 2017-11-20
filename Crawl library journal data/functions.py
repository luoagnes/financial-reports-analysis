# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select

import sys     
reload(sys) 
sys.setdefaultencoding('utf-8')


def get_browser_driver():
   driver= webdriver.Chrome(executable_path='C:\Python27\chromedriver.exe')
   print 'get the browser driver successfully!----------'
   return driver


def login(driver):
   driver.get('http://www.fenqubiao.com/')
   driver.find_element_by_id('Username').send_keys('szu')
   driver.find_element_by_id('Password').send_keys('123456')
   driver.find_element_by_id('login_button').click()
   print 'login successfully!------------'
   return True
   

def config_form(driver, i):
    
    Select(driver.find_element_by_id("ContentPlaceHolder1_dplCategoryType")).select_by_value('0')  ### 0 is the big class, 1 is the small class
    
    Select(driver.find_element_by_id("ContentPlaceHolder1_dplCategory")).select_by_index(i)
    
    driver.find_element_by_id("ContentPlaceHolder1_btnSearch").click()
    driver.implicitly_wait(30)
    time.sleep(3)
    driver.find_element_by_id("ContentPlaceHolder1_btnSearch").click()
    time.sleep(2)
    driver.find_element_by_id("ContentPlaceHolder1_btnSearch").click()
    return True



### 拉动滚动条到网页末尾
def scroll(driver):  
    driver.execute_script("""   
        (function () {   
            var y = document.body.scrollTop;   
            var step = 100;   
            window.scroll(0, y);   
  
  
            function f() {   
                if (y < document.body.scrollHeight) {   
                    y += step;   
                    window.scroll(0, y);   
                    setTimeout(f, 50);   
                }  
                else {   
                    window.scroll(0, y);   
                    document.title += "scroll-done";   
                }   
            }   
  
  
            setTimeout(f, 1000);   
        })();   
        """)  
