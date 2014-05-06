import nuke
import breakdown
from breakdown import *
from nukescripts import panels

paneMenu = nuke.menu('Pane')
paneMenu.addCommand('breakdown', addBreakdownPanel)
nukescripts.registerPanel('com.ohufx.breakdownPanel', addBreakdownPanel)