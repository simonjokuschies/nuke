###########################################################################################################
#
#  smartHelper
#  
#  @author simon jokuschies
#  @version 1.0
#
#  description:
#  helper functions for smart
#
##########################################################################################################

import nuke
import thread
import getpass
import datetime
import os, sys
import subprocess
import webbrowser

def getUser():
    return getpass.getuser()

User = getUser()

#  open text file, read in all lines and
#  return an array with all the lines
def openFileReturnArr(file):
    arr=[]
    fobj = open("%s"%file, "r")
    #load in all lines
    for line in fobj:
        #delete word wrap at the end of each line
        line=line.replace("\n", "")
        arr.append(line)
    fobj.close()
    return arr

# getValues by finding pattern in array.
# for getting the valuesout of the array which
# comes from the settings text file
def getSmartSettings(val):
    smartSettings = "/Users/%s/.nuke/smart/smartSettings.txt"%User
    arr = openFileReturnArr(smartSettings)
    i=0
    for line in arr:
        findVal=arr[i].find("%s"%val)
        #if pattern found
        if findVal!=-1:
            val=arr[i]
            valArr=val.split("=")
            try:
                val=valArr[1] #value
                if val=="":
                    val=" "
                elif val=="NONE":
                    val=" "
            except:
                val="---"
        i+=1
    return val
     
#get and format time
def getTime():
    t = str(datetime.datetime.now())
    t = t.replace(' ', '_')
    t = t.replace(':','-')
    dArr = t.split(".")
    d=dArr[0]
    return d
    
def createFolders(path):
    if not os.path.isdir(path):
         os.makedirs(path) 

def smartOpen(which):
    if which =="scriptDir":
        path = "/".join((nuke.root().name()).split("/")[:-2])
    elif which == "renderDir":
        try:
            path = "/".join((nuke.root().name()).split("/")[:-2])
            currentPath = "/".join(path.split("/")[-2:])
            projectPath=getSmartSettings("@projectPath") + "/"
            currentProject = ("/".join((nuke.root().name()).split("/")))
            activeProject = (currentProject.split(projectPath)[1]).split("/")[0]
            renderPath=getSmartSettings("@renderPath")
            path = projectPath + activeProject+ "/" + renderPath + "/" + currentPath
        except Exception, e:
            path=""

    openFolderInExplorer(path)

def openFolderInExplorer(path):
    if os.path.isdir(path):
        if sys.platform == 'darwin':   
            subprocess.check_call(['open', '--', path])
        elif sys.platform == 'linux2':
            subprocess.check_call(['gnome-open', '--', path])
        elif sys.platform == 'windows':
            subprocess.check_call(['explorer', path])

    else:
        nuke.message("There was a problem opening the directory. The path to open doesn't seem to exist.")

def openHelp():
    url = 'http://www.leafpictures.de/smart'
    webbrowser.open_new(url)



