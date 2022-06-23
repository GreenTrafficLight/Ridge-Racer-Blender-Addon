from .r7m import *


class ARCL:
    def __init__(self, binaryReader):
        self.br = binaryReader

        self.R7M_offsets = []
        self.path_offsets = []
        
        self.paths = []
        self.R7M_list = []

    def read(self, binaryReader):

        R7M_count = binaryReader.readUInt()
        R7M_offsetList = binaryReader.readUInt()
        path_offsetList = binaryReader.readUInt()

        binaryReader.seek(R7M_offsetList, 0)
        for offset in range(R7M_count):
            self.R7M_offsets.append(binaryReader.readUInt())

        binaryReader.seek(path_offsetList, 0)
        for path in range(R7M_count):
            self.path_offsets.append(binaryReader.readUInt())

        self.read_paths(binaryReader)

        self.read_R7M(binaryReader)

    def read_paths(self, binaryReader):
        
        for offset in self.path_offsets:
            binaryReader.seek(offset, 0)
            self.paths.append(binaryReader.readString())

    def read_R7M(self, binaryReader):
        
        count = 0
        for offset in self.R7M_offsets:
            binaryReader.seek(offset, 0)
            
            R7M_size = binaryReader.readUInt()
            R7M_offset = binaryReader.readUInt()

            binaryReader.seek(R7M_offset, 0)

            r7m = R7M()
            r7m.read(binaryReader)
            self.R7M_list.append(r7m)

            count += 1

            #if count == 5:
                #break