import os, sys, struct

model_offset = 120

def writeTo(filename, position, content):
    fh = open(filename, "r+b")
    fh.seek(position)
    fh.write(content)
    fh.close()

    
def mipTime(filename, position, number_mips):
    with open(filename, 'r+b') as f: 
        for k in range(1, number_mips + 1):
            pPos = 0
            print("Mip : " + str(k))
            pPos = position + (k * 16) + 12
            f.seek(pPos)
            offset = struct.unpack(">l",f.read(4))[0]
            pPos += offset
            f.seek(pPos)
            try:
                mips = struct.unpack(">l",f.read(4))[0]
            except:
                mips = 0
            print("Mip Value Before: " + str(mips))
            miplist = list(map(hex,struct.unpack('>4B',struct.pack('>l',mips))))
            if miplist[1] == "0x0":
                print("Pass")
                pass
            else:
                print("Edit")
                mips -= 131072
                content = struct.pack('>l', mips)
                print("Mip Value After: " + str(mips))
                print("Struct Version: " + str(content))
                writeTo(filename, pPos, content)
                print("Edited")
    
    
def matCheck(filename, tempPos, number_of_mats):
    with open(filename, 'rb') as f:      
        for j in range(1, number_of_mats + 1):
            mPos = 0
            print("Material Number : " + str(j))
            mPos = tempPos + 4 + (j * 16) + 12
            print("Mat Pos : " + str(mPos))
            f.seek(mPos)
            offset = struct.unpack(">l",f.read(4))[0]
            mPos += offset + 36 + 12
            f.seek(mPos)
            print(mPos)
            offset = struct.unpack(">l",f.read(4))[0]
            mPos += offset
            print(mPos)
            f.seek(mPos)
            mPos += 4
            f.seek(mPos)
            numberOfMips = struct.unpack(">l",f.read(4))[0]
            print("Number of Mips : " + str(numberOfMips))
            mipTime(filename, mPos, numberOfMips)

def main(filename):
    with open(filename, 'rb') as f:
        f.seek(32)
        ofsModelDict = struct.unpack(">l",f.read(4))[0]
        pointer = 32 + ofsModelDict
        f.seek(pointer)
        modelSize = struct.unpack(">l",f.read(4))[0]
        print("Size of Model (uint) : " + str(modelSize))
        pointer += 4
        f.seek(pointer)
        number_Models = struct.unpack(">l",f.read(4))[0]
        print("Number of Models : " + str(number_Models))
        pointer += 4
        for i in range(1, number_Models + 1):
            Mpointer = 0
            print("Model Number : " + str(i))
            Mpointer = pointer + (i * 16) + 12
            print(Mpointer)
            f.seek(Mpointer)
            ofsData = struct.unpack(">l",f.read(4))[0]
            Mpointer += ofsData + 24
            print(Mpointer)
            f.seek(Mpointer)
            ofsMaterialDict = struct.unpack(">l",f.read(4))[0]
            Mpointer += ofsMaterialDict + 4
            f.seek(Mpointer)
            number_Materials = struct.unpack(">l",f.read(4))[0]
            print("Number of Mats : " + str(number_Materials))
            print(Mpointer)
            matCheck(filename, Mpointer, number_Materials)
        print("Finished, have a nice day!")
           
if __name__ == "__main__":
    print(sys.version)
    if len(sys.argv) < 2:
        print('Insufficient arguments. Please supply a bfres file when using this tool.')
        exit()
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        p1 = struct.unpack(">s",f.read(1))[0]
        p2 = struct.unpack(">s",f.read(1))[0]
        p3 = struct.unpack(">s",f.read(1))[0]
        p4 = struct.unpack(">s",f.read(1))[0]
        word = str(p1+p2+p3+p4)
        word = word.replace("b", "").replace("'", "")
        if word == "Yaz0":
            print("Error 1: Encoded File Detected")
            print("This file has not been decoded yet." +
            " Please use BOTW-Yaz0 or Yaz0dec before using this tool.")
            exit()
        elif word != "FRES":
            print("Error 2: Unusual Filetype detected")
            print('File is the wrong format. Format Given : ' + str(word))
            exit()
        print("File Accepted...please wait while Mip-Maps are disabled.")
    main(filename)       
        
