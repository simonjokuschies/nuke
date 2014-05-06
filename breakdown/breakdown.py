###########################################################################################################
#
#  breakdown
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  create your shot breakdown list.
#  just select the nodes which you wnt to see in your breakdown. if you like you can also render out
#  all the steps as separate images. just activate the checkbox "create writes for each step" and set
#  a render path for the images. If you have all nodes that you want to have in your breakdownlist just
#  hit the "make breakdown"- button. 
#
#  instalation
#
#  put the whole breakdown directory in your nuke home directory.
#  in init.py write these line (without the '#' in the beginning):
#  nuke.pluginAddPath('breakdown')
#
#  you will find the breakdown widget under Pane->breakdown
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

global imgPath
imgPath = "breakdown.png"

def findMostLeftNode():
    '''
    find most left node in script to place the new created nodes left of these nodes
    return int x
    '''

    xCurrent=0
    for n in nuke.allNodes():
        x=n.xpos()
    
    for n in nuke.allNodes():
        if n==0:
            x=n.xpos()
        xCurrent=n.xpos() 
        if xCurrent<x:
            x=xCurrent          
    return x


def sortNodesByPosition(sel):
    '''
    sort all the nodes that are in the breakdownlist by the y-position in order to correctly
    built the shuffle pipes from top to bottom
    return: sorted array (node with lowest y position on top and with highest y position at the end)
    '''

    sel = sel
    selDict = {}
    sortedValues=[]
    sortedKeys=[]

    # built dictionary with nodes and y position
    for node in sel:
        selDict[node]=node.ypos()

    #append y position to new array
    for value in selDict.values():
        sortedValues.append(value)

    #sort array
    sortedValues.sort()

    #create new array with keys (=node names) based on sorted values array
    for v in sortedValues:
        for keys, values in selDict.items():
            if values == v:
                sortedKeys.append(keys)

    return sortedKeys


class BreakdownPanel(nukescripts.PythonPanel):
    '''
    dockable breakdown panel
    '''

    #breakdownlist - all nodes that are appended to the breakdownlist
    nuke.BREAKDOWNLIST=[]
    #breakdownknobs - all knobs that are created by the user (i.e. appended to the breakownlist)
    nuke.BREAKDOWNKNOBS=[]

    def __init__(self):
        '''
        init panel and knobs
        '''
        nukescripts.PythonPanel.__init__(self, 'breakdown', 'com.ohufx.breakdown')
        
        # CREATE KNOBS 
        self.home = nuke.PyScript_Knob('www.leafpictures.de', '<img src="%s" width = "450" height = "50">' % imgPath)
        self.div=nuke.Text_Knob("","","")
        self.writeEachStep = nuke.Boolean_Knob('writeEachStep', 'create writes for each step')    
        self.writeEachStep.setFlag(nuke.STARTLINE)
        self.renderPath = nuke.File_Knob('renderTo', '')    
        self.renderPath.setVisible(False)
        self.addToList = nuke.Script_Knob("addToList", "add selection")
        self.execute = nuke.Script_Knob("execute", "make breakdown")
        self.removeSelected = nuke.Script_Knob("removeUnchecked", "remove unchecked")
        
        #add knobs
        self.addKnob(self.home)
        self.addKnob(self.writeEachStep)
        self.addKnob(self.renderPath)
        self.addKnob(self.addToList)
        self.addKnob(self.removeSelected)
        self.addKnob(self.execute)
        self.addKnob(self.div)

    def knobChanged(self, knob):
        '''
        knob actions
        '''

        # toggle show/hide renderpath file input
        if knob.name()=="writeEachStep":
            if self.writeEachStep.getValue()==1:
                self.renderPath.setVisible(True)
            else:
                self.renderPath.setVisible(False)
        
        # remove all unchecked items
        if knob.name()=="removeUnchecked":
            
            deleteItems=[]

            #append all items to delete to array
            for k in nuke.BREAKDOWNKNOBS:
                if k.getValue()==0:
                    deleteItems.append(k.label())

            # remove all selected knobs from GUI and from breakdownlist
            for deleteItem in deleteItems:
                for k in nuke.BREAKDOWNKNOBS:
                    if deleteItem in k.label():
                        #remove knob from GUI
                        self.removeKnob(k)
                        #remove knob from array
                        nuke.BREAKDOWNKNOBS.remove(k)

            #remove all selected from breakdownlist
            for deleteItem in deleteItems:
                for k in nuke.BREAKDOWNLIST:
                    if k.name() in deleteItem:
                        nuke.BREAKDOWNLIST.remove(k)

        #add selected knobs to breakdown list
        if knob.name()=="addToList":
            i=len(nuke.BREAKDOWNLIST)
            for node in nuke.selectedNodes():
                if node not in nuke.BREAKDOWNLIST:
                    if node.Class()!="Viewer":
                        nuke.BREAKDOWNLIST.append(node)
                        self.new = nuke.Boolean_Knob('breakdown_%d' % i , '%s' % node.name()) 
                        self.new.setFlag(nuke.STARTLINE)
                        self.new.setValue(True)
                        self.addKnob(self.new)
                        nuke.BREAKDOWNKNOBS.append(self.new)
                    else:
                        pass
                else:
                    nuke.message("%s is already in breakdown list" % node.name())
                i+=1

        #help  
        if knob.name()=="www.leafpictures.de":
            url = 'http://www.leafpictures.de/breakdown'
            webbrowser.open_new(url)

        # start make breakdown
        if knob.name()=="execute":
            
            def executeBreakdown():
                # sort based on y position in dag. the node that is most top goes in first
                sortedBreakdownlist = sortNodesByPosition(nuke.BREAKDOWNLIST)

                if len(sortedBreakdownlist)==0:
                    nuke.message("Please select some nodes to your breakdown list.")           
                elif len(sortedBreakdownlist)==1:
                    nuke.message("Please select more than one item.")
                else:
                    breakdown(sortedBreakdownlist, self.writeEachStep.getValue(),self.renderPath.getValue())

            if self.writeEachStep.getValue()==1:
                if self.renderPath.getValue()!="":
                    if os.path.isdir(self.renderPath.getValue()):
                        executeBreakdown()
                    else:
                        nuke.message("The render path is invalid. Please Choose another render path.")
                else:
                    nuke.message("Please choose a render path if you want to render out individual breakdown images.")
            else:
                executeBreakdown()

def breakdown(sel, createWrites, renderTo):
    '''
    create breakdown with all the shuffle nodes etc.
    '''

    createWrites=createWrites
    renderTo=renderTo
    sel=sel
    leftOffset=findMostLeftNode()-300
    i=0
    createdNodes=[]   

    for n in sel:
        
        #step01
        # step01 has some special features so all necessary steps here in a row
        if i==0:
            posX = sel[i].xpos()
            posY = sel[i].ypos()
            #shuffle
            shuffle = nuke.nodes.Shuffle()
            shuffle.setInput(0, sel[0])
            shuffle.setXpos(leftOffset)      
            shuffle.setYpos(posY)
            createdNodes.append(shuffle)
            
            #creating channels
            chTemp = "step%s" % (i+1)
            r_temp="step%s"% (i+1)+".red"
            g_temp="step%s"% (i+1)+".green"
            b_temp="step%s"% (i+1)+".blue"
            newLayer = nuke.Layer(chTemp,[r_temp, g_temp, b_temp])        
            
            #setting up the shuffle nodes inputs and outputs
            shuffle.knob("out").setValue(("step%s"% (i+1)))
            
            if createWrites:
                w = nuke.nodes.Write()
                w.setInput(0,shuffle)
                w.setXpos(leftOffset-120)
                w.setYpos(posY)
                w.knob("file").setValue(renderTo+"step%s.jpg"%(i+1))
                w.knob("channels").setValue("step%s"% (i+1))
    
             #remove
            remove = nuke.nodes.Remove() 
            remove.knob("operation").setValue("keep") 
            remove.knob("channels").setValue("step1")      
            remove.setInput(0, createdNodes[i])
            remove.setXpos(leftOffset)      
            remove.setYpos(posY+70)
            createdNodes.append(remove)
            i+=1

        #step02+
        #all next steps
        else:
            posX = sel[i].xpos()
            posY = sel[i].ypos()
            shuffle = nuke.nodes.ShuffleCopy()
            shuffle.setInput(1, sel[i])
            shuffle.setInput(0, createdNodes[i])
            shuffle.setXpos(leftOffset)      
            shuffle.setYpos(posY)
            createdNodes.append(shuffle)  
            
            #creating channels
            chTemp = "step%s" % (i+1)
            r_temp="step%s"% (i+1)+".red"
            g_temp="step%s"% (i+1)+".green"
            b_temp="step%s"% (i+1)+".blue"
            newLayer = nuke.Layer(chTemp,[r_temp, g_temp, b_temp])        
            #setting up the shuffle nodes inputs and outputs
            shuffle.knob("out2").setValue(("step%s"% (i+1)))  
            
            shuffle['red'].setValue('red2')
            shuffle['green'].setValue('green2')
            shuffle['blue'].setValue('blue2') 
            shuffle['alpha'].setValue('alpha2') 
            
            shuffle['black'].setValue('red') 
            shuffle['white'].setValue('green')
            shuffle['red2'].setValue('blue') 
            shuffle['green2'].setValue('alpha')
            
            if createWrites:
                w = nuke.nodes.Write()
                w.setInput(0,shuffle)
                w.setXpos(leftOffset-120)
                w.setYpos(posY)
                w.knob("file").setValue(renderTo+"step%s.jpg"%(i+1))
                w.knob("channels").setValue("step%s"% (i+1))
            i+=1

    #final
    layersheet = nuke.nodes.LayerContactSheet()
    layersheet.setInput(0, createdNodes[(len(createdNodes)-1)])
    layersheet.setXpos(leftOffset)      
    layersheet.setYpos(posY+50)
    createdNodes.append(layersheet)
    if createWrites:
        w = nuke.nodes.Write()
        w.setInput(0,layersheet)
        w.setXpos(leftOffset)
        w.setYpos(posY+150)
        w.knob("file").setValue(renderTo+"layersheet.jpg")
        w.knob("channels").setValue("rgb")


def addBreakdownPanel():
    global breakdownPanel
    breakdownPanel = BreakdownPanel()
    return breakdownPanel.addToPane()

