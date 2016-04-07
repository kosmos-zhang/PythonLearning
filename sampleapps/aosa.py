#coding:utf-8
from bs4 import BeautifulSoup
import os,sys

reload(sys)
sys.setdefaultencoding('utf-8')

def replaceHref(html_doc):    
    soup = BeautifulSoup(html_doc, "html5lib")
    alists = soup.find_all('a')
    for a in alists:
        try:
            if a['href'].find("javascript:if(confirm('")>=0:
                temphref = a['href'][(a['href'].find("window.location='")+len("window.location='")):-1]
                a['href']=temphref
        except Exception,e:
            pass

    return soup.prettify()

def updateDirs(directory):
    listfile=os.listdir(directory)
    for filename in listfile:
        fulldirfile=os.path.join(directory,filename)
        if os.path.isdir(fulldirfile):
            updateDirs(fulldirfile)
        elif filename[-5:]==".html":
            html_doc = open(fulldirfile).read()
            html_doc = replaceHref(html_doc)
            file = open(fulldirfile, "w+")
            file.write(html_doc)
            file.close()

if __name__=='__main__':    
    updateDirs(*sys.argv)

