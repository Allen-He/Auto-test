# -*- coding: utf-8 -*-
import wx
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#import time
#Name=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
def execCmd(cmd): 
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text 
def isdevices():
    m = "device"
    os.system("adb kill-server") 
    mob = execCmd("adb devices")
    mob1 = mob[-8:]
    if (m in mob1):
        return True
    else:
        return False

def logcat(event):
    logButton.Enable(False)
    ass = isdevices()
    if (ass):
        log = os.system("adb logcat -v time -d > logcat.txt")
        os.system("notepad logcat.txt") 
        logButton.Enable(True)
    else:
        dial = wx.MessageDialog(None, u"手机没有连上，请先连上手机！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
        dial.ShowModal() 
        logButton.Enable(True)

def logcrash(event):
    crashButton.Enable(False)
    ass = isdevices()
    if (ass):
        log = os.system("adb shell dumpsys dropbox --print > logcat_crash.txt")
        os.system("notepad logcat_crash.txt")
        crashButton.Enable(True)
    else:
        dial = wx.MessageDialog(None, u"手机没有连上，请先连上手机！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
        dial.ShowModal()
        crashButton.Enable(True) 
           
def message(event):
    mesButton.Enable(False)
    ass = isdevices()
    if (ass):
         brand = execCmd("adb shell getprop ro.product.brand") #品牌
         name = execCmd("adb shell getprop ro.product.device") #名称
         model = execCmd("adb shell getprop ro.product.model") #型号
         version = execCmd("adb shell getprop ro.build.version.release") #安卓版本
         mes = u"品牌: " + brand + u"\n名称：" + name + u"\n型号：" + model + u"\n安卓版本：" + version
         f = open('mes.txt', 'w')
         f.write(mes)
         f.close()
         os.system("notepad mes.txt")
         mesButton.Enable(True)
    else:
        dial = wx.MessageDialog(None, u"手机没有连上，请先连上手机！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
        dial.ShowModal()
        mesButton.Enable(True) 
   

def screenshot(event):
    screenButton.Enable(False)
    ass = isdevices()
    if (ass):
        screen = os.system("adb shell screencap -p /sdcard/screen.png")
        screen_pull = os.system("adb pull /sdcard/screen.png D:/")
        dial = wx.MessageDialog(None, u"截图已经保存在D盘了", u"提示信息", wx.OK | wx.ICON_INFORMATION) 
        dial.ShowModal()
        screenButton.Enable(True) 
    else:
        dial = wx.MessageDialog(None, u"手机没有连上，请先连上手机！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
        dial.ShowModal()
        screenButton.Enable(True)
    
def function(event):
    functionButton.Enable(False) 
    ass = isdevices()
    if (ass):
        pack = package_text.GetValue()
        if (pack == "") or (pack==' ' ):
            dial = wx.MessageDialog(None, u"请填写正确的包名！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
            dial.ShowModal()
        else:
            Memory = execCmd("adb shell dumpsys meminfo %s" % pack)
            cpu = execCmd("adb shell dumpsys cpuinfo " + ("\"|grep %s\"") % pack)
            mem = pack + u"的内存数据如下" + "\n" + Memory + "\n" + pack + u"的cpu使用情况如下：" + "\n" + cpu
            f = open('mem.txt', 'w')
            f.write(mem)
            f.close()
            os.system("notepad mem.txt")
        functionButton.Enable(True)
    else:
        dial = wx.MessageDialog(None, u"手机没有连上，请先连上手机！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
        dial.ShowModal()
        functionButton.Enable(True)

def monkey(event):
    monkeyButton.Enable(False) 
    ass = isdevices()
    if (ass):
        pack = package_text1.GetValue()
        num = package_text2.GetValue()
        if (pack == "" ) or (num=="" ):
            dial = wx.MessageDialog(None, u"请填写正确的包名和次数！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
            dial.ShowModal()
        else:
            per = "--pct-touch 35 --pct-motion 15 --pct-trackball 20 --pct-majornav 15 --pct-appswitch 15"
            ig = "-s %RANDOM% --throttle 400 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes -v"
            monkey = os.system("adb shell monkey -p %s %s %s %s> monkey.txt" % (pack, per, ig, num))
            dial = wx.MessageDialog(None, u"monkey日志已保存在monkey.txt文件里了", u"提示信息", wx.OK | wx.ICON_INFORMATION) 
            dial.ShowModal() 
        monkeyButton.Enable(True)
    else:
        dial = wx.MessageDialog(None, u"手机没有连上，请先连上手机！", u"提示信息", wx.OK | wx.ICON_EXCLAMATION) 
        dial.ShowModal()
        monkeyButton.Enable(True)  

    
app = wx.App()
win = wx.Frame(None, title=u'android测试工具', size=(780, 400))
wx_font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.LIGHT)  

logButton = wx.Button(win, label=u'所有log', pos=(150, 50), size=(150, 35)) 
logButton.SetFont(wx_font)
logButton.Bind(wx.EVT_BUTTON, logcat)

crashButton = wx.Button(win, label=u'crash的log', pos=(450, 50), size=(150, 35))  
crashButton.SetFont(wx_font)
crashButton.Bind(wx.EVT_BUTTON, logcrash)

mesButton = wx.Button(win, label=u'手机基本信息', pos=(150, 150), size=(150, 35))
mesButton.Bind(wx.EVT_BUTTON, message)
mesButton.SetFont(wx_font)

screenButton = wx.Button(win, label=u'手机截屏', pos=(450, 150), size=(150, 35))
screenButton.SetFont(wx_font)
screenButton.Bind(wx.EVT_BUTTON, screenshot)

static_text = wx.StaticText(win, -1, u'包名', pos=(110, 250))
static_text.SetBackgroundColour("White")  #颜色  
static_text.SetFont(wx_font)  

package_text = wx.TextCtrl(win, 1, pos=(170, 250), size=(150, 25), style=wx.TE_LEFT)  
        
functionButton = wx.Button(win, label=u'应用的性能数据', pos=(150, 280), size=(150, 35))
functionButton.SetFont(wx_font)
functionButton.Bind(wx.EVT_BUTTON, function)

static_text1 = wx.StaticText(win, -1, u'包名', pos=(380, 250))
static_text1.SetBackgroundColour("White")  #颜色  
static_text1.SetFont(wx_font)  

package_text1 = wx.TextCtrl(win, 2, pos=(430, 250), size=(150, 25), style=wx.TE_LEFT) 

static_text2 = wx.StaticText(win, -1, u'次数', pos=(590, 250))
static_text2.SetBackgroundColour("White")  #颜色  
static_text2.SetFont(wx_font)  

package_text2 = wx.TextCtrl(win, 2, pos=(640, 250), size=(80, 25), style=wx.TE_LEFT) 

monkeyButton = wx.Button(win, label=u'执行monkey', pos=(450, 280), size=(150, 35))
monkeyButton.SetFont(wx_font)  
monkeyButton.Bind(wx.EVT_BUTTON, monkey)

win.Show()
app.MainLoop()
