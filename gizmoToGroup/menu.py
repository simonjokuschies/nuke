import nuke
import gizmoToGroup

nuke.menu("Nuke").addCommand('Scripts/gizmoToGroup', 'gizmoToGroup.replaceGizmoWithGroup()', 'alt+l')