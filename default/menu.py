import nuke
import default

nuke.menu("Animation").addCommand("default/set as new knobDefault", "default.createDefault()")
nuke.menu("Animation").addCommand("default/reset", "default.resetToDefault()")