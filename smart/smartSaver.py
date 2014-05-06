###########################################################################################################
#  smartSaver
#  
#  @author simon jokuschies
#  @version 1.0
#
#  description:
#  automatic background saver. Save a nuke script with its current date and time in the background
#  and drop it into the smartRecentScripts.txt - text file.
#  
#
##########################################################################################################

import nuke;
import datetime;
import os, sys;
from smartHelper import *

User = getUser()

#save the last xx latest scripts
saveNumberRecent = 20

# save current project to smartRecentScripts (textfile "smartRecentScripts.txt") so the latest version of
# the script gets to this file. It can then be loaded from the start menu.
# works like this: read all lines from the smartRecentScripts.txt file into an array, compare if the current
# project itself is in that list. If yes then drop it from that list and save the current script version at first
# item into smartRecentScripts.txt
def saveInSmartRecentScripts(currentScript):

    #get project dir of the current script
    scriptArr=currentScript.split("/")
    scriptArr.pop()
    scriptDir = "/".join(scriptArr)

    inp = open('/Users/%s/.nuke/smart/smartRecentScripts.txt'%User,'r')
    outp = open('/Users/%s/.nuke/smart/smartRecentScripts_w.txt'%User,'w')
    
    filelist=[]
    files=""
    i=0
    # add next line to path
    currentScript = currentScript+"\n"

    #read in the first 9 lines and put in arr filelist
    for line in inp:
        filelist.append(line)
        i+=1
        if i>=(saveNumberRecent-1):
           break

    #delete older scripts from the current script dir
    j=0
    for script in filelist:
        findVal=filelist[j].find("%s"%scriptDir)
        #if pattern found
        if findVal!=-1:
            del filelist[j]
        j+=1
     
    #fill files
    k=0
    for script in filelist:
        files = files + filelist[k]
        k=k+1
 
    #put current script first
    files=currentScript+files
    outp.write(files)
    
    #remove inp and rename outp to inp
    os.remove("/Users/%s/.nuke/smart/smartRecentScripts.txt"%User)
    os.rename("/Users/%s/.nuke/smart/smartRecentScripts_w.txt"%User, "/Users/%s/.nuke/smart/smartRecentScripts.txt"%User)
    
    inp.close()
    outp.close()
    
 
def smartSaver():
    
    r=nuke.root()['name'].value() #root
    
    if r!="":   
        rArray = r.split("/"); 
        rootLast = rArray[len(rArray)-1]
        rArray.pop() 
        directoryPath = '/'.join(rArray)
        nameArray = rootLast.split(".")
        projectName=nameArray[0]        
        
        #delete lastTime from project name        
        projectNameZeroDateArr = projectName.split("@")
        projectNameZeroDate = projectNameZeroDateArr[0]
     
        t = getTime()

        safeTo = directoryPath+"/"+projectNameZeroDate+"@"+t+".nk"
        nuke.scriptSaveAs(safeTo)
        #add current script to SmartRecentScripts
        saveInSmartRecentScripts(safeTo)
   
    else:
        nuke.message("You haven't saved your nuke project. Please make sure to save your project first in order to proceed.")
    
    
