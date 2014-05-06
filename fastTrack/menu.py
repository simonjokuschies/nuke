import nuke
import fastTrack

nuke.menu("Nodes").addCommand("Transform/Tracker", "nuke.createNode('Tracker4')", 'alt+t', icon='Tracker.png')
nuke.menu("Nuke").addCommand('Edit/Node/Tracker set Ref Frame', 'fastTrack.setRefFrame()', 'alt+r')

nuke.knobDefault("Tracker1.label", "ref: [value reference_frame]")
nuke.knobDefault("Tracker2.label", "ref: [value reference_frame]")
nuke.knobDefault("Tracker3.label", "ref: [value reference_frame]")
nuke.knobDefault("Tracker4.label", "ref: [value reference_frame]")