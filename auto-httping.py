# coding=utf-8

import time  # use to control time
import subprocess
import sys

num = 23

while num < 101:
	try:
		filename = "d:/httping" + str(num) + ".txt"
		ping_file = open(filename,"w")
		pingcmd = "httping -c110 34.251.210.107:8080"
		Popping = subprocess.Popen(pingcmd,stdout=ping_file,stderr=subprocess.PIPE)
		time.sleep(240)
		Popping.terminate()
		num = num + 1
	except:
		print(num + "error")


sys.exit()