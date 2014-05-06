import nuke

def renderFinished():
	nuke.message("render finished")
		
nuke.addAfterRender(renderFinished)