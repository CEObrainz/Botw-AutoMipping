import os, sys, struct

model_offset = 120

def writeTo(filename, position, content):
    fh = open(filename, "r+b")
    fh.seek(position)
    fh.write(content)
    fh.close()

def matCheck(filename, tempPos, number_of_mats):
    with open(filename, 'r+b') as f:        
        for j in range(1, number_of_mats + 1):
            #print("Material Number : " + str(j))
            matPos = tempPos + (j * 532) + 68
            #print("Mat Pos : " + str(matPos))
            f.seek(matPos)
            offset = struct.unpack(">l",f.read(4))[0]
            matPos = matPos + offset + 36
            f.seek(matPos)
            #print(matPos)
            offset = struct.unpack(">l",f.read(4))[0]
            matPos += offset
            #print(matPos)
            f.seek(matPos)
            try:
                mips = struct.unpack(">l",f.read(4))[0]
            except:
                mips = 0
            #print("Mip Value Before: " + str(mips))
            miplist = list(map(hex,struct.unpack('>4B',struct.pack('>l',mips))))
            if miplist[1] == "0x0":
                #print("Pass")
                pass
            else:
                print("Edit")
                mips -= 131072
                content = struct.pack('>l', mips)
                #print("Mip Value After: " + str(mips))
                #print("Struct Version: " + str(content))
                writeTo(filename, matPos, content)
                #print("Edited")

def main():
    if len(sys.argv) < 2:
        #print('Insufficient arguments.')
        #print(sys.argv)
        exit()
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        f.seek(model_offset)
        number_Models = struct.unpack(">l",f.read(4))[0]
        #print("Number of Models : " + str(number_Models))
        startPos = model_offset + 4
        #print("Start Position : " + str(startPos))
        for i in range(1, number_Models + 1):
            #print("Model Number : " + str(i))
            tempPos = startPos + (i * 16) + 12
            #print("Position : " + str(tempPos))
            f.seek(tempPos)
            offset = struct.unpack(">l",f.read(4))[0]
            #print("Offset 1 : " + str(offset))
            tempPos = tempPos + offset + 24
            #print("Temp Pos : " + str(tempPos))
            f.seek(tempPos)
            offset = struct.unpack(">l",f.read(4))[0]
            #print("Offset 2 : " + str(offset))
            tempPos = tempPos + offset + 4
            #print("Temp Pos 2 : " + str(tempPos))
            f.seek(tempPos)
            number_of_mats = struct.unpack(">l",f.read(4))[0]
            #print("Number of Mats : " + str(number_of_mats))
            matCheck(filename, tempPos, number_of_mats)
        print("Finished, have a nice day!")
           
if __name__ == "__main__":
    main()       
        
