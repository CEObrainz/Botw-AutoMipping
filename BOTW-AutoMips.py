import os, sys, struct

model_offset = 120
filename = sys.argv[1]

def writeTo(filename, position, content):
    fh = open(filename, "r+b")
    fh.seek(position)
    fh.write(content)
    fh.close()

def matCheck(filename, tempPos, number_of_mats):
    with open(filename, 'r+b') as f:        
        for j in range(1, number_of_mats + 1):
            matPos = tempPos + (j * 532) + 68
            f.seek(matPos)
            offset = struct.unpack(">l",f.read(4))[0]
            matPos = matPos + offset + 36
            f.seek(matPos)
            offset = struct.unpack(">l",f.read(4))[0]
            matPos += offset
            f.seek(matPos)
            mips = struct.unpack(">l",f.read(4))[0]
            miplist = list(map(hex,struct.unpack('>4B',struct.pack('>l',mips))))
            if miplist[1] == "0x0":
                pass
            else:
                mips -= 131072
                content = struct.pack('>l', mips)
                writeTo(filename, matPos, content)

with open(filename, 'rb') as f:
    f.seek(model_offset)
    number_Models = struct.unpack(">l",f.read(4))[0]
    startPos = model_offset + 4
    for i in range(1, number_Models + 1):
        tempPos = startPos + (i * 16) + 12
        f.seek(tempPos)
        offset = struct.unpack(">l",f.read(4))[0]
        tempPos = tempPos + offset + 24
        f.seek(tempPos)
        offset = struct.unpack(">l",f.read(4))[0]
        tempPos = tempPos + offset + 4
        f.seek(tempPos)
        number_of_mats = struct.unpack(">l",f.read(4))[0]
        matCheck(filename, tempPos, number_of_mats)
