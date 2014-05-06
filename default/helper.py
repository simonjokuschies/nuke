def openFileReturnArr(file):
    '''
    open set file, read in all lines and
    return an array with all the lines
    '''
    arr=[]
    fobj = open("%s"%file, "r")
    #load in all lines
    for line in fobj:
        #delete word wrap at the end of each line
        line=line.replace("\n", "")
        arr.append(line)
    fobj.close()
    return arr