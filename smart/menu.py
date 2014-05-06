###########################################################################################################
#
#  smart
#  @author simon jokuschies
#  @version 1.0
# 
#  project management system for nuke projects
#  set up your preferences in smartSettings.txt and make sure that the folders entered exist
#  when nuke launches you will be presented a project management system.
#  just put in your project you want to work in and a script name. nuke will then handle
#  everything automatically for you which is saving the script in the right project in the
#  right place with current time in the name and render in the right project in the right place with
#  current time in the foldername
#
###########################################################################################################

import smartSetter
import smartProjectSetter
import smartRender
import smartSaver
from smartHelper import *
import getpass

#get user name
User = getpass.getuser()
#get values out of array
smartOn=getSmartSettings("@smartOn")
projectPath=getSmartSettings("@projectPath")
artist=getSmartSettings("@artist")
scriptPath=getSmartSettings("@scriptPath")
renderPath=getSmartSettings("@renderPath")
overwirteSaveWithSmartSave=getSmartSettings("@overwirteSaveWithSmartSave")


if smartOn=="True":
    #setting smartProjectSetter
    if nuke.root()['name'].value()=="":
        smartProjectSetter.smartProjectSetter("%s"%projectPath, "%s"%scriptPath, "%s"%renderPath)
    
#add to menu
if overwirteSaveWithSmartSave=="True":
    nuke.menu("Nuke").addCommand('File/Save', 'smartSaver.smartSaver()', 'ctrl+s')
    nuke.menu("Nuke").addCommand('.smart/smart saver', 'smartSaver.smartSaver()', 'ctrl+s')
else:
    nuke.menu("Nuke").addCommand('.smart/smart saver', 'smartSaver.smartSaver()', 'ctrl+alt+s')

nuke.menu("Nuke").addCommand('.smart/smart render', 'smartRender.smartRender()', 'ctrl+r')
nuke.menu("Nuke").addCommand('.smart/smart open/open script directory', 'smartOpen("scriptDir")')
nuke.menu("Nuke").addCommand('.smart/smart open/open render directory', 'smartOpen("renderDir")')
nuke.menu("Nuke").addCommand('.smart/smart ProjectSetter', 'smartProjectSetter.smartProjectSetter("%s"%projectPath, "%s"%scriptPath, "%s"%renderPath)', 'ctrl+e')
nuke.menu("Nuke").addCommand('.smart/smart settings', 'smartSetter.smartSetter()')
nuke.menu("Nuke").addCommand('.smart/help', 'openHelp()')
