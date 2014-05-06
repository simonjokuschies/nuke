###########################################################################################################
#
#  smartRender
#  
#  @author simon jokuschies
#  @version 1.0
#
#  description:
#  the script creates a write node and fills in your selected choices from the 
#  panel and automatically creates a folder at the same place your nuke script is saved at.
#  it then sets the file name to output automatically based on your nuke scripts name and creates
#  a text files with notes you specified in the same directory where the render pictures go in.
#
##########################################################################################################

import nuke
import datetime
import os
import sys
import smartSaver
from smartSaver import smartSaver
from smartHelper import *

User = getUser()
#smart project setter
#load settings into array

projectPath=getSmartSettings("@projectPath")
artist=getSmartSettings("@artist")

scriptPath=getSmartSettings("@scriptPath")
renderPath=getSmartSettings("@renderPath")

#get and format time for unique render paths
def getTime():
    t = str(datetime.datetime.now())
    t = t.replace(' ', '_')
    t = t.replace(':','-')
    dArr = t.split(".")
    d=dArr[0]
    return d

# create panel
def createPanel():
    p = nuke.Panel('Smart Render')
    p.addBooleanCheckBox('autoexecute', True)
    p.addBooleanCheckBox('import render when finished', True)
    p.addEnumerationPulldown('channels', 'rgb rgba alpha all')
    p.addEnumerationPulldown('filetype', 'tiff png dpx exr cin jpeg mov abc cin dpx fpi hdr null pic sgi targa xpm yuv' )
    p.addSingleLineInput("render from:", int(nuke.Root()['first_frame'].value())) 
    p.addSingleLineInput("render to:", int(nuke.Root()['last_frame'].value())) 
    p.addMultilineTextInput('note', '')
    return p
    
def smartRender():

    sel = nuke.selectedNodes()
    
    if len(sel)>0:
        
        #create and show panel
        p = createPanel()    

        #getting and setting the path
        r=nuke.root()['name'].value() #root
        if r!="":
            
            #save script
            nuke.scriptSave()
            
            p.show()
            
            renderChannels=p.value("channels")
            renderFiletype=p.value("filetype")
            renderFromFrame=float(p.value("render from:"))
            renderToFrame=float(p.value("render to:"))
            importRender = p.value("import render when finished")
              
            rArray = r.split("/"); 
            rootLast = rArray[len(rArray)-1]
            rArray.pop() 
            renderpath = '/'.join(rArray)
            nameArray = rootLast.split(".")
            nameAndFolder=nameArray[0]         
            renderTo = renderpath+"/"+nameAndFolder
            
            print renderpath
            
            #split up to new location 
            renderToArr=renderTo.split("%s"%scriptPath)
            #keep only project path
            renderTo=renderToArr[0]
            
            #append renderpath and artist
            renderToFromArtist=renderTo+renderPath+"/"+artist
            #renderTo apend folder with name of the script
            renderTo=renderToFromArtist+"/"+nameAndFolder
            renderProjectDirTemp=renderToFromArtist+"/"+nameAndFolder
            renderProjectDirArr = renderProjectDirTemp.split("@")
            renderProjectDir = renderProjectDirArr[0]            

            projectNameArr=renderProjectDir.split("/")
            projectName=projectNameArr.pop()

            time="@"+renderProjectDirArr[1]          


            #set render up if not canceled
            if renderChannels is not None:
                
                #create folder if not exist
                if not os.path.isdir(renderProjectDir+"/"+projectName+time):
                    os.makedirs(str(renderProjectDir+"/"+projectName+time))
                
                #create write node 
                wr = nuke.nodes.Write(name="smart Render", inputs=sel, postage_stamp=True)
                wr.knob("file").setValue(renderProjectDir+"/"+projectName+time+"/"+nameAndFolder+"_%04d."+renderFiletype)
                wr.knob("channels").setValue(renderChannels)
                wr.knob("file_type").setValue(renderFiletype) 
                wr.knob("use_limit").setValue(True)
                wr.knob("first").setValue(renderFromFrame)     
                wr.knob("last").setValue(renderToFrame)     
                
                #write note
                if p.value('note')!="":
                    fobj_out = open(renderProjectDir+"/"+projectName+time+"/_rendernote.txt","w")
                    fobj_out.write(p.value("note"))
                    fobj_out.close()
    
                #autoexecute
                autoexecute=p.value("autoexecute")
                if autoexecute==True:
                    nuke.execute(wr,renderFromFrame,renderToFrame)   
                    nuke.delete(wr)
                    nuke.message("smart Render finished")
                    
                    #auto import
                    if importRender==True:
                        r =nuke.nodes.Read()
                        r.knob("name").setValue("smart rendered %s"%nameAndFolder)
                        r.knob("file").setValue(renderProjectDir+"/"+projectName+time+"/"+nameAndFolder+"_%04d."+renderFiletype)
                        r.knob("first").setValue(renderFromFrame)
                        r.knob("last").setValue(renderToFrame)
                    else:
                        pass
                    
                else:
                    pass
            else:
                pass
            
            #save, create new script so the script of the rendered version won't get changed from here
            smartSaver()
        else:
            nuke.message("You haven't safed your nuke project. Please make sure to save your project first in order to proceed.")
    
    else:
        nuke.message("Please select a node from where you want to render from")



