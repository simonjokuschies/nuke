###########################################################################################################
#
#  reloadAll
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  reload all assets inside dag
#
#  instalation
#
#  put revealInFinder folder in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('reloadAll')
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke

fileNodes =  ["Read","Write","ScannedGrain","OCIOCDLTransform","OCIOFileTransform","Vectorfield","GenerateLUT","Axis2","ReadGeo2","WriteGeo","Light2"]

def reloadAll():
    '''
    @author simon jokuschies
    @version 1.0
    @contact info@leafpictures.de

    description:
    reloads the file knob of all nodes that carry a file knob 
    '''
    for n in nuke.allNodes():
        if n.Class() in fileNodes:
            n['reload'].execute()
            print "reloaded %s" % n.name()