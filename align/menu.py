import nuke
import align

nuke.menu("Nuke").addCommand('Scripts/align', 'align.aligner()', 'ctrl+l')