# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time
import datetime
import re
import codecs

'''
返回cmd命令的输出值
'''
def getcmdOutput(cmd):
    pipe = os.popen(cmd)

    #读取cmd的值
    text = pipe.read()

    #close方法没有返回值
    sts = pipe.close()
    if sts is None:
        sts = 0

    #判断text最后一个字符换行符，为空的话则取开头到最后一个字符之前
    if text[-1:] == '\n':
        text = text[:-1]

    return sts,text

'''
获取应用的pid
'''
def getPid(device_id,package_name):
    cmd = "adb -s %s shell top -m 10 -n 1" % device_id
    sts,output = getcmdOutput(cmd)
    r = r'(\d+).*\s+%s[^:]' % package_name
    content = re.search(r,output)
    if content:
        pid = content.group(1)
    else:
        print "can't find pid %s" % output
        sys.exit(-1)
    return pid

'''
获取uid
'''
def getUid(device_id,pid):
    cmd = "adb -s %s shell cat /proc/%s/status" % (device_id,pid)
    sts,output = getcmdOutput(cmd)
    content = re.search(r'Uid:\s+(\d+)',output)
    if content:
        uid = content.group(1)
    else:
        print "can't find uid"
        sys.exit(-1)
    return uid

'''
查找cpu内核数量
'''
def getCpuCores(device_id):
    cmd = "adb -s %s shell ls /sys/devices/system/cpu/" % device_id;
    status,output = getcmdOutput(cmd)
    #re.findall会返回符合匹配的字符，以数组的形式返回
    content = re.findall("cpu\\d+",output)  #[cpu0,cpu1,cpu2.....]
    return len(content)

'''
获取GPU信息
'''
def getGpu(device_id):
    #获取GPU使用率，会得到两个值，（前一个/后一个）*100%=使用率
    cmd = "adb -s %s shell cat /sys/class/kgsl/kgsl-3d0/gpubusy" % device_id;
    status, output = getcmdOutput(cmd)
    content = re.search(r'\s*(\d+)\s*(\d+)',output)
    if content:
        gpu1 = content.group(1)
        gpu2 = content.group(2)
    else:
        print "Couldn't get utilization data from: %s!" % output;
        gpu1 = 0
        gpu2 = 0

    if gpu2 != '0':    #获取的gpu2是一个str类型，所有需要和‘0’对比
        utilization = round((float(gpu1)/float(gpu2))*100,2) #取小数点后两位，四舍五入
    else:
        utilization = 0.00

    return utilization


'''
 获取TOP中的数据
PID      PR     CPU%   S      #THR       VSS             RSS          PCY           UID           Name
PID:进程在系统中的ID
CPU% - 当前瞬时所以使用CPU占用率
#THR - 程序当前所用的线程数
UID - 运行当前进程的用户id
Name - 程序名称Android.process.media
VSS - Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）
RSS - Resident Set Size 实际使用物理内存（包含共享库占用的内存）
PSS - Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）
USS - Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）
return cpu,thr,vss,rss
'''
def getTop(device_id,package_name):
    #grep过滤，grep -E过滤多个匹配项，需要使用双引号，grep -E "com.duowan.gamevoice|system/bin/mediaserver"
    cmd = "adb -s %s shell \"top -n 1|grep -E \'%s|%s\'\"" % (device_id, package_name,r'/system/bin/mediaserver');
    status,output = getcmdOutput(cmd)

    #\d匹配数字，+表示一个或多个，\s匹配空白字符，\w匹配数字字母下划线，.匹配出\n换行符外的任何字符,引号里有%s格式化字符串，再匹配一个%的话需要%%，%%为输出%，r''只消除\转义机制，%格式化机制仍有效
    r = r'(\d+)%%\s+\w+\s+(\d+)\s+(\d+)\w+\s+(\d+)\w+.+\s+%s[^\S]' % package_name

    r1 = r'(\d+)%%\s*.*%s' % r'/system/bin/mediaserver'
    topCon = re.search(r, output)
    mediaCon = re.search(r1, output)

    if mediaCon:
        mediaserver = mediaCon.group(1)  #mediaserver占的cpu
    else:
        mediaserver = 0
    if topCon:
        return topCon.group(1),topCon.group(2),topCon.group(3),topCon.group(4),mediaserver  #分别是CPU，线程数，VSS，RSS
    else:
        return 0,0,0,0,mediaserver


'''
获取流量
'''
def getDev(device_id,app_pid):
    cmd = "adb -s %s shell cat /proc/%s/net/dev" % (device_id, app_pid)  #获取的是整个手机网卡的流量
    status, output = getcmdOutput(cmd)
    content = re.search(r'wlan0:\s*(\d+)\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*(\d+)', output)
    if content:
        rec_network = float(content.group(1))
        send_network = float(content.group(2))
    else:
        print "Couldn't get rx and tx data from: %s!" % output
        rec_network = 0.0
        send_network = 0.0

    return rec_network,send_network

'''
获取时间
'''
def getTime():
    t = datetime.datetime.now()
    return t

'''
获取日期
'''
def getDate():
    d = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    return d

'''
获取手机的设备ID
'''
def getDeviceid():
    cmd = "adb devices"
    status,output = getcmdOutput(cmd)
    #若电脑连接了多个手机，会出现多个设备ID，所有使用findall返回一个数组
    content = re.findall('\n(\S+)\s*device',output)

    if content:
        return content
    else:
        print u'%s 手机没插好' % output
        sys.exit(-1)

'''
检查机器是否正常运行
'''
def check_device(device):
    cmd = "adb devices";
    status,output = getcmdOutput(cmd);

    content = re.search("\\n(\\S+)\\s*device[$\n]", output);
    if content is None:
        print u"%s\n%s\n手机没插好，或offline状态，或deviceid：%s输入错误，请检查" %(cmd,output,device)
        sys.exit(-1)
    return device


def getAndroidInfo(interval,log_path,package_name,device_id):
    #传入时间间隔，log路径，包名，设备id，获取CPU，内存，流量等值
    sendNet = 0.0
    recNet = 0.0
    lastSend = 0.0
    lastRec = 0.0
    upflow = 0
    downflow = 0
    t1 = getTime()
    t2 = t1
    firstRun = True

    fileTime = getDate()
    fileName = os.path.join(log_path,"_%s_%s_%s.csv") % (device_id,package_name,fileTime)

    appPid = getPid(device_id,package_name)
    #appUid = getUid(device_id,appPid)
    cpuCores = getCpuCores(device_id)

    # codecs.open()打开文件可避免编码错误 'a' : 向一个文件追加内容,  不能使用 .read*()
    with codecs.open(fileName,'a','utf-8') as f:
        f.write(u'时间，上行流量(KB/S)，下行流量(KB/S)，应用CPU占比(%)，线程数，虚拟内存VSS(MB)，实际内存RSS(MB)，GPU()%，miedaseverCPU(%)\n')

    title = "时间,上行流量(KB/s),下行流量(KB/s),应用cpu占比,线程数,虚拟内存vss(MB),实际内存rss(MB),GPU（%）,mediaserver (cpu%)"
    print title.replace(",","  ").decode("utf-8")

    #循环开始
    while True:
        gpu = getGpu(device_id)
        cpu,thr,vss,rss,mediaserver = getTop(device_id,package_name)
        sendNet,recNet = getDev(device_id,appPid)
        t1 = getTime()

        t = t1-t2
        # d是datetime.timedelta类，所以取秒的对象使用seconds，microseconds是微秒，一秒等于1000000微秒
        seconds =t.seconds + t.microseconds/1000000.0
        t2 = t1
        upflow = ((sendNet-lastSend)/1024)/seconds
        downflow = ((recNet-lastRec)/1024)/seconds
        #round将数值四舍五入，第二个参数表明保留几位小数
        upflow = round(upflow, 2)
        downflow = round(downflow, 2)
        lastRec = recNet
        lastSend = sendNet
        str_now_time = getDate()
        write_str = "%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str_now_time, upflow, downflow, cpu, thr, round(float(vss) / 1024, 2),round(float(rss) / 1024, 2), gpu, mediaserver);
        print write_str.replace(",", "  ")
        with codecs.open(fileName, 'a', 'utf-8') as f:
            f.write(write_str)


        time.sleep(float(interval))


if __name__ == "__main__":
    dict = {"wechat":"com.tencent.mm", "yy":"com.duowan.mobile"}

    '''    变量分别为：包名 时间间隔 结果存放目录 设备ID    '''
    # 包名，若没有输入包名，则使用dict中定义的包名
    if len(sys.argv) > 1:
        package_name = sys.argv[1]
    else:
        package_name = dict['wechat']

    # 时间间隔，若没有则默认为0
    if len(sys.argv) > 2:
        param_interval_time = sys.argv[2]
    else:
        param_interval_time = 0

    # 存放目录，若没有则默认创建performance目录
    if len(sys.argv) > 3:
        param_log_path = sys.argv[3]
    else:
        param_log_path = 'performance'
        if not os.path.exists(param_log_path):
            os.mkdir(param_log_path)

    # 设备id，若没有则默认查找连接了电脑的第一个设备ID
    if len(sys.argv) > 4:
        device_id = check_device(sys.argv[4])
    else:
        device_id = getDeviceid()[0];


    getAndroidInfo(param_interval_time, param_log_path, package_name, device_id)



