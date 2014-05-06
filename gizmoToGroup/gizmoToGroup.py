###########################################################################################################
#
#  gizmoToGroup
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  replace selected gizmo with group, rename the group to the old gizmo name and pipe all the existing
#  inputs into that group. basically replace the gizmo with the group.
#  This is helpfull to open the script on other machines where the gizmos are not installed.
#
#  instalation
#
#  put gizmoToGroup folder nuke home directory and in your int.py write (without the '#'):
#  import gizmoToGroup
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke, nukescripts

def gizmoToGroup(sel):
    '''
    main function
    all procedures to replace a gizmo with the corresponding group
    '''
    sel=sel
    selName=""
    selInputs=[]
    x=0
    y=0
    
    for gizmo in sel:
    
        if len(sel)>0: 
            try:
                type = gizmo.Class().split(".")[1]
            except:
                type=None
            
            if type=="gizmo":
                
                #save name of sel
                selName=gizmo.name()
              
                #get all inputs of gizmo
                for i in range (0,gizmo.inputs()):
                    selInputs.append(gizmo.input(i))
               
                #make group
                g = gizmo.makeGroup()
                
                #get coordinates
                x=gizmo.xpos()
                y=gizmo.ypos()
                
                #delete gizmo
                nuke.delete(gizmo)
                
                #rename
                g["name"].setValue(selName)
                
                #reposition
                g.setXpos(x)
                g.setYpos(y)
                
                #set all inputs back
                for i in range(0,len(selInputs)):
                    g.setInput(i,selInputs[i])
                    
                #selInputs=[]
                
            else :
                if gizmo.Class()=="Group":
                    nuke.message("%s is already a group" % gizmo.name())    
                else:
                    nuke.message("Please select a gizmo")    
            
        elif len(sel)==0:
            nuke.message("please select a gizmo")   
           
            
def replaceGizmoWithGroup():
    '''
    replace the selected gizmos with the corresponding groups
    '''
    
    sel = nuke.selectedNodes()
    if len(sel)==1:
        gizmoToGroup(nuke.selectedNodes())
    elif len(sel)>1:
        for n in sel:
            nukescripts.clear_selection_recursive()
            if "gizmo" in n.Class():
                n.setSelected(True)
                gizmoToGroup(nuke.selectedNodes())    
    else:
        pass