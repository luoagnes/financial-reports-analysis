from pdf2txt import pdfTotxt1, pdfTotxt2
import os


def handleStock(stock_dir, dir, root_txt_path):
    for stock in stock_dir:
        years_dir=os.listdir(dir+stock)
        for y in years_dir:
            type_dir=os.listdir(dir+stock+'/'+y)
            for t in type_dir:
                report_dir=os.listdir(dir+stock+'/'+y+'/'+t)
                root_txt=root_txt_path+stock+'_'+y+'_'+t+'_Chairman Statement.txt'
                if os.path.exists(root_txt):
                    continue
                for r in report_dir:
                    try:
                        pdfTotxt1(dir+stock+'/'+y+'/'+t+'/'+r, root_txt)
                    except:
                        pdfTotxt2(dir+stock+'/'+y+'/'+t+'/'+r, root_txt)

if __name__=='__main__':
    
    root_txt_path='/home/luowang/data/financial reports/demo_68_txt/'
    if not os.path.exists(root_txt_path):
        os.mkdir(root_txt_path)
    
    root_pdf_path='/home/luowang/data/financial reports/demo_68_test/'
    if os.path.exists(root_pdf_path):
        stock_dir=os.listdir(root_pdf_path)
        handleStock(stock_dir, root_pdf_path, root_txt_path)
    
        
