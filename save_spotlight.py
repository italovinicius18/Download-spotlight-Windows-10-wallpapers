import os
import random
import shutil
import struct
import imghdr

def main():
    userprofile = input('Insert the user profile name: ')
    path = 'C:/Users/'+userprofile+'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'
    destinationFolder = './Spotlight_Wallpapers'
    copyFilesAndCreateDestFolder(path,userprofile,destinationFolder)
    renameFilesToJPG(destinationFolder)

def copyFilesAndCreateDestFolder(path,userprofile,destinationFolder):
    if not os.path.isdir(destinationFolder):
        os.mkdir(destinationFolder)

    for file in os.listdir(path):
        source = path+'/'+file
        if verifyWallpapers(source):
            shutil.copy(source, destinationFolder)

def renameFilesToJPG(destinationFolder):
    for file in os.listdir(destinationFolder):
        oldName = destinationFolder+'/'+file
        try:
            newName = oldName+'.jpg'
            os.rename(oldName,newName)
        except FileExistsError:
            oldName = destinationFolder+'/'+file
            file = ''.join(random.sample(file,len(file)))
            newName = destinationFolder+'/'+file+'.jpg'
            os.rename(oldName,newName)

def getImageSize(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

def verifyWallpapers(sourceImage):
    
    width,height = getImageSize(sourceImage)

    if height>1000:
        return True
    
    return False

if __name__ == "__main__":
    main()