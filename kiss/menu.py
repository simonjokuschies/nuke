import nuke
import kiss


nuke.menu('Nuke').addCommand('Edit/Node/toggle kiss', 'kiss.toggleKiss()', 'u', icon='kiss.png')

