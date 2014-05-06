###########################################################################################################
#
#  fastTrack
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  alt+f -> create track
#  alt+r -> set reference frame of tracker if a tracker was selected
#
#  instalation
#
#  put fastTrack in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('fastTrack')
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke

def setRefFrame():
	sel = nuke.selectedNode()
	if "Tracker" in sel.Class():
		sel.knob("reference_frame").setValue(nuke.frame())