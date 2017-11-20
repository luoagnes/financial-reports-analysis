# -*- coding: utf-8 -*-

import xlwt
import xlrd
import pickle
import sys     
reload(sys) 
sys.setdefaultencoding('utf-8')

def save_txt(path, data):
    f=open(path, 'w')
    for d in data:
        f.write(d+'\n')
    f.close()

def load_pkl(path):
    pkl_file = open(path, 'rb')
    data1 = pickle.load(pkl_file)
    pkl_file.close()
    return data1


def get_all_class_name():
    class_name_list=[]
    num=0
    class_num=[]
    
    path='title_content.txt'
    f=open(path, 'rb')
    lines=f.readlines()
    for line in lines:
        temp=line.split()
        class_name=' '.join([e.decode('utf-8') for e in temp[1:-3]])
        class_name_list.append(class_name)
        num +=int(temp[-2])
        class_num.append(class_name+': '+temp[-2])
    return class_name_list, class_num, num

def handle_all_journals():
    final_data={}
    
    path='all_small_data.txt'
    f=open(path, 'rb')
    lines=f.readlines()
    print len(lines), '------------lines------------'
    
    for i in range(177):
        final_data[str(i)]={}
        
    for line in lines:
        
        temp=line.strip().split()
        if len(temp)<5:
            print 'length less 5, continu+===================='
            continue
        
        
        index=temp[0]
        if_2016=temp[-2]
        distribute=temp[-3]
        
        if temp[-4]=='Y':
            Review='Y'
            journal='_'.join(temp[1:-4])
            journal_name=' '.join(temp[1:-4])
        else:
            Review='--'
            journal='_'.join(temp[1:-3])
            journal_name=' '.join(temp[1:-3])
        
        
        atemp=temp[-1].strip().split('___')
        class_no=atemp[1]
        avgif=atemp[0]
        
        
        temp=[index, journal_name, Review, distribute, if_2016, avgif]
        #print class_no
        
        #print journal
        final_data[class_no][journal]=temp
        
    return final_data

def save_pkl(path, data):
    output = open(path, 'wb')

    # Pickle dictionary using protocol 0.
    pickle.dump(data, output)
    output.close()
    
def save_excel(final_data, class_name_list):
    data=[]
    
    path='all_fournal_issn.pkl'
    before_journal_issn=load_pkl(path)
    
    path='added_fournal_issn.pkl'
    add_journal_issn=load_pkl(path)
    all_fournal_issn=dict(before_journal_issn, **add_journal_issn)
    
    index=0
    for class_no in final_data.keys():
        for journal in final_data[class_no].keys():
            print index, '------------------'
            temp=final_data[class_no][journal]
            temp.append(class_name_list[int(class_no)])
            
            try:
                if journal in all_fournal_issn.keys():
                    temp.append(all_fournal_issn[journal][0])
                else:
                    temp.append('---')
            except Exception:
                temp.append('---')
                
            data.append(temp)
            index +=1
    print len(data), '^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        
    wbk=xlwt.Workbook()
    table=wbk.add_sheet('sheet1')
    
    ### write col title
    row=0
    col=0
    table.write(row, col, u'序号')
    table.write(row, col+1, u'期刊名')
    table.write(row, col+2, u'Review')
    table.write(row, col+3, u'分区')
    table.write(row, col+4, u'2016年IF')
    table.write(row, col+5, u'3年平均IF')
    table.write(row, col+6, u'小类')
    table.write(row, col+7, u'ISSN')
    
    row=0
    col=0
    for d in data:
        row+=1
        col=0
        for e in d:
            if d.index(e)==6 :
                table.write(row, col, e.decode('utf-8'))
            else:
                table.write(row, col, e)
            
            col+=1
    
    path='small_class_library_journal_records_list.xls'
    wbk.save(path)
        

def read_excel(path):
    data={}
    wbk=xlrd.open_workbook(path)
    sheet=wbk.sheets()[0]
    
    nrows=sheet.nrows
    for row in range(1, nrows):
        content=sheet.row_values(row)
        data[content[1].strip()]=content
    return data

def save_excel2(final_data):
    wbk=xlwt.Workbook()
    table=wbk.add_sheet('sheet1')
    
    ### write col title
    row=0
    col=0
    table.write(row, col, u'序号')
    table.write(row, col+1, u'期刊名')
    table.write(row, col+2, u'Review')
    table.write(row, col+3, u'分区')
    table.write(row, col+4, u'2016年IF')
    table.write(row, col+5, u'3年平均IF')
    table.write(row, col+6, u'小类')
    table.write(row, col+7, u'ISSN')
    
    row=0
    col=0
    for key in final_data.keys():
        row+=1
        col=0
        for e in final_data[key]:
            if final_data[key].index(e)==6 :
                table.write(row, col, e.decode('utf-8'))
            else:
                table.write(row, col, e)
            
            col+=1
    
    path='empty_data.xls'
    wbk.save(path)
    
def save_excel0():
    data=[]
    path='first_level_reocrds.pkl'
    first_level_records=load_pkl(path)
    
    path='all_fournal_issn.pkl'
    before_journal_issn=load_pkl(path)
    
    path='added_fournal_issn.pkl'
    add_journal_issn=load_pkl(path)
    
    for key in first_level_records.keys():
        journal_name=' '.join(key.strip().split('_'))
        temp1=[journal_name]
        temp1.extend(first_level_records[key][2:])
        
        all_fournal_issn=dict(before_journal_issn, **add_journal_issn)
        temp1.extend(all_fournal_issn[key])
        data.append(temp1)
        
    wbk=xlwt.Workbook()
    table=wbk.add_sheet('sheet1')
    
    ### write col title
    row=0
    col=0
    table.write(row, col, u'序号')
    table.write(row, col+1, u'期刊名')
    table.write(row, col+2, u'Review')
    table.write(row, col+3, u'分区')
    table.write(row, col+4, u'2016年IF')
    table.write(row, col+5, u'3年平均IF')
    table.write(row, col+6, u'大类')
    table.write(row, col+7, u'ISSN')
    table.write(row, col+8, u'小类')
    
    row=0
    col=0
    for d in data:
        row+=1
        col=0
        for e in d:
            #print type(e), '------', e
            table.write(row, col, e.decode('utf-8'))
            col+=1
    
    path='big_library_journal_records_list.xls'
    wbk.save(path)

def final_func():
    path='empty_isssn.xls'
    empty_isssn=read_excel(path)
    
    path='big_calss_library_journal_records_list.xls'
    big_calss_library=read_excel(path)
    
    for e in empty_isssn.keys():
        if e in big_calss_library.keys():
            empty_isssn[e][7]=big_calss_library[e][6]
            
    save_excel2(empty_isssn)
        
    
    
if __name__=='__main__':
    '''
    class_name_list, class_num, num=get_all_class_name()
    
    path='class_name_list.pkl'
    save_pkl(path, class_name_list)
    
    path='class_num.pkl'
    save_pkl(path, class_num)
    
    print num, '---$----------------$'
    
    final_data=handle_all_journals()
    print '------'
    
    path='final_data.pkl'
    save_pkl(path, final_data)
    '''
    '''
    path='final_data.pkl'
    final_data=load_pkl(path)
    
    
    path='class_name_list.pkl'
    class_name_list=load_pkl(path)
    save_excel(final_data, class_name_list)
    '''
    
    final_func()
    
    
    
    
        
    
    
    
    

