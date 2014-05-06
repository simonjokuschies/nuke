###########################################################################################################
#
#  MultiChannelCombine
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  automatically shuffle copy all read nodes in one branch in order to write out one exr
#  containing all the input images
#
#  instalation
#
#  put script in nuke home directory
#  in menu.py write these two lines:
#  import MultiChannelCombine
#  nuke.menu("Nuke").addCommand('Scripts/MultiChannelCombine', 'MultiChannelCombine.MultiChannelCombine()');
#
##########################################################################################################

import nuke, nukescripts


# all the channels that will be recognized and renamed
# 'pattern recognized' : 'rename the whole la<er to this one'
global renameArr
renameArr = {
             'AO' : 'AO',
             'extra_tex_' : 'extra_tex_',
             'object_id'  : 'object_id_',
             'id_' : 'id',
             'motionvector'  : 'MV',
             'beauty' : 'B',
             'diffuse_color'  : 'diffCol',
             'direct_diffuse'  : 'dirDiff',
             'direct_diffuse_raw'  : 'dirDiffRaw',
             'indirect_diffuse'  : 'indirDiff',
             'indirect_diffuse_raw'  : 'indirDiffRaw',
             'direct_specular'  : 'dirSpec',
             'direct_specular_2' : 'dirSpec2',
             'indirect_specular' : 'indSpec',
             'indirect_specular2' : 'indSpec2',
             'reflection' : 'refl',
             'singleScatter'  : 'sglSctr',
             'emission'  : 'em',
             'refraction'  : 'refr',
             'deep_scatter'  : 'deepSc',
             'mid_scatter'  : 'midSc',
             'primary_specular'  : 'prmSpec',
             'secondary_specular'  : 'secSpec',
             'shallow_Scatte'  : 'shlSc',
             'direct_backlight'  : 'dirBL',
             'indirect_backlight'  : 'indirBL',
             'sss' : 'sss',
             'light_group_' : 'light_group_',
             'depth': 'depth',

             'shadow' : 'shadow',
             'uv' : 'uv',
             '_P_' : 'P',
             '_N_' : 'N',
             '_Z_' : 'Z'
            }

#no need to change anything from here. Edit only if you exactly know what you're doing.

def setLayerList(inputImages):
    output=[]  
    for p in inputImages:
        found=0
        for r in renameArr.keys():
            
            if r in p:
                
                #set layer name - get first piece of name (up to first "_") and remove the string "Layer" out of it
                pre=""
                temp=p.split("_")
                pre=temp[0]  
                pre = pre.replace("Layer", "")
                
                #special cases increasing numbers: get the number and drive it through
                if "light_group_" in p or "extra_tex_" in p or "id_" in p and not "object_id" in p:
                    what=""
                    
                    #distinguish between these 
                    if "light_group_" in p:
                        what="light_group_"    
                    if "extra_tex_" in p:
                        what="extra_tex_"      
                    if "id_" in p and not 'object_id' in p:
                        what="id_"      
                    
                    tempArr = p.split(what)
                    temp = tempArr[1]
                    tempArr = temp.split("_")
                    
                    #set shorter name
                    if what == "light_group_":
                        what="lightGroup_"
                        
                    if what == "extra_tex_":
                        what="extraTex_"
                        
                    layername = pre + "_" + what + tempArr[0]
                    
                else:
                    layername=pre + "_" + renameArr[r]
                
                output.append(layername)
                
                found=1
                break
        if found==0:
            output.append("")
    return output


# create panel
def createPanel(imageInput):
    
    imageInput=sorted(imageInput)
    renamed=setLayerList(imageInput)
    i=0
    p = nuke.Panel('MultiChannelCombine')
    p.setWidth(800)
    
    for s in imageInput:
        p.addSingleLineInput("%s" %s, renamed[i])
        i+=1

    p.addSingleLineInput("comment (optional): ", "")
    return p

def MultiChannelCombine():

    images = nuke.selectedNodes()
    passes=[]
    passesRename=[]
    lastPass=""
    pipe2=""
    i=0
    noread=0
    inputReads=[]
    
    if len(images)>1:
        
        #check if all selected nodes are read nodes
        imageIn=""
        for img in images:
            
            if img.Class()!="Read":
                noread+=1

        if noread==0:
            
            for img in images:
                
                #get file path
                readPath=img["file"].value()
                #split by "/" to get the image name
                readPathArr=readPath.split("/")
                #image name is last item of arr
                imageName=readPathArr[len(readPathArr)-1]
                #cut ending (.jpg, .png, .exr, etc...)
                imageRawArr = imageName.split(".")
                imageRawArr.pop()
                imageRaw = "".join(imageRawArr)   
                #cut padding %05d etc...
                if "%" in imageRaw:
                    temp=imageRaw.split("%")
                    imageRaw=temp[0]
                
                #cut "_" , "." and "-" if that is the last character
                if imageRaw!="":
                    if imageRaw[(len(imageRaw)-1)]=="_" or imageRaw[(len(imageRaw)-1)]=="." or imageRaw[(len(imageRaw)-1)]=="-" :
                       imageRaw=imageRaw[:-1]
                    
                inputReads.append(imageRaw)
                
            
            
            p = createPanel(inputReads)
           
            renamed = setLayerList(inputReads)
            
            if p.show():
                
                channelNames = []
                temp=0
                for cn in inputReads:
                    channelNames.append(p.value(inputReads[temp]))
                    temp+=1
                
                #check if all channels have a name
                isEmpty=0
                allUnder30Char = 0
                for c in channelNames:
                    if c == "":
                        isEmpty+=1
                    if len(c)>30:
                        allUnder30Char += 1 
                
                if isEmpty>0:
                    nuke.message("you haven't named all channels.")
                    MultiChannelCombine()
                    
                else:
                    
                    if allUnder30Char==0:
                        for img in images:
            
                            #autoplace selected nodes
                            nuke.autoplace(img)
                            
                            #get all the filenames to use them as pass name
                            imagePath = img.knob("file").value()  
                            imageSplit=imagePath.split("/")
                            lastVal = imageSplit.pop()     
                            #cutouts
                            lastVal = lastVal.split(".")    
                            passName = lastVal[0]  
                            #frame padding %
                            lastVal = passName.split("%")    
                            passName = lastVal[0]       
                            passes.append(passName)
                            
                            print "passes %s" % passes
                            
                            if i>0:
                                if i==1:
                                    #initialize pipe2 for first round 
                                    pipe2=images[0]
                               
                                print pipe2
                               
                                #creating shuffle
                                shuffle = nuke.nodes.ShuffleCopy()
                                
                                
                                
                                shuffle.setName("shuffle_%s" % channelNames[i])
                                shuffle.setInput(0, pipe2)
                                shuffle.setInput(1, images[i])
                                
                                #creating channels
                                r_temp=channelNames[i]+".red"
                                g_temp=channelNames[i]+".green"
                                b_temp=channelNames[i]+".blue"
                                newLayer = nuke.Layer(channelNames[i],[r_temp, g_temp, b_temp])        
                                
                                #setting up the shuffle nodes inputs and outputs
                                shuffle.knob("out2").setValue(channelNames[i])  
                                
                                shuffle['red'].setValue('red2')
                                shuffle['green'].setValue('green2')
                                shuffle['blue'].setValue('blue2') 
                                shuffle['alpha'].setValue('alpha2') 
                        
                                shuffle['black'].setValue('red') 
                                shuffle['white'].setValue('green')
                                shuffle['red2'].setValue('blue') 
                                shuffle['green2'].setValue('alpha') 
                                
                                
                                    #this was a reported bug; 
                                    #it's right that red2 is actually called black, green2 is actually called white, blue2 is actually called red2 and alpha2 is actually called green2
                                    #pretty strange but it is like that
                                    #look here:
                                    #http://forums.thefoundry.co.uk/phpBB2/viewtopic.php?t=5954&sid=5eba0be48c454bf34bc7bdf301983a21  
                                
                                #safe last shuffle for next round to pipe it in in shuffleknob pipe2
                                pipe2 = shuffle;
                         
                            i+=1
                        
                        #create metadata-tag when comment was set
                        lastShuffle = nuke.toNode("shuffle_"+channelNames[len(channelNames)-1])
                        commentVal=""
                        commentVal = p.value("comment (optional): ")
                        if commentVal!="":
                            md=nuke.nodes.ModifyMetaData()
                            md.knob("metadata").fromScript("{set comment %s}" % commentVal.replace(" ","_") )
                            md.setName("comment")
                            md.setInput(0,lastShuffle)
                        
                        #create write node
                        write = nuke.nodes.Write()
                        write.knob("file_type").setValue("exr")
                        write.knob("compression").setValue("Zip (16 scanlines)")
                        write.knob("channels").setValue("all")
                        if commentVal!="":
                            write.setInput(0,md)
                            write.knob("metadata").setValue("all metadata")
                        else:
                            write.setInput(0,lastShuffle)
                
                    else:
                        nuke.message("Wait, the channel names are too long. Pleae make sure, that each channel name is under 30 characters long. Otherwise the exr does not work properly.")
            
        else:
            nuke.message("Please make sure to select READ nodes only")
    else:
        nuke.message("Please select at least 2 Read Nodes")
    

