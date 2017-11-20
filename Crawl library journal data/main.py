# -*- coding: utf-8 -*-
import time
import re
import signal
from functions import get_browser_driver, login, config_form, scroll
from handle_data import save_pkl, load_pkl, save_excel0
import sys     
reload(sys) 
sys.setdefaultencoding('utf-8')

   
def get_first_level_form(driver):  ### get the first level page content which are between table/tbody
    content=driver.find_element_by_xpath('//table/tbody').text
    return content.split('\n')

def handle_one_record(record):  ## handle one line of table
    temp=record.split()         ### split by blank space
    
    if temp[-4]=='Y':           ### whether there is a review
        name_str='_'.join(temp[1:-4])
        name=''.join(temp[1:-4])
        Review=temp[-4]
    else:
        name=''.join(temp[1:-3])
        name_str='_'.join(temp[1:-3])
        Review='#NA'
    
    district=temp[-3]
    IF=temp[-2]
    aclass=temp[-1].split('___')
    avg_IF=aclass[0]
    class_str=aclass[1]
    id=temp[0]
    
    return [[id, name, Review, district, IF, avg_IF, class_str], name_str]
      

def handle_second_level_page(jurnal, driver):
    
    ###------------ready for complete link------------###
    temp=jurnal.split('_')
    suffix='%20'.join(temp)
    path='http://www.fenqubiao.com/Core/JournalDetail.aspx?y=2016&t='+suffix
    
    ### redirect to the new page-------------### 
    driver.get(path)
    driver.implicitly_wait(20)
    time.sleep(3)
    
    ### get the new page content which in table--------###
    obj=driver.find_element_by_xpath('//table')
    
    ### handle the content----------------###
    if obj:
        content=obj.text
    lines=content.split('\n')
    ISSN=lines[1].split()[-1]
    small_class=''.join(lines[4].split()[1:-2])
    
    print 'handle second level page successfully !-----------------------'
    return [ISSN, small_class]

        
def get_page_num(driver):   ### get the number of pages when the form selected as the way 
    
    href_content=driver.find_element_by_link_text(u'尾页').get_attribute('href')
    
    temp=href_content.split(',')[-1]
    page_num=int(temp.split(')')[0].replace("'", ''))
    print 'the page num is ', page_num, '-------------'
    return page_num

def switch_page(i, driver):  ### redirect to the next page
    driver.implicitly_wait(30)
    driver.find_element_by_link_text(str(i)).click()
    driver.implicitly_wait(30)
    return True
    

def each_page(driver, class_str, final_data):  ### handle a single page
    
    jurnal_list=get_first_level_form(driver)
    
    for jurnal in jurnal_list:
        obj=jurnal
        obj +='___'+class_str
        final_data.append(obj)
    return True


def handle_all_first_form():   
    all_fournal_name={}
    first_level_records={}
    
    ###----read first level page data----------##
    obj=open('all_data.txt', 'rb')
    lines=obj.readlines()
    obj.close()
    
    for line in lines:
        
        if len(line.strip())==0:
            continue
        try:
            temp=line.strip().split()
            if temp[-4]=='Y':
                name_str='_'.join(temp[1:-4])
                name=''.join(temp[1:-4])
                Review=temp[-4]
            else:
                name=''.join(temp[1:-3])
                name_str='_'.join(temp[1:-3])
                Review='--'
    
            district=temp[-3]
            IF=temp[-2]
            aclass=temp[-1].split('___')
            avg_IF=aclass[0]
            class_str=aclass[1]
            ID=temp[0]
            temp_record=[ID, name, Review, district, IF, avg_IF, class_str]
            
        except Exception:
            print 'handle this line error: ', line
            temp_record=[]
            name_str='###'
            
            
        all_fournal_name[name_str]=[]
        first_level_records[name_str]=temp_record
        
    path='all_fournal_name.pkl'
    save_pkl(path, all_fournal_name)
    
    path='first_level_reocrds.pkl'
    save_pkl(path, first_level_records)  
    return

def get_second_form_records():
    
    driver=get_browser_driver()
    login(driver)
    driver.implicitly_wait(15)
    
    path='all_fournal_name.pkl'
    all_fournal_name=load_pkl(path)
    
    error_journal=[]
    for journal in all_fournal_name.keys():
        if journal=='###' or journal=='':
            continue
        try:
            all_fournal_name[journal]=handle_second_level_page(journal, driver)
            time.sleep(3)
        except Exception:
            error_journal.append(journal)
            
    path='all_fournal_issn.pkl'
    save_pkl(path, all_fournal_name)
    
    path1='error_journal.pkl'
    save_pkl(path1, error_journal)

        
def get_first_level_page_data():

    ####-------------------准备页面--------------################
    driver=get_browser_driver()
    
    login(driver)
    driver.implicitly_wait(15)
    driver.find_element_by_id("ContentPlaceHolder1_btnSearch").click()
    driver.implicitly_wait(30)
    time.sleep(2)
    
    #### ----------------准备页面完毕---------------################
    final_data=[]
    error_class_list=[]
    for i in range(7):
        #class_str=u'地学天文'
        #time.sleep(10)
        try:
            config_form(driver, i)
            driver.implicitly_wait(30)
        
            text=driver.find_element_by_id("ContentPlaceHolder1_lblMessage").text   ### judge the number of journal
            num_journals=int(re.findall(u'(\d+) 本', text)[0])
        
            if num_journals <21:
                each_page(driver, str(1), final_data)
                continue
        
            page_num=get_page_num(driver)
        
            each_page(driver, str(i), final_data)
            for page in range(1, page_num):
                scroll(driver)
                switch_page(page+1, driver)
                driver.implicitly_wait(30)
                scroll(driver)
                each_page(driver, str(i), final_data)
                time.sleep(3)
        except Exception:
            error_class_list.append(i)
            print 'the ', str(i), 'is error !----------------'
                        
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()   
    
    f=open('all_data.txt', 'w')
    for d in final_data:
        f.write(d+'\n')
    f.close()
    path='all_data.pkl'
    save_pkl(path, final_data)
    
    path='error_small_class_list.pkl'
    save_pkl(path, error_class_list)
    
if __name__=='__main__':
    get_first_level_page_data()
    handle_all_first_form()
    get_second_form_records()
    save_excel0()
    
    
    
   

