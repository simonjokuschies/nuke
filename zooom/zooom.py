###########################################################################################################
#
#  zooom
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  widget to premanently save zoomlevel and x/y position in dag.
#  usefull to quickly switch from one part to other parts if you have a huge tree
#  how it works:
#  just set up the the zoomlevel and the position which you like to safe. set an name and click register
#  for each zoom setting there will be a separate button. with that you can toggle between different pretty quickly.
#  The smart thing is that the zoom-settings are saved inside your nukescript. so after quitting the script
#  and loading it again you'll still find all your zoom settings.
#
#  instalation
#
#  put the zooom folder inside your nuke home directory
#  in your init.py inside your home directory write this line: (without the "#" sign in the beginning)
#  nuke.pluginAddPath('zooom')
# 
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke
import os
import sys
import nuke
import nukescripts
from nukescripts import panels
import webbrowser

global zooomStart
global zooomEnd
global imgPath

zooomStart="#<zooom>"
zooomEnd='#</zooom>'
imgPath = "zooom.png"

def saveZooomdataOnClose():
    '''
    on script close write all nuke.ZOOOMDATA into script file
    '''
    currentScript=nuke.root()['name'].getValue()
    with open(currentScript, "a") as myfile:
            myfile.write("".join(nuke.ZOOOMDATA))
    
def initZooomData():
    '''
    read zooom data from script.
    if no zooomdata available return []
    if found return zooomdata as array
    '''
    zooomdata=[]
    nuke.root()["onScriptClose"].setValue("saveZooomdataOnClose()")
    
    #getZooomData from nuke script
    try:    
        currentScript=nuke.root()['name'].getValue()
        if os.path.exists(currentScript):     
            loadFile = open(currentScript,"r")
            foundZooomdata=False
            
            for line in loadFile:                
                
                if zooomStart in line :         
                    foundZooomdata=True                        
                
                if foundZooomdata:        
                    zooomdata.append(line)
                
                if zooomEnd in line :         
                    foundZooomdata=False
                    break  
        else:
            #no zooomData found
            pass
        
        #format zooomdata
        nuke.ZOOOMDATA=zooomdata
        return zooomdata
    
    except Exception, e:   
        print "nuke error. could'nt init zooomdata"
        pass

def registerPos(description):
    '''
    write item into nuke.ZOOOMDATA
    item must be next to last item which is the keyword for ending zooomdata 
    ''' 
    
    description=description.replace(" ", "_")
    
    if description !="":
        x = nuke.center()[0]
        y = nuke.center()[1]
        zooom = nuke.zoom()
        #format new zooomItem for nuke.ZOOOMDATA
        newZooomItem = "#"+description+",%d" % zooom +",%d" % x+",%d"% y +"\n" 
        
        #create start and end if not set yet
        if len(nuke.ZOOOMDATA)==0:
            nuke.ZOOOMDATA.append(zooomStart+"\n")
            nuke.ZOOOMDATA.append(zooomEnd)
        
        nuke.ZOOOMDATA.insert( (len(nuke.ZOOOMDATA)-1), newZooomItem)
    else:
        pass


def zooomTo(item):
    '''
    zooom to item
    '''
    try:
        zooomLevel=item.split(",")
        zooomLevel[3] = zooomLevel[3].replace("\n", "")
        nuke.zoom(float(zooomLevel[1]), [float(zooomLevel[2]), float(zooomLevel[3])])
        
        print "zooom to %s" % zooomLevel[0] 
        print zooomLevel[1]
        print zooomLevel[2]
        print zooomLevel[3]

    except Exception, e:
        pass

class zooomPanel(nukescripts.PythonPanel):
    '''
    dockable zooompanel widget
    ''' 
    nuke.ZOOOMKNOBS = {}
    
    def __init__(self):
        
        #read all the zooomdata of file
        initZooomData()
    
        #create panel
        nukescripts.PythonPanel.__init__(self, 'zooom', 'com.ohufx.zooomPanel')
        # CREATE KNOBS
        self.zooomHome = nuke.PyScript_Knob('www.leafpictures.de', '<img src="%s" width = "450" height = "50">' % imgPath)
        self.div00=nuke.Text_Knob(" "," "," ") 
        self.description = nuke.String_Knob('description', 'description:')
        self.register = nuke.PyScript_Knob('register', 'register')    
        self.div=nuke.Text_Knob("","","")    
        self.deleteZooomItem = nuke.PyScript_Knob('deleteZooomItem', 'deleteZooomItem')    
        
        #dynamically created knobs
        itemNames=[]
        buttons=[]
        i=0
        for item in nuke.ZOOOMDATA:
            if zooomStart not in item and zooomEnd not in item:
                itemTemp = item
                itemTemp = itemTemp.replace("#","")
                itemTemp = itemTemp.replace("\n","")
                itemNames.append(itemTemp.split(",")[0])
                buttons.append("pos_%d" % i)
                i+=1

        # ADD KNOBS
        self.addKnob(self.zooomHome)
        self.addKnob(self.div00)
        self.addKnob(self.description)
        self.addKnob(self.register)
        self.addKnob(self.deleteZooomItem)
        self.addKnob(self.div)
        
        #append dynamically created knobs
        i=0
        for b in nuke.ZOOOMDATA: 
            if zooomStart not in b and zooomEnd not in b:
                self.b = nuke.PyScript_Knob(b, itemNames[i])
                self.addKnob(self.b)        
                nuke.ZOOOMKNOBS[itemNames[i]] = self.b         
                i+=1

    def knobChanged(self, knob):
        '''
        register knob actions
        '''
        
        #register zooomItem
        if knob.name()=="register":

            if self.description.value()!="":

                if self.description.value() not in nuke.ZOOOMKNOBS.keys():
                    registerPos(self.description.value())     
                    newKnob=self.description.value().replace(" ","_")
                    self.new = nuke.PyScript_Knob('%s' %newKnob, self.description.value())
                    self.addKnob(self.new)
                    #add to zooomknobs
                    nuke.ZOOOMKNOBS[self.description.value()] = self.new
                    self.description.setValue("")
                else:
                    nuke.message("The zooom item '%s' already exists. Please choose another name." % self.description.value()) 
            else:
                nuke.message("Please give the zooom position a name")
        
        # delete zooomItem
        elif knob.name()=="deleteZooomItem":
            
            def deleteZooomItem():    
                p = nuke.Panel('Delete ZooomItem')
                p.setWidth(500)
                zooomItems=[]
                
                #add checkbox for each zooomDataItem
                for zooomItem in nuke.ZOOOMDATA:
                    if not zooomStart in zooomItem and not zooomEnd in zooomItem:
                        zooomItemName = zooomItem.split(",")[0]
                        #escape the first character which is '#'
                        zooomItemName=zooomItemName[1:]
                        zooomItems.append(zooomItemName)
                        p.addBooleanCheckBox(zooomItemName, False)
                      
                if p.show():
                    # register which zooomItems are to be deleted
                    deleteArray=[]
                    for zooomItem in zooomItems:
                        if p.value(zooomItem):
                            deleteArray.append(zooomItem)

                    # remove from nuke.ZOOOMDATA
                    for i in nuke.ZOOOMDATA:
                        for j in deleteArray:
                            if j == i:
                                itemToDelete = i
                                #remove from nuke.ZOOOMDATA
                                nuke.ZOOOMDATA.remove(itemToDelete)
                  
                    # remove knob from panel
                    for key, value in nuke.ZOOOMKNOBS.items():
                        for j in deleteArray:
                            if key == j:
                                knobToDelete = value
                                print knobToDelete
                                self.removeKnob(knobToDelete)
                                del nuke.ZOOOMKNOBS[j]     
                                
            deleteZooomItem()
        
        #help  
        elif knob.name()=="www.leafpictures.de":
            url = 'http://www.leafpictures.de/zooom'
            webbrowser.open_new(url)
        
        # press an zooomItem      
        else:
            loc = knob.name()
            #solve knobdata
            zooomActive=""
            
            for z in nuke.ZOOOMDATA:
                if loc in z:
                    zooomActive = z
                    break
                
            zooomTo(zooomActive)
                    
def addZooomPanel():
    global zooomPanel
    nuke.ZOOOMDATA=""
    zooomPanel = zooomPanel()
    return zooomPanel.addToPane()

#init zooom data for current script
nuke.addOnScriptLoad(initZooomData)

 

