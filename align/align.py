###########################################################################################################
#
#  align
#  
#  @author simon jokuschies
#  @version 2.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  automatically align selected nodes horizontally or vertically and decide the spacing.
#  update v02: the order the selected nodes had remain.
#
#  instalation
#
#  put script in nuke home directory
#  in menu.py write these two lines (without the '#'):
#  import align
#  nuke.menu("Nuke").addCommand('Scripts/align', 'align.aligner()');
#
##########################################################################################################

import nuke

global offset
global directions
global which
global offset

offset = 200

# no need to change anything from here. Change only if you exactly know what you're doing

def createPanel():
	'''
	aligner panel for user
	'''
	
	p=nuke.Panel('align')
	p.setWidth(400)   
	p.addEnumerationPulldown('direction', 'horizontal vertical')
	p.addSingleLineInput('offset', offset)      
	return p


def sortNodes(sel, which):
    '''
    sort all selected nodes by the x-position(if which is horizontal) or
    y-position (if which is vertical) in order to correctly
    align everything but remain the order the nodes had.
    return: array sorted by position (lowest to highest)
    '''

    sel = sel
    selDict = {}
    sortedValues=[]
    sortedKeys=[]

    # built dictionary with nodes and x-position or y-position
    for node in sel:
        if which == "horizontal":
        	selDict[node]=node.xpos()
        else:
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


def align(sel, which, offset):
	'''
	align nodes based on decission of user inputs (horizontal/vertical, offset)
	'''
	
	sumX=0
	sumY=0
	i=0

	#vertical
	if which == "vertical":
		
		#find most top node
		mostY=sel[0].ypos()
		for node in sel:
			if mostY>node.ypos():
				mostY=node.ypos()    
		
		sortedVertical = sortNodes(sel, "vertical")
				
		# sum up all xpos and get average
		for node in sortedVertical:
			sumX += node.xpos()
		avergageX = sumX / len(sortedVertical)

		#reposition
		for node in sortedVertical:
			node.setXpos(avergageX)
			node.setYpos(mostY +  i * int(offset) )
			i+=1

	#horizontal
	if which == "horizontal":

		#find most left node
		mostX=sel[0].xpos()
		for node in sel:
			if mostX>node.xpos():
				mostX=node.xpos() 

		sel = sortNodes(sel, "horizontal")

		# sum up all ypos and get average
		for node in sel:
			sumY += node.ypos()
		avergageY = sumY / len(sel)

		#reposition
		for node in sel:
			node.setYpos(avergageY)
			node.setXpos(mostX +  i * int(offset) )
			i+=1

def aligner():
	'''
	main 
	create panel and call align function
	'''
	sel = nuke.selectedNodes()
	
	if len(sel) > 1:
		p = createPanel()
		if p.show():
			which = p.value("direction")
			offset = p.value("offset")
			align(sel, which, offset)
	else:
		nuke.message("Please select more than one node.")


