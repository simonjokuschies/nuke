import nuke
import nextVersion

nuke.menu("Nuke").addCommand('Scripts/nextVersion', 'nextVersion.nextVersion()')
nuke.addOnUserCreate(nextVersion.addCustomElements, nodeClass = "Write")
nuke.addKnobChanged(nextVersion.performCustomAction, nodeClass = "Write")
