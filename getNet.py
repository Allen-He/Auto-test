# coding=utf-8
import time  
import subprocess
import xlwt


def getUid(package_name):  # 获取UID
    p1 = subprocess.Popen('adb shell "dumpsys package" ' + package_name + ' "| grep userId"',
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 用adb获取信息
    uidLongString = p1.stdout.read()
    uidLongList = uidLongString.split()
    uidMap = uidLongList[0]
    uid = str(uidMap.split("=")[1])
    print(uid)
    return uid


def Rev(package_name):  # 获取某个APP的TCP下载流量
    p1 = subprocess.Popen('adb shell cd proc && cd uid_stat && cd ' + getUid(package_name) + ' && cat tcp_rcv',
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 用adb获取信息uid
    flo_rec = int(p1.stdout.read())
    return flo_rec


def getSnd(package_name):  # 获取某个APP的TCP上传流量
    p1 = subprocess.Popen('adb shell cd proc && cd uid_stat && cd ' + getUid(package_name) + ' && cat tcp_snd',
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 用adb获取信息
    flo_snd = int(p1.stdout.read())
    return flo_snd


time_start = 0
time_end = 0
col = 0
row = 0

book_sdk = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建新的工作簿sdk


sheet_load_sdk = book_sdk.add_sheet(
    'LOAD', cell_overwrite_ok=True)  # 创建新的sheet，并命名为LOAD
sheet_upload_sdk = book_sdk.add_sheet('UPLOAD', cell_overwrite_ok=True)


sheet_load_sdk.write(row, col, "time")
sheet_load_sdk.write(row, col + 1, "load")


sheet_upload_sdk.write(row, col, "time")
sheet_upload_sdk.write(row, col + 1, "upload")


package_name_sdk = "com.tencent.mm"

try:
    uid_sdk = getUid(package_name_sdk)
    print(time.strftime('%Y-%m-%d   %H:%M:%S',
                        time.localtime(time.time())) + '  uid =  ' + str(uid_sdk))
except:
    print('获取sdk-uid失败')


row = 1
col = 0

while time_end <= 60:

    load_sdk = getRev(package_name_sdk)
    upload_sdk = getSnd(package_name_sdk)


    timeNow = time.strftime('%Y-%m-%d   %H:%M:%S',
                            time.localtime(time.time()))  # 获取当前时间

    sheet_load_sdk.write(row, col, timeNow)  # 写入时间
    sheet_load_sdk.write(row, col + 1, load_sdk)  # 写入下载流量
    sheet_upload_sdk.write(row, col, timeNow)  # 写入时间
    sheet_upload_sdk.write(row, col + 1, upload_sdk)  # 写入下载流量

    print str(timeNow) + '  load=' + str(load_sdk) + '   upload=' + str(upload_sdk)

    row = row + 1

time.sleep(10)
time_end += 10
book_sdk.save(r"d:\sdkFolw.xls")
