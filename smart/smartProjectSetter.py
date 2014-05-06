###########################################################################################################
#
#  smartProjectSetter
#  
#  @author simon jokuschies
#  @version 1.0
#
#  description:
#  the smart project setter sets up a nuke project automatically based on your inputs.
#  make sure to set up the projectPath variable to where all your projects are located.
#  all projects are then automatically listed and the user can choose in which project he wants to work in
#  he just fills in a name and an comment (optional). Inside the project there will be created a folder based
#  on the name the user   put in the name field. The project is automatically put into that folder. 
#  
#  works with smartSaver and smartRender
#
#
##########################################################################################################

import nuke
import nukescripts
from smartSaver import *
import os, sys
import datetime
from smartHelper import *
from smartSetter import *

#get user name
User = getUser()
#load settings
showRecentFiles=getSmartSettings("@showRecentFiles")
artist = getSmartSettings("@artist")
#exclude these projects in the list to be shown and to be choosen from
dontIncludeProjects=[
    "__EpisodeWatch",
    "_Projekt_Projektnummer_Producer_Vorlage",
    "01_Temp"
]
global recentScriptsFile
recentScriptsFile = '/Users/%s/.nuke/smart/smartRecentScripts.txt' % User
# if cannot find recentScriptsFile create one
if not os.path.isfile(recentScriptsFile):
    loadFile = open(recentScriptsFile,'w')

def getAllProjects(path):
    projectsArr =[]
    projectsPath = path
    projectsPathArr = projectsPath.split("/")
    last = len(projectsPathArr)
    
    try:
        os.chdir(projectsPath)
        all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
        for dirs in all_subdirs:
            dir = os.path.join(projectsPath, dirs)
            os.chdir(dir)
            current = os.getcwd()
            project = str(current).split("/")[last]
            #cutout white space with custom unique character
            project = project.replace(" ", "**")
            #dont include hidden folders
            if project[0]!=".":
                dA=0             
                for dontAppend in dontIncludeProjects:
                    if project==dontAppend:
                        dA+=1
                #append if not in list
                if dA==0:
                    projectsArr.append(project)
        
        projectsArr.sort()
        return projectsArr
    except:
        #return empty projects array if projecpath doesn't exist; open smart setter
        return projectsArr


def getRecentProjects(projectPath):
    projectList=[]
    listTemp=[]
    
    rp = open(recentScriptsFile, "r")
    
    #read in latest number of scripts
    readNumberLatestScripts=15       
    rnls=0
    
    for line in rp:
        listTemp.append(line)
    rp.close()

    for pr in listTemp:
        pr=pr.replace(projectPath,"")
        prTempArr=pr.split("/")
        projectList.append(prTempArr[1])
        
        rnls+=1
        
        if rnls>=readNumberLatestScripts:
            break
    
    #return sorted list without duplicates
    projectList.sort()
    return set(projectList)


# create panel
def createPanel(projectPath):
    
    projectsPath = projectPath
    
    if os.path.isdir(projectPath):
    
        if showRecentFiles=="True":
            filelist=["---OpenRecentFile---"]
            fobj = open("/Users/%s/.nuke/recent_files"%User, "r")
            for line in fobj:
                filelist.append(line)
            fobj.close()
            recentFiles= ' '.join(filelist)
         
        latestScripts=["---OpenLatestScript---"]
        ls = open('/Users/%s/.nuke/smart/smartRecentScripts.txt'%User, "r")
        for line in ls:
            latestScripts.append(line)
        ls.close()
        latestScripts=' '.join(latestScripts)
        
        
        p = nuke.Panel('Smart Project Setter')
        p.setWidth(1000)
        
        
        if showRecentFiles=="True":
            p.addEnumerationPulldown('open recent file', recentFiles)
            
        p.addEnumerationPulldown('open latest script', latestScripts)
        rp = getRecentProjects(projectPath)
        recentProjects = ' '.join(rp)
        projects = ' '.join(getAllProjects(projectPath))
        projects = "---ChooseProject--- " + recentProjects + " -------------------- " + projects
    
        p.addEnumerationPulldown('create new script: ', projects)
        p.addSingleLineInput("artist: ", "%s"%artist) 
        p.addSingleLineInput("script name: ", "") 
        p.addMultilineTextInput("comment (optional): ", "")
        return p
    else:
        pass

def smartProjectSetter(projectPath, scriptPath, renderPath):
    projectPath = projectPath
    scriptPath=scriptPath
    renderPath=renderPath
        
    if os.path.isdir(projectPath):
    
        #setting up
        p = createPanel(projectPath)
        
        if p.show():
        
            userPath=p.value('create new script: ')
            #convert whitespace back
            userPath = userPath.replace("**", " ")
            artist = p.value('artist: ')
            
            scriptname=p.value('script name: ')
            scriptname=scriptname.replace(" ","_")
            scriptname=scriptname.replace("@","_")
            projectComment = p.value("comment (optional): ")
    
    
            #
            # actions
            #
            # 1 open recent
            # 2 open latest script
            # 3 create project
            
            #01 open recent
            recentFile=p.value("open recent file")
            
            #cancel button pressed
            if recentFile is None:
                recentFile="---OpenRecentFile---"
            
            if recentFile!="---OpenRecentFile---":
                def openRecent():
                    nuke.scriptOpen(recentFile) 
                    return True
        
                def thread_dispatch():
                    return nuke.executeInMainThreadWithResult(openRecent, ())
                
                thread.start_new_thread(thread_dispatch, ())
            
            #02 open latest script
            latestScript=p.value("open latest script")
            #cancel button pressed
            if latestScript is None:
                latestScript="---OpenLatestScript---"
            
            if latestScript!="---OpenLatestScript---":
                def openRecent():
                    nuke.scriptOpen(latestScript) 
                    return True
        
                def thread_dispatch():
                    return nuke.executeInMainThreadWithResult(openRecent, ())
                
                thread.start_new_thread(thread_dispatch, ())
           
            
            #03 create project    
            if userPath!="---ChooseProject---" and userPath!=" -------------------- ":
                
                #convert whitespace back
                if scriptname!="":
                    t=getTime()
                    
                    #create Folder
                    projectPath=getSmartSettings("@projectPath")
                    project = userPath
                    scriptPath = getSmartSettings("@scriptPath")
                    
                    #setting script and render folder
                    scriptFolder = projectPath + "/" + project + "/" + scriptPath + "/" + artist + "/" + scriptname
                    scriptsDir = scriptFolder + "/scripts"
                    footageFolderPath = scriptFolder + "/_footage"
                    trkFolder = scriptFolder + "/trk"
                    assetsFolder = scriptFolder + "/assets"
                    referencesFolder = scriptFolder + "/references"
                    fullScriptPath =  scriptsDir + "/" + scriptname + "@" + t  + ".nk" 
                    renderFolder = projectPath + "/" + project + "/" + renderPath + "/" + artist + "/" + scriptname
                   
                    #create scriptFolder, renderFolder, toFolder            
                    createFolders(scriptFolder)
                    createFolders(scriptsDir)
                    createFolders(footageFolderPath)
                    createFolders(trkFolder)
                    createFolders(assetsFolder)
                    createFolders(referencesFolder)
                    createFolders(renderFolder) 
              
                    #set root name
                    #when starting nuke and setting up project
                    nuke.knobDefault("Root.name", fullScriptPath)
                    #when setting up new project in between
                    nuke.root()['name'].setValue(fullScriptPath)
                         
                    if projectComment!="":
                        #write comment in root.label and create text file in project folder
                        #when starting nuke and setting up project
                        nuke.knobDefault("Root.label", projectComment)
                        #when setting up new project in between
                        nuke.root()['label'].setValue(projectComment)
                        
                        #create txt file
                        fobj_out = open(scriptFolder+"/_projectnote.txt","w")
                        fobj_out.write(projectComment)
                        fobj_out.close()
                    smartSaver()
    else:    
        if(scriptPath=="---" and renderPath=="---" and projectPath=="---"):
            nuke.message("Welcome to smart. Please make sure to insert all the inputs correctly in order to make .smart work correctly")
        else:
            nuke.message("Could not find the project path. Make sure that the path is set correctly")
        smartSetter()
