@ECHO OFF
E:
cd E:\sdk\platform-tools
set dir=%~dp0
set fileName="%dir%report\logcat_%date:~0,4%%date:~5,2%%date:~8,2%.txt"
adb shell logcat -v time > %fileName%
Pause