###########################################################################################################
#
#  createReadWrite
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  create a read from selected write node to copy the file name of the write node directly into the read node
#
#  instalation
#
#  put createReadWrite folder inside nuke home directory. In your int.py write (without the '#'):
#  import default
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke

def createReadWrite():

	sel = nuke.selectedNode()

	if sel.Class() == "Write":
	    read = nuke.createNode("Read")
	    read.setXpos(int(sel["xpos"].getValue()))
	    read.setYpos(int(sel["ypos"].getValue()+50))
	    read["file"].setValue(sel["file"].getValue())
	    read["first"].setValue(int(nuke.Root()['first_frame'].getValue() ))
	    read["last"].setValue(int(nuke.Root()['last_frame'].getValue() ))
	    read["origfirst"].setValue(int(nuke.Root()['first_frame'].getValue() ))
	    read["origlast"].setValue(int(nuke.Root()['last_frame'].getValue() ))
	    read["colorspace"].setValue(int(sel["colorspace"].getValue()))
