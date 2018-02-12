# coding=utf-8

import time  # use to control time
import subprocess
import xlwt
import sys

# packageName = input("plese input you packageName:\n")
# packageName = 'com.transsion.shopnc'
packageName = 'com.duowan.gamevoice'


def getPSS(package_name):
    p1 = subprocess.Popen('adb shell "dumpsys meminfo" ' + package_name +
                          '" | grep TOTAL"', stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 用adb获取total内存值
    text = p1.stdout.read()
    print(type(text))
    listoftext = text.split()
    # print(listoftext)
    # import pdb
    # pdb.set_trace()
    # print('PSS=' + str(listoftext[1]))
    a = listoftext[1]
    return a.decode()


def getCPU(package_name):

    cpuVal = subprocess.Popen('adb shell "dumpsys cpuinfo | grep " ' + package_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 获取cpu占用值
    text = cpuVal.stdout.read()
    
    listtext = text.split()
    print(listtext[0].decode())
    # import pdb
    # pdb.set_trace()
    # print("CPU=" + str(listtext[2]))
    return listtext[0].decode()


time_start = 0
time_end = 0

book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建新的工作簿
sheet_sdk = book.add_sheet('PSS-SDK', cell_overwrite_ok=True)  # 创建新的sheet
sheet_sdk.write(0, 0, "time")
sheet_sdk.write(0, 1, "PSS")
sheet_sdk.write(0, 2, "CPU")


row = 1
col = 0

while time_end <= 20:
    timeNow = time.strftime('%Y-%m-%d   %H:%M:%S',
                            time.localtime(time.time()))  # 获取当前时间
    print(timeNow)
    sheet_sdk.write(row, col, timeNow)
    # pss_sdk = getPSS(packageName)
    # sheet_sdk.write(row, col + 1, pss_sdk)
    try:
        pss_sdk = getPSS(packageName)
        cpu_sdk = getCPU(packageName)
        sheet_sdk.write(row, col + 1, pss_sdk)
        print("ok")
        sheet_sdk.write(row, col + 2, cpu_sdk)
        print("ok")
    except:
        print(time.strftime('%Y-%m-%d   %H:%M:%S',
                            time.localtime(time.time())) + "  process has been shoutdown!")
        sys.exit()
    time_end = time_end + 1
    row += 1
    time.sleep(3)
book.save(r"d:\pss.xls")
