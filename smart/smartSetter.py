###########################################################################################################
#
#  smartValueSetter
#  @author simon jokuschies
#  @version 1.0
#  
#  description:
#  GUI for changing the values of all the smartSettings
#
###########################################################################################################

import nuke
import nukescripts
from smartSaver import *
import os, sys
import datetime
from smartHelper import *

smartOn=True
projectPath=""
artist=""
scriptPath=""
renderPath=""
overwirteSaveWithSmartSave=True
showRecentFiles=False
User=getUser()
smartSettingsInputPath = '/Users/%s/.nuke/smart/smartSettings.txt'%User
smartSettingsOutputPath = '/Users/%s/.nuke/smart/smartSettings_w.txt'%User

#get settings
smartOn=getSmartSettings("@smartOn")
projectPath=getSmartSettings("@projectPath")
artist=getSmartSettings("@artist")
scriptPath=getSmartSettings("@scriptPath")
renderPath=getSmartSettings("@renderPath")
overwirteSaveWithSmartSave=getSmartSettings("@overwirteSaveWithSmartSave")
showRecentFiles=getSmartSettings("@showRecentFiles")

if projectPath == "NONE" or projectPath=="":
    projectPath==""
if scriptPath == "NONE":
    scriptPath=""
if renderPath == "NONE":
    renderPath=""
if artist == "NONE":
    artist==""

def createPanel():
    p = nuke.Panel("SmartSetter")
    p.setWidth(850)
    #set loaded settings
    p.addBooleanCheckBox("enable smart on start", smartOn)
    p.addFilenameSearch("project path: ",projectPath)
    p.addSingleLineInput("default artist: ",artist)
    p.addSingleLineInput("script path inside a project: ",scriptPath)
    p.addSingleLineInput("render path inside a project: ",renderPath)
    p.addBooleanCheckBox("always smartSave", overwirteSaveWithSmartSave)
    p.addBooleanCheckBox("show recent files", showRecentFiles)
    return p

def updateSettings(settings, id, val):
    settings = settings
    j=0
    #search for id in settings, if found replace with new line 
    for line in settings:
        findVal=settings[j].find("%s"%id)
        #if pattern found
        if findVal!=-1:
            del settings[j]
            settings.insert(j,"@%s=%s"%(id,val))
            settings.insert(j+1,"\n")
        j+=1

def smartSetter():
    p=createPanel()
    
    if p.show(): 
       
        inp = open(smartSettingsInputPath,'r')
        smartOn=p.value("enable smart on start") 
        projectPath=p.value("project path: ")
        #delete last /
        if projectPath!="" and projectPath[-1]=="/":
            projectPath = projectPath[:-1]
            
        artist=p.value("default artist: ")
        scriptPath=p.value("script path inside a project: ")
        renderPath=p.value("render path inside a project: ")
        overwirteSaveWithSmartSave=p.value("always smartSave")
        showRecentFiles=p.value("show recent files")
        
        #read in settingsdocument and save per line
        settingsCont=[]
        for line in inp:
            settingsCont.append(line)
    
        #change settings
        updateSettings(settingsCont,"smartOn",smartOn)
        updateSettings(settingsCont,"projectPath",projectPath) 
        updateSettings(settingsCont,"artist",artist)
        updateSettings(settingsCont,"scriptPath",scriptPath)
        updateSettings(settingsCont,"renderPath",renderPath)    
        updateSettings(settingsCont,"overwirteSaveWithSmartSave",overwirteSaveWithSmartSave) 
        updateSettings(settingsCont,"showRecentFiles",showRecentFiles)
    
        #write settings in string for output
        outputSettings=""
        i=0
        for i in range(0,len(settingsCont)):
              outputSettings=outputSettings+ settingsCont[i]
    
        #update smartSettings
        outp = open(smartSettingsOutputPath,'w')
        outp.write(outputSettings)
        outp.close()
        
        #rename to original in order to overwrite
        os.rename('/Users/%s/.nuke/smart/smartSettings_w.txt'%User, '/Users/%s/.nuke/smart/smartSettings.txt'%User)
        
        if nuke.ask("Your nuke must be restarted before the updated settings work. restart now?"):
            nuke.scriptClose()



 
