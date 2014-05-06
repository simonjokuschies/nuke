###########################################################################################################
#
#  blackbox
#  
#  @author simon jokuschies
#  @version 2.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  automatically create backups of your script whenever you save it.
#  you can choose between a global backup directory or a backup directory per script directly sitting next
#  to your nuke script.
#  works with normal save, incremental save and save as.
#
#  instalation
#
#  put the whole blackbox folder in nuke home directory
#  in init.py write (without the '#'):
#  
#  nuke.pluginAddPath("blackbox")
#
#
#
#  Addition for version 2.0
#  set backupMinute, default set to true (description see below line 50)
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke
import nukescripts
import os
import time
import getpass
import blackboxHelper

global backupDir
global enableBackup
global backupPath
global numberOfBackups
global backupSettingsPath
global backupSettings
global backupMinute

backupSettingsPath = "/Users/%s/.nuke/blackbox" % getpass.getuser()
backupSettings = backupSettingsPath+"/blackbox.set"

# In a nutshell you won't have more than one backup per minute and thus not having 3 million backups of your nuke script.
# save backup only for every minute and not for every second.
# If set to true the name of the backup path contains only date_Hour-Minute. So you cannot produce a backup for every second.
# This results in not having 3 Million copies if you always press the save button.
# If set to true backups saved within a minute get overwritten.
backupMinute = True


'''
init backup settings values; create blank file with defaults if blackbox.set doesn't exist
'''
if not os.path.isfile(backupSettings):
    if not os.path.isdir(backupSettingsPath):
        os.makedirs(backupSettingsPath)
    loadBackupSettings = open(backupSettings,'w')
    open(backupSettings,"w").write("@enableBackup=1.0\n@backupPath=\n@operation=1.0\n@numberOfBackups=10")
enableBackup=blackboxHelper.getBackupSettings("@enableBackup", backupSettings)
backupPath=blackboxHelper.getBackupSettings("@backupPath", backupSettings)
operation=blackboxHelper.getBackupSettings("@operation", backupSettings)
numberOfBackups=blackboxHelper.getBackupSettings("@numberOfBackups", backupSettings)

class blackboxSettingsPanel(nukescripts.PythonPanel):
    '''
    blackbox panel
    '''
    def __init__( self ):
            '''
            init values
            '''
            enableBackup=blackboxHelper.getBackupSettings("@enableBackup", backupSettings)
            backupPath=blackboxHelper.getBackupSettings("@backupPath", backupSettings)
            operation=blackboxHelper.getBackupSettings("@operation", backupSettings)
            numberOfBackups=int(blackboxHelper.getBackupSettings("@numberOfBackups", backupSettings))
            
            if enableBackup == "1.0":
                enableBackup=True
            else:
                enableBackup=False

            nukescripts.PythonPanel.__init__(self, "Blackbox Settings", "Blackbox Settings")
            self.setMinimumSize(450,160)
        
            self.enableBackup = nuke.Boolean_Knob("enableBackup","enable backup",enableBackup)
            self.backupDirOp=nuke.Enumeration_Knob("operation","operation",["backup directory on global place","backup directory per script"])
            self.backupDirOp.setValue(str(operation))
            self.backupDirOp.resize(300, 30)
            self.backupPath = nuke.File_Knob('backupPath', 'backupPath')
            self.backupPath.setValue(backupPath)
            
            if operation == "0.0":
                self.backupPath.setVisible(True)
            else:
                self.backupPath.setVisible(False)
            
            self.numberOfBackups = nuke.String_Knob('numberOfBackups', 'number of backups')
            self.numberOfBackups.setValue(str(numberOfBackups))
            
            self.addKnob(self.enableBackup)
            self.addKnob(self.backupDirOp)
            self.addKnob(self.backupPath)
            self.addKnob(self.numberOfBackups)
    
    def show( self ):
        '''
        action performed when pressed ok
        '''
        result = nukescripts.PythonPanel.showModalDialog(self)
        
        if result:    
            def editBackupSettings():
                '''
                edit backup settings - write new values to blackbox.set
                '''
                enableBackup = self.enableBackup.getValue()
                backupPath = self.backupPath.getValue()
                backupDirOp = self.backupDirOp.getValue()
                numberOfBackups = self.numberOfBackups.getValue()
             
                if numberOfBackups.isdigit():   
                    if backupDirOp == 0:
                        if os.path.exists(backupPath):
                            pass
                        else:
                            nuke.message("The following directory you entered does not exist or is not valid: \n\n %s" % backupPath)
                            backupSetter()

                    #update settings
                    open(backupSettings,"w").write("@enableBackup={0}\n@backupPath={1}\n@operation={2}\n@numberOfBackups={3}".format(str(enableBackup),backupPath,backupDirOp,numberOfBackups))
                    toggleBackupProcess()
                else:
                    nuke.message("Your input for was wrong. Please enter a number")
                    backupSetter()
                
            editBackupSettings()
    
    def knobChanged( self, knob ): 
        '''
        panel knob changed actions
        '''
        enableBackup = self.enableBackup.getValue()
        backupPath = self.backupPath.getValue()
        numberOfBackups = self.numberOfBackups.getValue()
        
        if knob.name() == "operation":
            if self.backupDirOp.getValue() == 0:
                self.backupPath.setVisible(True)
            else:
                self.backupPath.setVisible(False)
            
def deleteOlderBackupVersions(path):
    '''
    delete all the older versions which are older than {all backups - max. backup number}
    '''
    numberOfBackups=int(blackboxHelper.getBackupSettings("@numberOfBackups", backupSettings))

    i=0
    files=""
    for file in os.listdir(path):
        if file.endswith(".nk"):
           files+="%s," %file
           i+=1

    filesArr = files.split(",")
    #little hack, delete last comma
    filesArr.pop()
    
    #only keep the latest versions
    if len(filesArr)>numberOfBackups:
        toDelete = len(filesArr) - int(numberOfBackups)
        for f in range(0,toDelete):
            os.remove(path+"/"+filesArr[f])
    
def makeBackup():
    '''
    make backup of script
    '''
    #get script name and make folder if not exist
    script = nuke.root().name()
    scriptName = (nuke.root().name().split("/")[-1]).replace(".nk","")
    operation=blackboxHelper.getBackupSettings("@operation", backupSettings)
    backupPath=blackboxHelper.getBackupSettings("@backupPath", backupSettings)
    numberOfBackups=int(blackboxHelper.getBackupSettings("@numberOfBackups", backupSettings))

    if backupMinute == True:
    	t = time.strftime("%y%m%d-%H%M")
    else:
    	t = time.strftime("%y%m%d-%H%M%S")

    # global dir
    if operation=="0.0":
        
        if not os.path.isdir(backupPath+"/"+scriptName):
            os.makedirs(backupPath+"/"+scriptName) 
        try:
            nuke.removeOnScriptSave(makeBackup)
            nuke.scriptSave(backupPath+"/"+scriptName+"/bckp_"+t+"_"+scriptName+".nk")
            nuke.addOnScriptSave(makeBackup)
        except Exception, e:
            nuke.message("couldn't write a backup file")

        deleteOlderBackupVersions(backupPath+"/"+scriptName)
    # per script
    else:
        backupPath = "/".join(nuke.root().name().split("/")[:-1])+"/_backups_%s" % scriptName
        if not os.path.isdir(backupPath):
            os.makedirs(backupPath)
        try:
            nuke.removeOnScriptSave(makeBackup)
            nuke.scriptSave(backupPath+"/bckp_"+t+"_"+scriptName+".nk")
            nuke.addOnScriptSave(makeBackup)
        except Exception, e:
            nuke.message("couldn't write a backup file")

        deleteOlderBackupVersions(backupPath)

def toggleBackupProcess():
    '''
    enable/disable blackbox - set by value in blackbox.set 
    '''
    #reload settings
    enableBackup=blackboxHelper.getBackupSettings("@enableBackup", backupSettings)
    backupPath=blackboxHelper.getBackupSettings("@backupPath", backupSettings)
    operation=blackboxHelper.getBackupSettings("@operation", backupSettings)
    numberOfBackups=blackboxHelper.getBackupSettings("@numberOfBackups", backupSettings)

    if enableBackup == "1.0":
        nuke.addOnScriptSave(makeBackup)
    else:
        nuke.removeOnScriptSave(makeBackup) 

def openBackupDir():
    '''
    open backup directory in explorer
    '''
    backupPath=blackboxHelper.getBackupSettings("@backupPath", backupSettings)
    operation=blackboxHelper.getBackupSettings("@operation", backupSettings)
    scriptName = (nuke.root().name().split("/")[-1]).replace(".nk","")

    # global dir
    if operation=="0.0":
        backupPath
        try:
            blackboxHelper.openFolder(backupPath+"/"+scriptName)
        except Exception, e:
            nuke.message("couldn't open backupPath. no such directory")
    # per script
    else:
        backupPath = "/".join(nuke.root().name().split("/")[:-1])+"/_backups_%s" % scriptName 
        try:
            blackboxHelper.openFolder(backupPath)
        except Exception, e:
            nuke.message("couldn't open backupPath. no such directory")

def backupSetter():
    blackboxSettingsPanel().show()

toggleBackupProcess()



            