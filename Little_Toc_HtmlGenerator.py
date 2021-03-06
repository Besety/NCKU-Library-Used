# encode 'Latin1'
'''

NCKU Library 期刊組
ProjectMUSE 爬蟲
使用BeautifulSoup建立目錄及對應檔名

'''

import requests
import string
import re
import os
import bottle
import difflib
from bs4 import BeautifulSoup
from collections import defaultdict
from tkinter import *
import tkinter as tk

# 送HTML Request查看網頁是否有回應
def HTMLrequest(addr):
	my_headers = {'user-agent': 'my-toc/0.0.1'}
	res = requests.get(addr ,headers = my_headers)
	rescheck = res.status_code
	while rescheck != 200:
		if rescheck == 404:
			print(rescheck ,"Not Found. 請重新輸入")
		else :
			print(rescheck ,"請查詢HTTP狀態碼. 並重新輸入")
		addr = input("請重新輸入網址:")
		res = requests.get(addr ,headers = my_headers)
		rescheck = res.status_code
	pass
	print(rescheck ,"OK")
	return res

# 抓網頁的目錄
def findHrefDict(soup):
	a = soup.findAll('li',{'class':'volume'})
	a = str(a).replace('<li class="volume">\n','').replace('</a></span>','').replace('</li>, <span>','')
	a2 = re.sub('(\".*\")',"",a) # nameofhref
	a2 = str(a2).replace('<a href=>','').replace('<span>','')
	a2 = str(a2).split('\n')
	c = re.findall('(\".*\")',a) #href "/issue/38369"

	i=0
	while i< len(c):
		c[i] = 'https://muse.jhu.edu' + c[i].strip("\"")
		i = i+1
		pass
	dict ={}
	k=0
	while  k < len(c):
		dict[a2[k]]=c[k]
		k=k+1

		pass

	return (dict)

# 抓取卷期名稱
def crawTitle(list):
	for drink in soup.select('{}'.format('.title')):
		# print(drink.get_text())
		list.append(str(drink.get_text()).strip())
	pass
	#print("titles:",list,len(list))

# 抓取作者
def crawAuthor(list):
	for drink in soup.select('{}'.format('.author')):
		# print(drink.get_text())
		if drink.get_text() == "":
			list.append("")
		else:
			list.append(str(drink.get_text()).strip().replace('\n',''))
	pass
	#print("authors",list,len(list))

# 抓取大標題
def BigTitle():
	pat = re.compile("(\-.*?\-)")
	b = soup.find('title').get_text()
	b = re.findall(pat,b)
	return(b[0].replace('- ',"").replace('-',""))

# 抓取副標題, 但後來改版網頁上就沒顯示了
def crawSubTitle(list):
	for drink in soup.select('{}'.format('#toc h3')):
		#print(drink.get_text())
		list.append(str(drink.get_text()))
	pass

# 切割期數與卷數(volume/number)
def split_vol_num(s):
	try:
		#適用patten:Volume 3, Number 4, 1960
		vol , num = s.split(",",1)
		vol= int(re.sub("(\w*\s|,.*$)","",vol))
		num= (re.sub("(\w*\s|,.*$)","",num))
		#print(Vol,Num)
		pass
	# 若有其他的格式,再手動輸入
	except ValueError :
		print(">>無法抓取Volume及Number , 請手動輸入\n")
		vol = input("請輸入Volume :")
		num = input("請輸入Number :")
	return int(vol) ,num

# 判斷檔案是否為PDF
def is_pdf(filename):
	#查看檔案名稱最後(副檔名)是否為.pdf
	return (os.path.splitext(filename)[-1] in ['.pdf'])

# 檢查相同的檔案是否已存在
def is_filExists(fileName,htmName):
	filepath = fileName+'\\toc\\'+htmName
	if os.path.isfile(filepath):
		return 1
	else:
		return 0

# 檢查相同的期數資料夾是否已存在
def is_vNOTExtist(fileName,volname):
	vpath = fileName+'\\'+volname
	if os.path.exists(vpath):
		return 0
		print(vpath)
	else:
		print(vpath)
		return 1

# 找在該卷期內的所有檔名
def findFileName(volname,Vol,Num):
	# 取得所有在該卷期內資料夾(e.g v003內)PDF的檔名
	listFilter =[]
	print(filedir+"\\"+DN)
	listFilter =list(filter(is_pdf, os.listdir(filedir+"\\"+DN)))
	#print (listFilter)

	# 取得該卷期的所有檔名(e.g 3.2Besety.pdf => Besety)
	i=0
	Dname =[]
	while i< len(listFilter):
		if str(Vol)+"."+Num in listFilter[i]:
			# 去頭：因為要找純粹的檔名(通常會等於作者名稱)，在這裡把前面的卷期(e.g 3.2)去除
			a = listFilter[i].strip( str(Vol)+ "."+ Num )
			# 去尾：把.pdf去除
			a = a[:-4]
			Dname.append(a)
		i = i+1
	pass
	#print('已存在檔名(Dname):',Dname,len(Dname))

	return (Dname)

# 找字串內是否包含數字
def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

# 找重複的作者文章的所有檔名(eg. Besety01 Besety02)
def findRepeat(filenamelist):
	repeat_item = defaultdict(list)
	k=0
	while k < len(Dname_m):
		 # 若檔名有數字就加進list
		if hasNumbers(Dname_m[k]):
			repeat_item[re.sub("\d" ,"", Dname_m[k])].append(Dname_m[k])
		k = k +1
	pass
	#print (repeat_item)
	return(repeat_item)

# 比對字串的相似度
# 可以再找其他method套用,SequenceMatcher主要是比對字的組合跟順序相似度
def dif_ratio(a,b):
	seq = difflib.SequenceMatcher(None, a, b)
	ratio = seq.ratio()
	return (ratio)

# 比對抓取的作者名稱和已存在資料夾中的檔名並回傳list
def Compare_and_Map_FileName(Dname,authors):
	fName =[] # 已比對成功的檔名LSIT
	j=0
	# InfoMessge.write("'\n'+ BIGtitle + ", " + titles[0]\n-------------------------------------------------------\n>>比對檔名")
	print("\n"+ BIGtitle + ", " + titles[0]+"\n-------------------------------------------------------\n>>比對檔名")
	while j<len(authors):
		k=0
		# 若作者名稱為空
		if authors[j] == "":
			fN = (re.sub("(\w*\.|\w*\s|,.*$)" ,"", titles[j+1])).lower() #取篇名做re處理
			if fN in Dname: # 處理後的篇名若在已存在檔名內則mapping
				#print('inD: ',fN)
				del Dname[Dname.index(fN)]
			else:
				while k < len(Dname):
					if fN.find(Dname[k]) != -1:
						fN = Dname[k]
						del Dname[k]
						pass
					elif dif_ratio(fN,Dname[k]) > 0.5:
						print(fN,Dname[k])
						print("相似度:",dif_ratio(fN,Dname[k]))
						#InfoMessge.write(fN,Dname[k]+''+"相似度:",dif_ratio(fN,Dname[k]))
						fN = Dname[k]
						del Dname[k]
						pass
					k = k + 1
			fName.append(fN)
		# 若作者名稱不為空
		else :
			# 取作者名比對
			fN = (re.sub("(\w*\.|\w*\s|,.*$)" ,"", authors[j])).lower()
			# 若作者名稱有在已存在檔名內, 則刪掉已比對到的檔名
			if fN in Dname:
				#print('inD: ',fN)
				del Dname[Dname.index(fN)]
			# 沒有直接對應到檔名(有些抓下來是拉丁文，或是有'-'等字符), 則比對相似度
			else:
				while k < len(Dname):
					if dif_ratio(fN,Dname[k]) > 0.67:
						print(fN,Dname[k])
						print("相似度:",dif_ratio(fN,Dname[k]))
						#InfoMessge.write(fN,Dname[k]+''+"相似度:",dif_ratio(fN,Dname[k]))
						fN = Dname[k]
						del Dname[k]
						pass
					k = k + 1
			fName.append(fN)
		j = j+1
	pass
	return(fName)

#  寫入HTML
def WriteHTM(htmName,BIGtitle,authors,titles,DN,Vol,Num,fName):
	f = open( filedir +"/toc/"+hName,'w',encoding ='utf8')

	message1 = """
	<h1>
	%s
	<br />
	<small>%s</small>
	</h1>

	<h2>
	C<small>ONTENTS</small>
	</h2>"""%(BIGtitle,titles[0])

	f.write(message1)

	i = 0
	while i < len(subTitles) :
		message3 = """<H3>%s</H3>
		"""%(subTitles[i])
		i = i+1
		f.write(message3)
	pass

	i = 0
	while i < len(titles)-1 :
		message2 = """
		<!--Article-->
		<UL>%s
		<LI>
		<I>%s</I></LI>"""%(authors[i],titles[i+1])
		f.write(message2)
		if Num =='':
			message3 = """
			<!-- <A HREF="../%s/%d.%s.html">[Access article in HTML]</A> -->"""%(DN,Vol,fName[i])+"""
			<A HREF="../%s/%d.%s.pdf">[Access article in PDF]</A>
			</ul>"""%(DN,Vol,fName[i])
			i = i+1
		else:
			message3 = """
			<!-- <A HREF="../%s/%d.%s.%s.html">[Access article in HTML]</A> -->"""%(DN,Vol,Num,fName[i])+"""
			<A HREF="../%s/%d.%s.%s.pdf">[Access article in PDF]</A>
			</ul>"""%(DN,Vol,Num,fName[i])
			i = i+1
		f.write(message3)
	pass
	f.close()

# 寫入ERROR MSG, 供人工比對
def ErrorMesg(BIGtitle,volnum,fName,Dname,Dname_m,repeat_item):
	if(os.path.isfile(filedir+'/ErrorMessage.txt')):
		f = open(filedir+'/ErrorMessage.txt','a',encoding ='utf8')
		pass
	else:
		f = open(filedir+'/ErrorMessage.txt','w',encoding ='utf8')
		pass
	# WRITE ERROR MESSAGEs
	print('\n\n'+ BIGtitle + ", " + titles[0],file=f)
	print ( "-----------------------/* ERROR  MESSAGE */---------------------------------",file=f)
	print("目前已建立好的檔名\n",fName,len(fName),file=f)
	print("htm中尚未對應到的檔名\n",Dname_m ,len(Dname_m),file=f)
	print("在資料夾內尚未對應到的檔名\n",Dname,len(Dname),file=f)
	if len(Dname_m)==0 and len(Dname)==0:
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>全部MAPPING完成!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",file=f)
	print("重複作者列表\n",dict(repeat_item),file=f)
	print ( "----------------------- ----- ----- ---- ------------------------------------",file=f)
	f.close()

	'''
	# WRITE ERROR MESSAGE
	print('\n'+ BIGtitle + ", " + titles[0])
	print ( "-----------------------/* ERROR  MESSAGE */---------------------------------")
	print("目前已建立好的檔名(fName)\n",fName,len(fName))
	print("htm中尚未對應到的檔名(Dname_m)\n",Dname_m ,len(Dname_m))
	print("在資料夾內尚未對應到的檔名(Dname)\n",Dname,len(Dname))
	if len(Dname_m)==0 and len(Dname)==0:
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>全部MAPPING完成!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	print("重複作者列表\n",dict(repeat_item))
	print ( "----------------------- ----- ----- ---- ------------------------------------")
	'''

# GUI
def onselect(evt):
	selection =nameBox.curselection()
	print(selection)

	chooseBox.delete(0,END)
	for item in selection:
		chooseBox.insert(END,nameBox.get(item))
		pass

def oncreate(evt):
	i=0
	while i<chooseBox.size():
		print(chooseBox.get(i))
		selectHref.append(HrefDict[chooseBox.get(i)])
		i= i+1
	pass
	print(selectHref)




# 輸入該期刊的ProjectMUSE網址
addr = input("請輸入網址:")
soup = BeautifulSoup(HTMLrequest(addr).text, "lxml")
HrefDict = findHrefDict(soup)
selectHref =[]

'''
re.compile('journal_banner_title')
jounalTitle = soup.findAll(id='journal_banner_title').find('h2')
#jounalTitle = re.compile('h2')
print(jounalTitle)
'''

# 建立GUI介面
window = tk.Tk()
window.title('little TOC GENERTATOR')
#window.geometry('500x500')
nameBox = tk.Listbox(window, width = 60,selectmode = MULTIPLE)
nameBox.grid(row=1,column=0)
for keys in HrefDict:
	nameBox.insert('end', keys)
chooseBox = tk.Listbox(window, width = 60)
button=tk.Button(window, text=">>")
creatbutton = tk.Button(window, text="產生小toc")
button.bind('<Double-Button-1>',onselect)
creatbutton.bind('<Double-Button-1>',oncreate)
creatbutton.grid(row=1,columnspan=2)
nameBox.grid(row=0,column=0)
button.grid(row=0,column=1)
chooseBox.grid(row=0,column=2)
window.mainloop()


# 選取期刊資料夾跟輸入縮寫
check = 0
filedir = str(input("請輸入期刊資料夾名稱:"))
tag = str(input("請輸入檔名縮寫:"))
print(selectHref)
while check < len(selectHref):
	# 開爬!
	soup = BeautifulSoup(HTMLrequest(selectHref[check]).text, "lxml")
	# 取出大標題
	BIGtitle = BigTitle()

	#  取出所有標題
	titles =[]
	crawTitle(titles)

	#  字串處理titles[0] 取出期刊數
	# (\w*\s|,.*$)
	Vol , Num = split_vol_num(titles[0])
	hName = tag + str(Vol) + "." + str(Num) + ".htm" # e.g. drj24.5.htm
	if len(str(Num)) >= 4:
		print("htm檔名為:",hName)
		swhName = input("是否重新命名?(1:重新命名 0:檔名正確)")
		if swhName:
			Vol = int(input("請輸入Volume:"))
			Num = (input("請輸入Number:"))
			if Num == '':
				hName = tag + str(Vol) + ".htm" # e.g. drj24.5.htm
			else :
				hName = tag + str(Vol) + "." + str(Num) + ".htm" # e.g. drj24.5.htm
		pass


	#vol資料夾名
	if len(str(Vol)) >2:
		DN = 'v%d'%Vol
	else:
		DN = 'v0%.2d'%Vol




	# 取出所有副標
	subTitles = []
	crawSubTitle(subTitles)

	# 取出所有作者名稱
	authors =[]
	crawAuthor(authors)

	# 有些篇章無作者，填空
	i=0
	while i <((len(titles)-1)-len(authors)):
		authors.append(" ")
		i = i+1
	pass


	# 找出該期的所有PDF檔名
	while is_vNOTExtist(filedir,DN):
		DN = "v"+ str(input("找不到對應資料夾,請手動輸入:"))
		pass
	Dname = findFileName(DN,Vol,Num)
	Dname_m =Dname.copy()

	# 找出重複作者的檔名
	repeat_item = findRepeat(Dname)

	# 比對檔名
	fName = Compare_and_Map_FileName(Dname,authors)

	# 找出剩下沒有被對應到的檔名
	Dname_m = list(set(fName)-(set(fName) & set(Dname_m)))

	# 若都只剩一個則MAP在一起
	if (len(Dname_m) == 1) & (len(Dname) == 1):
		fName[fName.index(Dname_m[0])]=Dname[0]
		del Dname[0]
		del Dname_m[0]

	# 若有檔案已經存在看要不要覆蓋或是重新命名
	if (is_filExists(filedir,hName)):
		print(">>"+hName+"已存在")
		swF=int(input("是否略過?或產生新的檔案/覆蓋?(anyKEY:略過 0:覆蓋 1:產生新檔案並重新命名)"))
		if swF ==0:
			WriteHTM(hName,BIGtitle,authors,titles,DN,Vol,Num,fName)
			ErrorMesg(BIGtitle,titles[0],fName,Dname,Dname_m,repeat_item)
			pass
		elif swF ==1:
			newNum =input("重新命名number:")
			hName = tag + str(Vol) + "." + str(newNum) + ".htm" # e.g. drj24.5A.htm
			WriteHTM(hName,BIGtitle,authors,titles,DN,Vol,Num,fName)
			ErrorMesg(BIGtitle,titles[0],fName,Dname,Dname_m,repeat_item)
		else :
			pass

		pass
		#hName =  tag + str(Vol) + "." + str(Num) + "01.htm" # e.g. drj24.5.htm
		#Write HTM
		#WriteHTM(hName,BIGtitle,authors,titles,Vol,Num,fName)
		#print Error Massage
		#ErrorMesg(BIGtitle,titles[0],fName,Dname,Dname_m,repeat_item)

	else:
		#Write HTM
		WriteHTM(hName,BIGtitle,authors,titles,DN,Vol,Num,fName)
		#print Error Massage
		ErrorMesg(BIGtitle,titles[0],fName,Dname,Dname_m,repeat_item)
		pass

	check = check +1
	pass




os.system('pause')

