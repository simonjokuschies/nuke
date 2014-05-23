import nuke
import nukePluginManager
import nukescripts

nuke.menu('Pane').addCommand('Nuke Plugin Manager', nukePluginManager.addPMPanel)
nukescripts.registerPanel('com.ohufx.pluginManager', nukePluginManager.addPMPanel)

nukePluginManager.init()

