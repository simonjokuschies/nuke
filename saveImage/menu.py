import nuke
import saveImage

nuke.menu("Nuke").addCommand('Scripts/save image', 'saveImage.imageSaver()')