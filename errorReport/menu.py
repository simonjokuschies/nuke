import nuke
import errorReport

nuke.menu("Nuke").addCommand('Scripts/errorReport', 'errorReport.runErrorReport()', 'alt+e')
nuke.menu("Nuke").addCommand('Scripts/checkForErrors', 'errorReport.checkForErrors()', 'alt+a')