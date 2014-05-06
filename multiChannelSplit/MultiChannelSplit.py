#################################################################
#  MultiChannelSplit
#  
#  @author simon jokuschies
#  @email info@leafpictures.de
#  @version 2.0
#
#  description:
#  the script splits a multichannel exr into single layers
#  and autocrops them automatically.
#
#  instalation
#
#  put script in nuke home directory
#  in menu.py write these two lines:
#  import MultiChannelSplit
#  nuke.menu("Nuke").addCommand('Scripts/MultiChannelSplit', 'MultiChannelSplit.MultiChannelSplit()');
#
#################################################################

import nuke
import os,sys

def getUniqueChannelLayerList(readNode):
    '''
    return all channel layer that are included in the selected read node
    return: string-array
    '''
    #function that returns unique channel layers
    rawChannelList = readNode.channels()    
    channelLayerList = []
    for channel in rawChannelList:
        channelLayer = channel.split(".")
        channelLayerList .append(channelLayer[0])
    return list(set(channelLayerList))

def createPanel():
    '''
    panel - prepare for render or not
    if set each shuffle node gets an own write node to render out the shuffled data
    in addition there will be a folder created for every channel layer
    return panel
    '''
    p = nuke.Panel('MultiChannelSplit')
    p.setWidth(400)
    p.addBooleanCheckBox("auto crop?", True)
    p.addBooleanCheckBox("prepare for output?", False)
    return p


def createPanel_renderloc():
    '''
    panel to set render location
    return panel
    '''
    p = nuke.Panel('MultiChannelSplit - set renderpath')
    p.setWidth(400)
    p.addFilenameSearch("render to: ", "")
    return p

def createFolders(path):
    '''
    create folder if not exist
    return true if suceeded, false otherwise
    '''
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
            return True
        except:
            return False

def MultiChannelSplit():
    '''
    main function
    split the selected read node in separate channel layers
    if set create separate folders and write nodes 
    '''
    selectedNodes = nuke.selectedNodes()
    lenSelectedNodes= len(selectedNodes)
    shuffles=[]
    renderTo=""
    p_renderLoc=None

    if len(selectedNodes)>0:
        
        p=createPanel()
        if p.show():
            if p.value("prepare for output?") == True:
                p_renderLoc = createPanel_renderloc()
                p_renderLoc.show()

            #main procedure
            #create shuffle, shuffle channel in, curvetool crop, create cropnode and paste that information in, delete crop node
            for readNode in selectedNodes:
                if readNode.Class()=="Read":
                    uniqueLayers = getUniqueChannelLayerList(readNode)
            
                    for channelLayer in uniqueLayers:
                        shuffleNode = nuke.nodes.Shuffle(name="Shuffle_"+channelLayer)        
                        shuffles.append(shuffleNode.name())
                        shuffleNode.knob("in").setValue(channelLayer)
                        shuffleNode.setInput(0,readNode)
                        
                        #auto crop if selected
                        if p.value("auto crop?")==True:
                            curveNode = nuke.nodes.CurveTool(name="Autocrop_"+channelLayer, inputs = [shuffleNode], operation="Auto Crop")
                            curveNode.knob("ROI").setValue([0,0,readNode.width(),readNode.height()])
                            nuke.execute(curveNode, readNode.knob("first").value(), readNode.knob("last").value())
                            cropNode = nuke.nodes.Crop(name="Crop_"+channelLayer, inputs = [curveNode])
                            cropNode.knob("hide_input").setValue(True)
                            cropNode.knob("box").copyAnimations(curveNode.knob("autocropdata").animations())
                            nuke.delete(curveNode)
                            cropNode.knob("postage_stamp").setValue(True)
                    
                        #create folders for all layer and create write node for every shuffle                       
                        if p_renderLoc!=None:
							renderTo = p_renderLoc.value("render to: ")
							#createFolder
							createFolders(renderTo+"/"+channelLayer)            
                            
							#create write node
							write = nuke.nodes.Write()
							write.knob("file_type").setValue("exr")
							write.knob("file").setValue(renderTo+channelLayer+"/"+channelLayer+"_%04d.exr")
							write.knob("compression").setValue("Zip (16 scanlines)")
							write.knob("channels").setValue("rgba")
 
							if p.value("auto crop?")==True:       
								write.setInput(0,cropNode) 
							else:
								write.setInput(0,shuffleNode) 
                    
                else:
                    nuke.message("No read node selected")
            
            #hide all created shuffle inputs
            for shuffleNode in shuffles:
                if p.value("auto crop?")==False:
                	temp = nuke.toNode(shuffleNode)
                	temp.knob("hide_input").setValue(True)
                	temp.knob("postage_stamp").setValue(True)

            
            nuke.message("Finished shuffling channels and autocropping them")
    else:
            nuke.message("Please select a read node first")