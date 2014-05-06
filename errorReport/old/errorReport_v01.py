import nuke
import os


# create panel
def createPanel():   
    p = nuke.Panel('Error Report')
    p.addFilenameSearch("output report to: ", "") 
    return p


def errorReport():
    
    p = createPanel()
    if p.show():

        script = os.path.basename(nuke.root().name())
        output= os.path.dirname(p.value("output report to: ")) + "errorReport_%s" % script.replace(".nk","")
        
        errorOutput = open(output,'w')

        title="error report \nscript name: %s" % script + "\nscript path:%s" % nuke.root().name()
        errorOutput.write(title)

        content=[]

        for node in nuke.allNodes():
            
            #special case read nodes - check all images of sequences
            if node.Class == "Read":
                for frame in range(int(node["first"].getValue()), int(node["last"].getValue())+1):
                    f = nukescripts.replaceHashes( sel['file'].value() ) % (frame)
                    if not os.path.isFile(f):
                        content.append(f)


            #all other nodes
            else:
                if node.hasError():
                    content.append(node.name())
                    try:
                        content.append(node["file"].getValue())
                    except Exception, e:
                        content.append("no file knob found")
                    content.append("----------")

        print report
        #open(outputPath,"w").write(content)
       

       

        


        #print filename

            
        
       


#errorReport()