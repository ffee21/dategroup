from os import listdir, mkdir, rename, rmdir
from os.path import isfile, join, getmtime, isdir, exists, splitext
from os import path
from datetime import datetime
from re import match
import time

def append_filename(originalfilepath, appendstr):
    filename = splitext(originalfilepath)[0]
    ext = splitext(originalfilepath)[1]
    filename = filename + appendstr
    return filename + ext

def isnumdir(d):
    if match("^1[0-9]$", d):
        return "yy"
    if match("^1[0-9](0[1-9]|1[012])$", d):
        return "yymm"
    if match("^1[0-9](0[1-9]|1[012])(0[1-9]|1[0-9]|2[0-9]|3[01])$", d):
        return "yymmdd"
    else:
        return False

def cleandir(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f)) and (isnumdir(f) == False)]

    def movefile(p):
        newdir = datetime.fromtimestamp(getmtime(join(mypath, p))).strftime("%y%m%d")
        newpath = join(mypath, newdir)
        oldlocation = join(mypath, p)
        newlocation = join(newpath, p)
        
        if not exists(newpath):
            mkdir(newpath)
        while exists(newlocation):
            newlocation = append_filename(newlocation, "_dup")
        try:
            rename(oldlocation, newlocation)    
        except:
            pass
    
    for p in onlyfiles:
        movefile(p)
    for p in onlydirs:
        movefile(p)

    def sortdirs(d):
        dirtype = isnumdir(d)

        curmonth = datetime.now().strftime("%y%m")
        curyear = datetime.now().strftime("%y")
        
        if dirtype == "yy":
            pass
        elif dirtype == "yymm" or dirtype == "yymmdd":
            def movetoparent(newparent, curparent):
                if match("^" + curparent, d):
                    pass
                else:
                    # past years' month directories
                    oldlocation = join(mypath, d)
                    newlocation = join(newparent, d)

                    if exists(newparent):
                        if exists(newlocation):
                            allsubfiles = listdir(oldlocation)
                            
                            exceptioncount = 0
                            for sf in allsubfiles:
                                try:
                                    newlocation2 = join(newlocation, sf)
                                    while exists(newlocation2):
                                        newlocation2 = append_filename(newlocation2, "_dup")
                                    rename(join(oldlocation, sf), newlocation2)
                                except:
                                    exceptioncount += 1
                            if exceptioncount == 0:
                                rmdir(oldlocation)
                        else:
                            try:
                                rename(oldlocation, newlocation)
                            except:
                                pass
                    else:
                        mkdir(newparent)
                        rename(oldlocation, newlocation)



            if dirtype == "yymm":
                np = join(mypath, d[:2])
                cp = curyear
                movetoparent(np, cp)
            else:
                np = join(mypath, d[:4])
                cp = curmonth
                movetoparent(np, cp)
        else:
            pass

    onlynumdirs = [f for f in listdir(mypath) if isdir(join(mypath, f)) and (isnumdir(f) != False)]
    for p in onlynumdirs:
        sortdirs(p)

    onlynumdirs = [f for f in listdir(mypath) if isdir(join(mypath, f)) and (isnumdir(f) != False)]
    for p in onlynumdirs:
        sortdirs(p)

maindir = 'C:\Google Drive\Download'
dirlist = ["C:\\Google Drive\\Download", "C:\\Users\\BigdataTeam1\\Downloads", "C:\\Google Drive\\pics2"]

for dirtoclear in dirlist:
    cleandir(dirtoclear)
