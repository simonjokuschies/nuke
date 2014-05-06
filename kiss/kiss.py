###########################################################################################################
#
#  kiss
#  
#  @author simon jokuschies
#  @version 2.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  kiss function for nodes in nuke. Inspired by the kiss function in Flame and Smoke.
#  just press l to enable the kiss function. Drag a node next to another node and the selected
#  node's input will be connected to the nearby node's output. 
#
#  update v02: now you can also connect the output of your selected node with inputs of nearby nodes.
#  so like the other way around connection. 
#
#  instalation
#
#  put kiss directory in nuke home directory
#  in init.py write this line (without the '#' in the beginning):
#
#  nuke.pluginAddPath('kiss')
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke

global KISS
global nodeName
global nodeX
global nodeY
global nodeWidth
global nodeHeight

nodeName=[]
nodeX=[]
nodeY=[]
nodeWidth=[]
nodeHeight=[]

#force init nuke.KISS
try:
	nuke.KISS=False
except:
	nuke.KISS=False

def toggleKiss():
	'''
	globally toggle enable/disable the kiss function
	save node data
	'''

	#save all nodenames, positions and dimensions
	for node in nuke.allNodes():
		nodeName.append(node.name())
		nodeX.append(node.xpos())
		nodeY.append(node.ypos())
		nodeWidth.append(node.screenWidth())
		nodeHeight.append(node.screenHeight())

	#toggle KISS
	if nuke.KISS==False:
		nuke.KISS=True
		nuke.addKnobChanged(kissNodes)
		print "enable kiss"
	else:
		nuke.KISS=False
		nuke.removeKnobChanged(kissNodes)
		print "disable kiss"

def kissNodes():
	'''
	kiss function
	check if selectedNode is near other nodes. 
	If so then connect the input of the selectedNode to the nearby node
	'''

	sel = nuke.selectedNodes()
	nodeToConnect=""
	nX=0
	nY=0
	tollerance=30

	# selected node's position data
	if len(sel) > 0 and nuke.KISS==True:
		actNode = sel[0]
		nX = actNode.xpos()
		nY = actNode.ypos()

	#check for overlap between selected node and nearby nodes
	for i in range(0,len(nodeName)):
		if nX>=nodeX[i]-tollerance and nX <= ( nodeX[i] + nodeWidth[i]+tollerance):
			if nY>=nodeY[i]-100 and nY <= ( nodeY[i] + nodeHeight[i]+tollerance):
				if actNode.name() != nodeName[i] and nodeName[i] != "":
	
					nodeToConnect = nuke.toNode(nodeName[i])

					if nY < nodeY[i]:
						'''
						selected node is higher than the nearby node
						connect output of selected node to input of nearby node
						'''
						if (actNode.maxOutputs()>0):

							if nodeToConnect.maxInputs()>0:
								'''
								connect the next available input
								check which input is free and count
								'''
								k=0
								for inp in range(0,nodeToConnect.inputs()):
									if nodeToConnect.input(k)!=None:
										k+=1
									else:
										break

								nodeToConnect.setInput(k,actNode)
								nuke.removeKnobChanged(kissNodes)
								nuke.KISS=False

					else:
						'''
						selected node is under the nearby node
						connect input of selected node to output of nearby node
						'''
						if (actNode.maxInputs()>0):
							
							if nodeToConnect.maxOutputs()>0:
								'''
								connect the next available input
								check which input is free and count
								'''
								k=0
								for inp in range(0,actNode.inputs()):
									if actNode.input(k)!=None:
										k+=1
									else:
										break

								actNode.setInput(k,nodeToConnect)
								nuke.removeKnobChanged(kissNodes)
								nuke.KISS=False
									
					#no expression arrows
					try:
						_internal_expression_arrow_cmd()
					except:
						pass		
					break

					








