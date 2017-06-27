@ECHO OFF

rem 修改为自己电脑里SDK的路径
E:
cd E:\sdk\platform-tools
set dir=%~dp0
set fileName="%dir%shopnc_moneky_%date:~0,4%%date:~5,2%%date:~8,2%.txt"

rem 修改需要测试的包名
adb shell monkey -p test20.transsion.shopnc --pct-touch 40 --pct-motion 20 --pct-trackball 20 --pct-majornav 15 --pct-appswitch 5 -s %RANDOM% --throttle 400 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes -v -v 10000000>%fileName%
Pause