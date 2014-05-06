###########################################################################################################
#
#  errorReport
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#  @plugin: www.leafpictures.de/errorReport  
#
#  description:
#  check whole nodegraph on errors:
#      # check if all images of all read nodes exist
#      # check if all other nodes have errors
#   display all error nodes with a button to quickly jump to these error nodes
#   write out an error report to desired destination
#
#  instalation
#
#  put errorReport script in nuke home directory
#  in init.py add this line (without "#"):
#
#  nuke.pluginAddPath("errorReport")
#
##########################################################################################################

# no need to change anything from here. Change only if you exactly know what you're doing

import nuke
import nukescripts
import os
import time

def initSessionVars():
    '''
    init session vars
    '''
    try:
        nuke.errors_lenErrors=0
        nuke.errors_nodes=[]
        nuke.errors_footageBtn=[]
        nuke.errors_missingFrames=[]
    except:
        nuke.errors_lenErrors=0
        nuke.errors_nodes=[]
        nuke.errors_footageBtn=[]
        nuke.errors_missingFrames=[]

def checkForErrors():
    '''
    check existense of all images of all read nodes and all other nodes on error
    '''

    errors=[]
    nuke.errors_nodes=[]
    nuke.errors_lenErrors=0

    for node in nuke.allNodes():
        
        #special case read nodes - check all images of sequences
        if node.Class() == "Read":
            for frame in range(int(node["first"].getValue()), int(node["last"].getValue())+1):
                try:
                    f = nukescripts.replaceHashes(node['file'].value() ) % (frame)
                except:
                    f = ""
                if not os.path.isfile(f):
                    errors.append(f)
                    if f not in nuke.errors_missingFrames:
                        nuke.errors_missingFrames.append(f)
                    if node not in nuke.errors_nodes:
                        nuke.errors_nodes.append(node)
                       
        #all other nodes
        else:
            if node.hasError() == True:
                
                errors.append(node.name())

                if node not in nuke.errors_nodes:
                    nuke.errors_nodes.append(node)
                   
    if len(errors)>0:
        nuke.errors_lenErrors=len(errors)
    else:
        nuke.message("No errors found in script.")

class errorReportPanel(nukescripts.PythonPanel):
    '''
    errorReportPanel
    '''

    def __init__( self ):
        
        nukescripts.PythonPanel.__init__(self, "error report", "error report")
    
        if nuke.errors_lenErrors==0:
            col="green"
        else:
            col="red"
        countErrors = '<span style="color:{col}">{countErr}</span>'.format(col=col, countErr=nuke.errors_lenErrors)
        #create elements
        self.errorCount = nuke.Text_Knob( '', 'errors found: ', '%s' % countErrors)
        self.div = nuke.Text_Knob("","","")
        self.errorCount.setFlag(nuke.STARTLINE)
        self.outputPath = nuke.File_Knob('output to: ', '') 
        self.write = nuke.PyScript_Knob('write', 'write')   
        self.update = nuke.PyScript_Knob('update', 'update')
        self.outputPath = nuke.File_Knob('', 'outputPath')
        #add elements
        self.addKnob(self.errorCount)
        self.addKnob(self.outputPath)
        self.addKnob(self.write)
        self.addKnob(self.update)
        self.addKnob(self.div)
        #error node knobs
        for errorNode in nuke.errors_nodes:
            self.en = nuke.PyScript_Knob(errorNode.name(), errorNode.name())
            self.addKnob(self.en)   
            nuke.errors_footageBtn.append(self.en) 

    def showModalDialog( self ):
        result = nukescripts.PythonPanel.show(self)

    def knobChanged( self, knob ): 
     
        #update
        if knob.name()=="update":
            
            #reset
            for btn in nuke.errors_footageBtn:
                self.removeKnob(btn)

            nuke.errors_footageBtn=[]
            errors=[]
            nuke.errors_nodes=[]
            nuke.errors_missingFrames=[]
            
            with nuke.root():
                all = nuke.allNodes()
                for n in all: 
                    if n.Class()!="Read":
                        if n.hasError():    
                            errors.append(n.name())
                            if n not in nuke.errors_nodes:
                                nuke.errors_nodes.append(n)
                    else:
                        for frame in range(int(n["first"].getValue()), int(n["last"].getValue())+1):
                            try:
                                f = nukescripts.replaceHashes(n['file'].value() ) % (frame)
                            except:
                                f = ""
                            if not os.path.isfile(f):
                                errors.append(f)
                                if f not in nuke.errors_missingFrames:
                                    nuke.errors_missingFrames.append(f)
                                if n not in nuke.errors_nodes:
                                    nuke.errors_nodes.append(n)

            for errorNode in nuke.errors_nodes:
                self.en = nuke.PyScript_Knob(errorNode.name(), errorNode.name())
                self.addKnob(self.en)   
                nuke.errors_footageBtn.append(self.en) 
            
            nuke.errors_lenErrors=len(errors)
           
            if nuke.errors_lenErrors==0:
                col="green"
            else:
                col="red"
            countErrors = '<span style="color:{col}">{countErr}</span>'.format(col=col, countErr=nuke.errors_lenErrors)
            self.errorCount.setValue(countErrors)
         
        #write
        if knob.name()=="write":
            if self.outputPath.getValue()!="":
                try:
                    script = os.path.basename(nuke.root().name())
                    output= os.path.dirname(self.outputPath.getValue()) + "/errorReport_%s" % script.replace(".nk",".txt")

                    errorOutput = open(output,'w')
                    date = time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime())
                    header="error report \nscript name: {scriptname}\nscript path: {scriptPath}\ndate: {date}\nnumber of errors: {countErrors}\n------------------------------".format(scriptname=script, scriptPath=nuke.root().name(), date=date, countErrors=nuke.errors_lenErrors)
                    errorOutput.write(header)

                    #all read nodes
                    errorOutput.write("\nread nodes\n\n")
                    for n in nuke.errors_nodes:
                        if n.Class()=="Read":
                            errorOutput.write("read node: %s\n" % n.name())
                    #all missing frames
                    errorOutput.write("\n----------\nmissing frames\n\n")
                    for f in nuke.errors_missingFrames:
                        errorOutput.write("missing frame: %s\n" % f)
                    #all other nodes
                    errorOutput.write("\n----------\nother nodes\n\n")
                    for n in nuke.errors_nodes:
                        if n.Class()!="Read":
                            errorOutput.write("node: %s\n" % n.name())

                    nuke.message("successfully written error report to:\n\n%s" % output)
                except:
                    nuke.message("some error occured. The report could not be written.")
            else:
                nuke.message("Please enter a output path for the error report.")
         
        #all other error nodes   
        else:
            allNodes=nuke.allNodes()
            pKnob=knob.name()
            for n in allNodes:
                if n.name() == pKnob: 
                    nuke.zoom( 1, [ n.xpos(), n.ypos() ])
                    nukescripts.clear_selection_recursive()
                    n.setSelected(True)

def runErrorReport():
    '''
    main
    check for errors, save in session vars, show errorReportPanel
    '''
    initSessionVars()
    checkForErrors()

    if nuke.errors_lenErrors>0:
        errorReportPanel().show()
       


