#!/usr/bin/python

import os
import sys
import time
import datetime
import commands
import httplib
import requests

gDebugMode = 1
gLogFile = "/home/ethos/gpu_crash.log"
gRigName = commands.getstatusoutput("cat /etc/hostname")[1]
gPrivateKey = commands.getstatusoutput("cat /etc/ethos/pushsafer")[1]
disconnectCount = 0
waitForReconnect = 1

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
  miner_hashes = [ int(x) for x in miner_hashes ] # have them without comma
  numGpus = int(commands.getstatusoutput("cat /var/run/ethos/gpucount.file")[1])
  numRunningGpus = len(filter(lambda a: a > 0, miner_hashes))
 
  if (numRunningGpus != numGpus):
    
    if (waitForReconnect == 1 and numRunningGpus == 0):      
      # all GPUs dead. propably TCP disconnect / pool issue
      # we wait 12 times to resolve these issues. this equals to 3 minutes. most likely appears with nicehash. 
      disconnectCount += 1            
      if (disconnectCount < 12):
        DumpActivity("Waiting for hashes back: " + str(disconnectCount))       
        time.sleep(15)
    else:
     disconnectCount = 0       
    
    DumpActivity("Rebooting (" + str(miner_hashes) + ")")

    if gPrivateKey:
        url = 'https://www.pushsafer.com/api' # URL de destination
        post_fields = {
              "t" : "RIG: " + gRigName + " rebooting", # Titre de la notification
              "m" : "Your rig : " + gRigName + " rebooting due to low HashRate: " + str(miner_hashes) + ".", # Message (corp) de la notification
              "s" : "",
              "v" : "",
              "i" : "37",
              "c" : "",
              "d" : "a",
              "u" : "https://verges.ethosdistro.com/graphs/?rig=" + gRigName + "&type=miner_hashes", # URL pour Android & IOS
              "ut" : "Open graphs link", # Titre de l'URL
              "k" : gPrivateKey
              } # Private key qui doit etre rensigne ligne 38

        result = requests.post(url, data=post_fields)
        DumpActivity(result)

    # auto-update to the newest version of the script
    os.system("curl -O https://raw.githubusercontent.com/jmverges/ethos_utilities/master/check_crash.py")
    
    #reboot
    os.system("sudo reboot")
    break
  else:
    time.sleep(15)

    
