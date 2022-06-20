from .r7m import *


class ARCL:
    def __init__(self, binaryReader):
        self.br = binaryReader

        self.R7M_offsets = []
        self.path_offsets = []
        
        self.paths = []
        self.R7M_list = []

        self.R7M_count = self.br.readUInt()
        R7M_offsetList = self.br.readUInt()
        path_offsetList = self.br.readUInt()

        self.br.seek(R7M_offsetList, 0)
        for offset in range(self.R7M_count):
            self.R7M_offsets.append(self.br.readUInt())

        self.br.seek(path_offsetList, 0)
        for path in range(self.R7M_count):
            self.path_offsets.append(self.br.readUInt())

    def read_paths(self):
        for offset in self.path_offsets:
            self.br.seek(offset, 0)
            self.paths.append(self.br.readString())


    def read_R7M(self):
        count = 0
        for offset in self.R7M_offsets:
            self.br.seek(offset, 0)
            
            R7M_size = self.br.readUInt()
            R7M_offset = self.br.readUInt()

            self.br.seek(R7M_offset, 0)

            r7m = R7M(self.br)
            self.R7M_list.append(r7m)

            count += 1

            #if count == 5:
                #break