from .r6o import *

class R6M:
    def __init__(self):
        self.r6o = None

    def read(self, binaryReader):

        offsets = []

        R6M_pos = binaryReader.tell()
        header = binaryReader.bytesToString(binaryReader.readBytes(4)).replace("\0", "")
        binaryReader.seek(4, 1) # zeros ?

        for i in range(3):
            # offset 1 = submesh groups
            # offset 2 = ?
            # offest 3 = r6o
            offsets.append(R6M_pos + binaryReader.readUInt())

        binaryReader.seek(offsets[2], 0)
        
        self.r6o = R6O()
