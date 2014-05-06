import nuke
import os, sys

global gizmoLoadersetting
global home
global gizmosPath
gizmoLoaderSetting = os.getenv("HOME")+'/.nuke/gizmoLoad.txt'
home = os.path.abspath(os.getenv("HOME")+"/Dropbox/simons_stuff/_nuke/_NUKE_SIMON_MASTER/")
gizmosPath = home+"/gizmos/"
if not os.path.isdir(gizmosPath):
    os.makedirs(gizmosPath)

def createFolders(path):
    if not os.path.isdir(path):
         os.makedirs(path) 

def loadGizmosOnStart():
    #try to open gizmoLoadSetting
    #if it doesn't exist, create a new one
    
    if not os.path.isfile(gizmoLoaderSetting):
        loadFile = open(gizmoLoaderSetting,'w')
    
    loadDoc = open(gizmoLoaderSetting,'r')
    loadFiles=[]
    for line in loadDoc:
        line=line.replace("\n","")
        loadFiles.append(line)
    loadGizmos(loadFiles)


def createPanel(gizmoGroups):
    loadDoc = open(gizmoLoaderSetting,'r')
    loadFiles=[]
    for line in loadDoc:
        line=line.replace("\n","")
        loadFiles.append(line)

    gizmoGroups=gizmoGroups
    p= nuke.Panel('gizmoLoader')
    p.setWidth(400)   
    for i in gizmoGroups:
        if i in loadFiles:
            p.addBooleanCheckBox(i, True)
        else:
            p.addBooleanCheckBox(i, False)
    return p

def gizmoLoadSetter():
    allGizmosFolder = []
    if os.path.isdir(gizmosPath):
        gizmoDirsArr = os.listdir(gizmosPath)
    
        for i in gizmoDirsArr:
            if os.path.isdir(gizmosPath+"/"+i):
                allGizmosFolder.append(i)
    
        p = createPanel(allGizmosFolder)
        if p.show():
            loadArr=[]
            #update loadinglist
            for group in allGizmosFolder:
                groupValue=(p.value(group))
                if groupValue is True:
                    loadArr.append(group)
            outp = open(gizmoLoaderSetting,'w')
            loadOutput =""
            for i in loadArr:
                loadOutput=loadOutput+i+"\n"
            l = outp.write(loadOutput)
            outp.close
            loadGizmos(loadArr)
    else:
        nuke.message("gizmos folder not found")

def loadGizmos(loadArr):

    loadArr=loadArr
    # gizmos
    toolbar = nuke.menu('Nodes')

    #gizmosFolder laden
    gizmosFolder = []
    
    gizmoDirsArr = os.listdir(gizmosPath)
   
    for i in loadArr:
        gizmosFolder.append(i)
            
    for i in gizmosFolder:
        
        #does gizmogroup exist?
        if os.path.isdir(gizmosPath + i):
        
            #add to nodes toolbar    
            iconsPath = gizmosPath + i + "/icons/"
            
            nuke.pluginAddPath(home+"/gizmos/"+i)
            nuke.pluginAddPath(home+"/gizmos/"+i+"/gizmos")
            nuke.pluginAddPath(home+"/gizmos/"+i+"/icons")
            
            gizmoGroup = nuke.menu('Nodes').addMenu('%s'% i, icon='%s' % ((i+".png")))
            #load all gizmos in arr
            gizmosArr = []
            gizmosPathCont = []
            currentGizmoGroupPath = gizmosPath + i + "/gizmos"
            currentGizmoGroupIconPath = gizmosPath + i + "/icons"
            
            #does gizmos folder in group exist?
            if os.path.isdir(currentGizmoGroupPath):      
                gizmosPathCont=os.listdir(currentGizmoGroupPath)
                for i in gizmosPathCont:
                    if ".gizmo" in i:
                        gizmosArr.append(i)
                        for i in gizmosArr:
                            gIcon=i.replace("gizmo", "png")
                            gName=i.replace(".gizmo","")
                            gizmoGroup.addCommand('%s'% gName, "nuke.createNode('%s')"% i, icon='%s'% gIcon);
            else:
                #nuke.message("Could not find the gizmos folder in the group \"%s\"" %i+". Please make sure that it exists.")
                #create folder on the fly
                createFolders(currentGizmoGroupPath)
            
            #does icons folder in group exist?
            if not os.path.isdir(currentGizmoGroupIconPath):
                #nuke.message("Could not find the icons folder in the group \"%s\"" %i+". Please make sure that it exists.")
                #create folders on the fly
                createFolders(currentGizmoGroupIconPath)
                
        else:
            nuke.message("Could not load the gizmo group \"%s\"" %i+" because it was not found. Please make sure that it exists.")
                
                
#load gizmos on start
loadGizmosOnStart()