import nuke
import blackbox
import blackboxHelper

nuke.menu("Nuke").addCommand('Scripts/blackbox/blackbox settings', 'blackbox.backupSetter()')
nuke.menu("Nuke").addCommand('Scripts/blackbox/open backup dir', 'blackbox.openBackupDir()')
nuke.menu("Nuke").addCommand('Scripts/blackbox/help', 'blackboxHelper.help()')