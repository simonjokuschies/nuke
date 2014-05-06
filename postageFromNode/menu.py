import nuke
import postageFromNode

nuke.menu("Nuke").addCommand('Scripts/postageFromNode', 'postageFromNode.postageFromNode()', 'alt+ctrl+p')