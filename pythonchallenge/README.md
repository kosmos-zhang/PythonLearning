# Python challenge解谜详细过程。
===================================

项目基本介绍
-----------------------------------
		项目主页在 [http://www.pythonchallenge.com/](http://www.pythonchallenge.com/)<br /> ，用于通过解谜的过程帮助学习巩固Python知识。
		Python Challenge is a game in which each level can be solved by a bit of (Python) programming. 
		The Python Challenge was written by Nadav Samet. 
		All levels can be solved by straightforward and very short1 scripts. 
		Python Challenge welcomes programmers of all languages. You will be able to solve most riddles in any programming language, but some of them will require Python. 
		Sometimes you'll need extra modules. All can be downloaded for free from the internet. 
		It is just for fun - nothing waits for you at the end. 
		Keep the scripts you write - they might become useful. 

谜题及相关解谜过程
-----------------------------------
- 0. http://www.pythonchallenge.com/pc/def/0.html
>>> print 2**38
274877906944

- 1. http://www.pythonchallenge.com/pc/def/274877906944.html
http://www.pythonchallenge.com/pc/def/map.html
>>> import string
>>> intab='abcdefghijklmnopqrstuvwxyz'   #string.lowercase
>>> outtab='cdefghijklmnopqrstuvwxyzab'  #string.lowercase[2:]+string.lowercase[:2]
>>> transtab=maketrans(intab, outtab)
>>> str="g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
>>> print str.translate(transtab)
i hope you didnt translate it by hand. thats what computers are for. doing it in by hand is inefficient and that's why this text is so long. using string.maketrans() is recommended. now apply on the url.
>>> str='map'
>>> print str.translate(transtab)
ocr

- 2. http://www.pythonchallenge.com/pc/def/ocr.html
>>> import string
>>> txt=open('ocr.txt').read()                        
>>> filter(lambda x:x in string.letters, txt)         
'equality'

>>> s = ''.join([line.rstrip() for line in open('ocr.txt')])    
>>> OCCURRENCES = {}
>>> for c in s: OCCURRENCES[c] = OCCURRENCES.get(c, 0) + 1
...
>>> avgOC = len(s) // len(OCCURRENCES)
>>> print ''.join([c for c in s if OCCURRENCES[c] < avgOC])
equality

- 3. http://www.pythonchallenge.com/pc/def/equality.html
xXXXcXXXx
>>> import string
>>> f=open('equality.txt')
>>> chs=[]
>>> while True:
...     line = f.readline()
...     if line:
...         for i in range(3, len(line)-3):
...             if line[i] in string.lowercase and line[i-1] in string.uppercase and line[i-2] in string.uppercase and line[i-3] in string.uppercase and line[i+1] in string.uppercase and line[i+2] in string.uppercase and line[i+3] in string.uppercase:
...                 if i-4<0 or line[i-4] in string.uppercase:
...                     continue
...                 if i+4>=len(line) or line[i+4] in string.uppercase:
...                     continue
...                 chs.append(line[i])
...     else:
...         break
...
>>> print ''.join(chs)
linkedlist

>>> import re
>>> txt = open('equality.txt').read()
>>> print ''.join(x[1] for x in re.findall('(^|[^A-Z])[A-Z]{3}([a-z])[A-Z]{3}([^A-Z]|$)', txt))
linkedlist

- 4. http://www.pythonchallenge.com/pc/def/linkedlist.php
#由于网络不是很正常，所以使用函数，这样出现问题之后可以从断点继续
>>> import urllib
>>> def getnoth(ind=0, nothing='12345'):
...     url='http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='
...     while ind<400:
...             f=urllib.urlopen(url+nothing)
...             line=f.readline()
...             nothing=line.split(' ')[-1]
...             ind += 1
...             print ind,':',nothing
...                                                                   
>>> getnoth()

- 5. http://www.pythonchallenge.com/pc/def/peak.html
>>> import cPickle as pickle
>>> str=load('banner.p').load()
>>> t=pickle.loads(str)
>>> for a in t:
...     print ''.join([c*count for c, count in a])
...


              #####                                                                      #####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
      ###      ####   ###         ###       #####   ###    #####   ###          ###       ####
   ###   ##    #### #######     ##  ###      #### #######   #### #######     ###  ###     ####
  ###     ###  #####    ####   ###   ####    #####    ####  #####    ####   ###     ###   ####
 ###           ####     ####   ###    ###    ####     ####  ####     ####  ###      ####  ####
 ###           ####     ####          ###    ####     ####  ####     ####  ###       ###  ####
####           ####     ####     ##   ###    ####     ####  ####     #### ####       ###  ####
####           ####     ####   ##########    ####     ####  ####     #### ##############  ####
####           ####     ####  ###    ####    ####     ####  ####     #### ####            ####
####           ####     #### ####     ###    ####     ####  ####     #### ####            ####
 ###           ####     #### ####     ###    ####     ####  ####     ####  ###            ####
  ###      ##  ####     ####  ###    ####    ####     ####  ####     ####   ###      ##   ####
   ###    ##   ####     ####   ###########   ####     ####  ####     ####    ###    ##    ####
      ###     ######    #####    ##    #### ######    ###########    #####      ###      ######

- 6. http://www.pythonchallenge.com/pc/def/channel.html
download file http://www.pythonchallenge.com/pc/def/channel.zip, ang read readme.txt
>>> import zipfile
>>> z=zipfile.ZipFile('channel.zip')
>>> def getcont(filename='90052'):
...     while True:
...         t=z.read(filename+'.txt')
...         print t
...         filename=t.split(' ')[-1]

>>> def getcomt(num='90052'):                                    
...     filename = num+'.txt'                                    
...     comments=[]                                                     
...     while filename in z.namelist():                          
...         comments.append(z.getinfo(filename).comment)
...         filename=z.read(filename).split(' ')[-1]+'.txt'
...     print ''.join(comments)
... 
>>> getcomt()                                                    
**************************************************************** 
**************************************************************** 
**                                                            ** 
**   OO    OO    XX      YYYY    GG    GG  EEEEEE NN      NN  ** 
**   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE  NN    NN   ** 
**   OO    OO XXX  XXX YYY   YY  GG GG     EE       NN  NN    ** 
**   OOOOOOOO XX    XX YY        GGG       EEEEE     NNNN     ** 
**   OOOOOOOO XX    XX YY        GGG       EEEEE      NN      ** 
**   OO    OO XXX  XXX YYY   YY  GG GG     EE         NN      ** 
**   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE     NN      ** 
**   OO    OO    XX      YYYY    GG    GG  EEEEEE     NN      ** 
**                                                            ** 
**************************************************************** 
 **************************************************************  

- 7. http://www.pythonchallenge.com/pc/def/oxygen.html
>>> import Image
>>> im=Image.open('oxygen.png')
>>> print im.size
(629, 95)
>>> row = [im.getpixel((x, 45)) for x in range(0, im.size[0], 7)]
>>> ords = [r for r, g, b, a in row if r == g == b]
>>> print "".join(map(chr, ords))
smart guy, you made it. the next level is [105, 110, 116, 101, 103, 114, 105, 116, 121]
>>> "".join(map(chr,[105, 110, 116, 101, 103, 114, 105, 116, 121]))
'integrity'

- 8. http://www.pythonchallenge.com/pc/def/integrity.html
>>> import bz2                                                                                           
>>> bz2.decompress('BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084')
'huge'
>>> bz2.decompress('BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08')
'file'

- 9. http://huge:file@www.pythonchallenge.com/pc/return/good.html
>>> import Image, os, ImageDraw
>>> def crtimg(f="out.png",ps=()):
...     if os.path.isfile(f):
...         im=Image.open(f)
...     else:
...         im=Image.new("RGB", (600, 600), (255,255,255))
...     a=ImageDraw.Draw(im)
...     for i in range(0, len(ps)//2-1):
...         a.line(((ps[i*2], ps[i*2+1]), (ps[i*2+2], ps[i*2+3])),fill=(0,0,0))
...     im.save(f)
...

- 10. http://huge:file@www.pythonchallenge.com/pc/return/bull.html
a = [1, 11, 21, 1211, 111221, ...
a = [1, 11, 21, 1211, 111221, 312211,13112221,1113213211,...
    '1'*1, '1'*2, '2'*1+'1'*1,'1'*1+'2'*1+'1'*2,...   字符编码功能实现
>>> def describ(s):
...     cs=[]
...     c=''
...     cc=0
...     for i in range(0, len(s)):
...         if c==s[i]: cc+=1
...         else:
...             if cc>0:
...                 cs.append(str(cc)+c)
...             cc = 1
...             c=s[i]
...     if cc>0:
...         cs.append(str(cc)+c)
...     return "".join(cs)
...
>>> s='1'
>>> for i in range(0, 30):
...     s=describ(s)
...
>>> print len(s)
5808
>>> import re
>>> def describe(s):
...     return "".join([str(len(m.group(0))) + m.group(1) for m in re.finditer(r"(\d)\1*", s)])
...

- 11. http://huge:file@www.pythonchallenge.com/pc/return/5808.html
>>> import Image
>>> im=Image.open('cave.jpg')
>>> print im.size
(640, 480)
>>> im1=Image.new(im.mode, (320, 240))
>>> im2=Image.new(im.mode, (320, 240))
>>> for x in range(640):
...     for y in range(480):
...             if x%2==0 and y%2==0:
...                     im1.putpixel((x//2,y//2), im.getpixel((x,y)))
...             else:
...                     im2.putpixel((x//2,y//2), im.getpixel((x,y)))
...
>>> im1.show()
>>> im2.show()

- 12. http://huge:file@www.pythonchallenge.com/pc/return/evil.html
>>> s=open('evil2.gfx', 'rb').read()
>>> for i in range(5):
...     open("evil"+str(i)+".jpg",'wb').write(s[i::5])
...

- 13. http://huge:file@www.pythonchallenge.com/pc/return/disproportional.html
>>> import xmlrpclib
>>> url = 'http://www.pythonchallenge.com/pc/phonebook.php'
>>> phonebook = xmlrpclib.Server(url)
>>> print phonebook.system.listMethods()
['phone', 'system.listMethods', 'system.methodHelp', 'system.methodSignature', 'system.multicall', 'system.getCapabilities']
>>> print phonebook.system.methodHelp('phone')
Returns the phone of a person
>>> print phonebook.system.methodSignature('phone')
[['string', 'string']]
>>> phonebook.phone('Bert')
'555-ITALY'

- 14. http://huge:file@www.pythonchallenge.com/pc/return/italy.html
<!-- remember: 100*100 = (100+99+99+98) + (...  -->
>>> import Image
>>> im=Image.open('wire.png')
>>> print im.size
(10000,1)
>>> im1=Image.new(im.mode, (100, 100))
>>> t, l, b, r = 0, 0, 99, 99
>>> x,y=0,0
>>> ix,iy=1,0
>>> for i in xrange(10000):
...     im1.putpixel((x,y), im.getpixel((i,0)))
...     if ix==1 and x==r: ix,iy,t=0,1,t+1
...     elif iy==1 and y==b: ix,iy,r=-1,0,r-1
...     elif ix==-1 and x==l: ix,iy,b=0,-1,b-1
...     elif iy==-1 and y==t: ix,iy,l=1,0,l+1
...     x,y=x+ix,y+iy
...
>>> im1.save('wire1.png')

http://www.pythonchallenge.com/pc/return/cat.html
and its name is uzi. you'll hear from him later. 

- 15. http://huge:file@www.pythonchallenge.com/pc/return/uzi.html
>>> for i in range(1006, 2000, 10):
...     if datetime.datetime(i, 1, 26).weekday()==0 and i%4==0:
...             print i
...
1176
1356
1576
1756
1976
>>>
1756年1月27日(乙亥年腊月廿六)，奥地利音乐大师莫扎特诞生。

- 16. http://huge:file@www.pythonchallenge.com/pc/return/mozart.html
>>> import Image
>>> im=Image.open('mozart.gif')
>>> im1=im.copy()
>>> w,h=im.size
>>> for y in range(h):
...     line=[im.getpixel((x, y)) for x in range(w)]
...     pink=line.index(195)
...     line=line[pink:]+line[:pink]
...     for i in range(w): im1.putpixel((i, y), line[i])
...
>>> im1.save('out.gif')

- 17. http://huge:file@www.pythonchallenge.com/pc/return/romance.html
