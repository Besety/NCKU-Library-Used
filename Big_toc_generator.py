
import webbrowser
print("－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－\n"
	+"     *  B i g T O C     H T M L    T e x t    G e n e r a t o r   *\n"
	+"                                                 	  2018 March byBTW\n"
	+"－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－\n")



#--USER INPUT--
title = input("請輸入期刊名稱:")
name = input("請輸入期刊檔名縮寫:")
year_start = eval(input("請輸入起始年份:"))
vol_start = eval(input("請輸入起始卷數:"))
vol_end = eval(input("請輸入結束卷數:"))
num = eval(input("請輸入每卷有幾期:"))
sw = eval(input("請選擇每期出刊時間表達方式(0:無/1:季節/2:月份/3:手動輸入):"))
#print(vol_start,vol_num,number,year_start,name)

#--COMPUTE VOL_NUMBER & YEAR_END--
vol_number =( vol_end - vol_start ) + 1
year_end =( year_start + vol_number )- 1
#print(year_end,"\n",vol_number,"\n")


#--SET SEASON & MONTH & USER LIST--
season = list(["Spring","Summer","Fall","Winter"])
month = list(["January","February","March","April","May","June","July","August","September","October","November","December"])
userlist = list()
#print(season,month)

# WRITE HTML
hName = name + "_toc_list_of_volumes.html"
f = open(hName,'wt',encoding ='utf8')

message1 = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Project MUSE -- %s</title>

<style type="text/css">
  a:link {
    color:blue;
    text-decoration:none;
  }

  ul {
  	font-size: 18px;
  	font-family:sans-serif,"fantasy","cursive";
  }

  li {
  	margin: 5px;
  	line-height: 30px;
  }

  table {
  	margin-top: 30px;
		border:#ff3030 1px solid;
  }

  h2 {
  	text-align: center;
  }
</style>

<script language="javascript">
<!-- Begin
function hidestatus()
{
	window.status='Project MUSE -- %s'
	return true
}

if (document.layers)
document.captureEvents(Event.MOUSEOVER | Event.MOUSEOUT)
document.onmouseover=hidestatus
document.onmouseout=hidestatus


</script>
</head>

<table width="700px" border="0" align="center" cellpadding="0" cellspacing="0">
	<tr>
		<td><h2>%s</h2></td>
	</tr>
	<tr>
		<td>
"""%(title,title,title)

f.write(message1)


index = 0;
#--CHOOSE SEASON TO REPRESENT--
if sw == 1:
#--USER INPUT SEASON CODE--
	while index < num :
#		userlist.insert(index,input("Enter the Season following:"))
		userlist.append(eval(input("請依序輸入季節代碼(1:春 2:夏 3:秋 4:冬) :")))
		index = index + 1
	pass
#	print(userlist)

#--OUTPUT HTML TEXT--
	while vol_start <= vol_end :
		print("<ul>\n<b>Volume "+str(vol_end)+ ", "+ str(year_end) + "</b>",file=f)
		j = num
		while j>0 :
			print(
				"	<li><a href=\"" +str(name)+str(vol_end)+ "."+str(j)+ ".htm\" target=\"\" >Volume "+str(vol_end)+", Number "+str(j)+",",season[userlist[j-1]-1],year_end,"</a></li>"
				,file=f)
			j = j-1 
		pass
		vol_end = vol_end -1
		year_end = year_end -1
		print("</ul>",file=f)
	pass

#--CHOOSE MONTH TO REPRESENT--
if sw == 2:
#--USER INPUT MONTH CODE--
	while index < num :
#		userlist.insert(index,input("Enter the Season following:"))
		userlist.append(eval(input("請依序輸入月份代碼(1~12:一至十二月) :")))
		index = index + 1
	pass

#	print(userlist)
#--OUTPUT HTML TEXT--
	while vol_start <= vol_end :
		print("<ul>\n<b>Volume "+str(vol_end)+", "+str(year_end)+"</b>",file=f)
		j = num
		while j>0 :
			print(
				"	<li><a href=\"" +str(name)+str(vol_end)+ "."+str(j)+ ".htm\" target=\"\" >Volume "+str(vol_end)+", Number "+str(j)+",",month[userlist[j-1]-1],year_end,"</a></li>"
				,file=f)
			j = j-1 
		pass
		vol_end = vol_end -1
		year_end = year_end -1
		print("</ul>",file=f)
	pass

#--CHOOSE USER INPUT--
if sw == 3:
	while index < num :
		userlist.insert(index,input("請依序輸入:"))
		index = index + 1
	pass
#	print(userlist)
#--OUTPUT HTML TEXT--
	while vol_start <= vol_end :
		print("<ul>\n<b>Volume "+str(vol_end)+", "+str(year_end)+"</b>",file=f)
		j = num
		while j>0 :
			print(
				"	<li><a href=\"" +str(name)+str(vol_end)+ "."+str(j)+ ".htm\" target=\"\" >Volume "+str(vol_end)+", Number "+str(j)+",",userlist[j-1],year_end,"</a></li>"
				,file=f)
			j = j-1
		pass
		vol_end = vol_end -1
		year_end = year_end -1
		print("</ul>",file=f)
	pass

#--CHOOSE NO REPRESENT--
else :
#--OUTPUT HTML TEXT--
	while vol_start <= vol_end :
		print("<ul>\n<b>Volume "+str(vol_end)+", "+str(year_end)+"</b>",file=f)
		j = num
		while j>0 :
			print(
				"	<li><a href=\"" +str(name)+str(vol_end)+ "."+str(j)+ ".htm\" target=\"\" >Volume "+str(vol_end)+", Number "+str(j)+",",year_end,"</a></li>"
				,file=f)
			j = j-1
		pass
		vol_end = vol_end -1
		year_end = year_end -1
		print("</ul>",file=f)
	pass
pass

f.close()
print("輸出!")

os.system("pause")