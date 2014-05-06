###########################################################################################################
#
#  postageFromNode
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  create postageStamp from current selection, hide input, postage stamp the cerated node
#
#  instalation
#
#  put postageFromNode folder in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('postageFromNode')
#
##########################################################################################################

import nuke

# create panel
def createPanel(sel):

    p = nuke.Panel('Postage from Node')
    p.setWidth(300)  
    p.addSingleLineInput("Postage Name: ", "%s"% sel[0].name()) 
    return p
    
def postageFromNode():
    sel = nuke.selectedNodes()
    
    if len(sel)<1:
        nuke.message("Please select a node.")
    
    if len(sel)>1:
        nuke.message("Please select only one node")
        
    else:
        p = createPanel(sel)
        if p.show():
            #ps = nuke.nodes.PostageStamp(name="_" + p.value('Postage Name: '), postage_stamp=True, hide_input=True, tile_color=2529426687);
            
            ps = nuke.createNode("PostageStamp")
            #ps.setXpos(int(sel["xpos"].getValue()))
            #ps.setYpos(int(sel["ypos"].getValue())+100)
            ps["name"].setValue("_%s" % p.value('Postage Name: '))
            ps["postage_stamp"].setValue(True)
            ps["hide_input"].setValue(True)
            ps["tile_color"].setValue(2529426687)
            
            ps.setInput(0, sel[0])
            ps.setXpos(sel[0].xpos())
            ps.setYpos(sel[0].ypos() + 100)
            
            print sel[0].xpos()
            print sel[0].ypos()