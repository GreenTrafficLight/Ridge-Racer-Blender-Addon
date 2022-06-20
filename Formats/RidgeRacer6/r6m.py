from .r6o import *

class R6M:
    def __init__(self, binaryReader):
        self.br = binaryReader
        self.r6o = None

    def read(self):

        R6M_pos = self.br.tell()
        header = self.br.bytesToString(self.br.readBytes(4)).replace("\0", "")

        self.br.seek(4, 1) # zeros ?
        self.br.seek(4, 1) # offset to ?
        self.br.seek(4, 1) # offset to ?
        R6O_offset = R6M_pos + self.br.readUInt()

        self.br.seek(R6O_offset, 0)
        
        self.r6o = R6O(self.br)
