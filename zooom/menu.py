import nuke
import zooom
from zooom import *
from nukescripts import panels

initZooomData()

paneMenu = nuke.menu('Pane')
paneMenu.addCommand('zooom', zooom.addZooomPanel)
nukescripts.registerPanel('com.ohufx.zooomPanel', addZooomPanel)