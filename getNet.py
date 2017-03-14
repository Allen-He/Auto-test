#coding=utf-8
import time#use to control time
import subprocess
import xlwt

def getUid(package_name):#获取UID
	p1 = subprocess.Popen('adb shell "dumpsys package" '+package_name+' "| grep userId"',
							stdout=subprocess.PIPE,stderr=subprocess.PIPE)#用adb获取信息
	uidLongString = p1.stdout.read()
	uidLongList = uidLongString.split()
	uidMap = uidLongList[0]
	uid =str(uidMap.split("=")[1])
	print (uid)
	return uid

def getRev(package_name):#获取某个APP的TCP下载流量
	p1 = subprocess.Popen('adb shell cd proc && cd uid_stat && cd '+ getUid(package_name) +' && cat tcp_rcv',
	stdout=subprocess.PIPE,stderr=subprocess.PIPE)#用adb获取信息uid
	flo_rec =int(p1.stdout.read())
	return flo_rec

def getSnd(package_name):#获取某个APP的TCP上传流量
	p1 = subprocess.Popen('adb shell cd proc && cd uid_stat && cd '+ getUid(package_name) +' && cat tcp_snd',
	stdout=subprocess.PIPE,stderr=subprocess.PIPE)#用adb获取信息
	flo_snd =int(p1.stdout.read())
	return flo_snd

time_start =0
time_end =0
col =0
row =0

book_sdk = xlwt.Workbook(encoding='utf-8',style_compression=0)#创建新的工作簿sdk
# book_wx = xlwt.Workbook(encoding='utf-8',style_compression=0)#创建新的工作簿wx

sheet_load_sdk = book_sdk.add_sheet('LOAD',cell_overwrite_ok=True)#创建新的sheet，并命名为LOAD
sheet_upload_sdk = book_sdk.add_sheet('UPLOAD',cell_overwrite_ok=True)

# sheet_load_wx = book_wx.add_sheet('LOAD',cell_overwrite_ok=True)#创建新的sheet，并命名为LOAD
# sheet_upload_wx = book_wx.add_sheet('UPLOAD',cell_overwrite_ok=True)

sheet_load_sdk.write(row,col,"time")
sheet_load_sdk.write(row,col +1,"load")

# sheet_load_wx.write(row,col,"time")
# sheet_load_wx.write(row,col +1,"load")

sheet_upload_sdk.write(row,col,"time")
sheet_upload_sdk.write(row,col +1,"upload")

# sheet_upload_wx.write(row,col,"time")
# sheet_upload_wx.write(row,col +1,"upload")

package_name_sdk ="com.tencent.mm"
# package_name_wx ="com.tencent.mm"
try:
	uid_sdk = getUid(package_name_sdk)
	print (time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime(time.time())) +'  uid =  '+str(uid_sdk))
except:
	print('获取sdk-uid失败')

# try:
# 	uid_wx = getUid(package_name_wx)
# 	print time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime(time.time())) +'  uid =  '+str(uid_wx)
# except:
# 	print'获取wx-uid失败'
row =1
col =0

while time_end <=60:

	load_sdk = getRev(package_name_sdk)
	upload_sdk = getSnd(package_name_sdk)

	# load_wx = getRev(package_name_wx)
	# upload_wx = getSnd(package_name_wx)

	timeNow = time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime(time.time()))#获取当前时间

	sheet_load_sdk.write(row,col,timeNow)#写入时间
	sheet_load_sdk.write(row,col +1,load_sdk)#写入下载流量
	sheet_upload_sdk.write(row,col,timeNow)#写入时间
	sheet_upload_sdk.write(row,col +1,upload_sdk)#写入下载流量

	# sheet_load_wx.write(row,col,timeNow)#写入时间
	# sheet_load_wx.write(row,col +1,load_wx)#写入下载流量
	# sheet_upload_wx.write(row,col,timeNow)#写入时间
	# sheet_upload_wx.write(row,col +1,upload_wx)#写入下载流量

	printstr(timeNow) +'  load='+str(load_sdk) +'    upload='+str(upload_sdk)
	# printstr(timeNow) +'  load='+str(load_wx) +'    upload='+str(upload_wx)
	row = row +1

time.sleep(10)
time_end +=10
book_sdk.save(r"d:\sdkFolw.xls")
book_wx.save(r"d:\wxFlow.xls")

