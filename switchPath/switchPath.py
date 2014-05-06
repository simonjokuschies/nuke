###########################################################################################################
#
#  switchPath
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  switch the path values of all read and write nodes 
#
#  instalation
#
#  put switchPath folder in nuke home directory
#  in init.py write (without "#"):
#  nuke.pluginAddPath("switchPath")
#
##########################################################################################################

# paths - put in here your default path changes
searchFor = "/Volumes/projects"
replaceWith = "S:/nhb/Projects"

'''
fileNodes
all nodes that carry a file knob
'''
global fileNodes

#fileNodes = ["Read", "Write", "ScannedGrain", "OCIOCDLTransform", "OCIOFileTransform", "Vectorfield", "GenerateLUT", "Axis2", "ReadGeo2", "WriteGeo", "Light2", "Camera2"]

fileNodes = {
              "Read" : "file",
              "Write" : "file",
              "ScannedGrain" : "fullGrain",
              "OCIOCDLTransform" : "file",
              "OCIOFileTransform" : "file",
              "Vectorfield" : "vfield_file",
              "GenerateLUT" : "file",
              "Axis2" : "file",
              "ReadGeo2" : "file",
              "WriteGeo" : "file",
              "Light2" : "file",
}

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke

def createPanel():
    p= nuke.Panel('switchOS')
    p.setWidth(400)   
    p.addSingleLineInput('search for', searchFor)    
    p.addSingleLineInput('replace with', replaceWith)    
    return p

def switchTo(searchFor, replaceWith):   
    searchFor=searchFor
    replaceWith=replaceWith
    
    for node in nuke.allNodes(): 
        #change all read  and write nodes
        if node.Class() in fileNodes.keys():
            print node.Class()
            filePath = node["file"].getValue()         
            #replace
            filePath = filePath.replace(searchFor, replaceWith)
            
            node["file"].setValue(filePath)
            
    
    for n in nuke.allNodes('Read'):
        n['reload'].execute()
    nuke.message("replaced\n '%s'" %searchFor + "\nwith \n'%s'" %replaceWith )

def switchPath():  
    p = createPanel()   
    if p.show():
        searchFor = p.value('search for')
        replaceWith = p.value('replace with')
        if searchFor!="" and replaceWith !="":
            switchTo(searchFor, replaceWith)
