#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#
# WARRANTY:
# Use all material in this file at your own risk. Hiranmoy Basak
# makes no claims about any material contained in this file.
#
# Contact: hiranmoy.iitkgp@gmail.com


#!/usr/bin/python
import os
import sys
import time
import datetime
import commands
 
gDebugMode = 1
gLogFile = "/home/ethos/gpu_crash.log"
gRigName = commands.getstatusoutput("cat /etc/hostname")[1]
 
def DumpActivity(dumpStr):
  print dumpStr
  pLogFile = open(gLogFile, "a")
  pLogFile.write("%s @ %s\n" % (dumpStr, str(datetime.datetime.now())))
  pLogFile.close()
 
 
# wait till 3 minutes runtime, so we can be sure that mining did start
while( float(commands.getstatusoutput("cat /proc/uptime")[1].split()[0]) < 3 * 60):
  time.sleep(5)
 
# start checking
while 1:
  miner_hashes = map( float, commands.getstatusoutput("cat /var/run/ethos/miner_hashes.file")[1].split("\n")[-1].split() )
  numGpus = int(commands.getstatusoutput("cat /var/run/ethos/gpucount.file")[1])
  numRunningGpus = len(filter(lambda a: a > 0, miner_hashes))
 
  if (numRunningGpus != numGpus):
    DumpActivity("Rebooting (" + str(miner_hashes) + ")")
    
    # todo: send optional request to external server to keep track of crashes
    
    # auto-update to the newest version of the script
    os.system("curl -O https://raw.githubusercontent.com/krtschmr/ethos_monitor/master/check_crash.py")
    
    #reboot
    os.system("sudo reboot")
    break
  else:
    time.sleep(15)

    
