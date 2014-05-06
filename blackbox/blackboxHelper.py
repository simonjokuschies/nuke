import nuke
import sys
import os
import webbrowser
import subprocess

def openFileReturnArr(file):
    '''
    open set file, read in all lines and
    return an array with all the lines
    '''
    arr=[]
    fobj = open("%s"%file, "r")
    #load in all lines
    for line in fobj:
        #delete word wrap at the end of each line
        line=line.replace("\n", "")
        arr.append(line)
    fobj.close()
    return arr

def getBackupSettings(val, path):
    '''
    getValues by finding pattern in array.
    for getting the values out of the array which
    comes from the settings file
    '''
    path = path
    arr = openFileReturnArr(path)
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

def openFolder(path):
    if sys.platform == 'darwin':
        subprocess.check_call(['open', '--', path])
    elif sys.platform == 'linux2': 
        subprocess.check_call(['gnome-open', '--', path])
    elif sys.platform == 'windows':
        subprocess.check_call(['explorer', path])

def help():
    '''
    goto web
    '''
    url = 'http://www.leafpictures.de/blackbox'
    webbrowser.open_new(url)