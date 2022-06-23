from .r7o import *

class R7M:
    def __init__(self, binaryReader):
        self.br = binaryReader
        self.submesh_groups = []
        self.r7o = None

        offsets = []

        R7M_pos = self.br.tell()
        header = self.br.bytesToString(self.br.readBytes(4)).replace("\0", "")
        self.br.seek(4, 1) # zeros ?

        for i in range(3):
            # offset 1 = submesh groups
            # offset 2 = ?
            # offest 3 = r7o
            offsets.append(R7M_pos + self.br.readUInt())

        self.br.seek(offsets[0], 0)
        self.read_submesh_groups()
        self.br.seek(offsets[2], 0)
        self.read_r7o()

    def read_submesh_groups(self):
        """
        Number of submesh linked to matrix transformation in map file
        """
        
        self.br.seek(4, 1)  # zeros ?
        count = self.br.readUInt() # submesh group count

        for i in range(count):
            submesh_count = self.br.readUInt()
            submesh_total_count = self.br.readUInt()
            self.submesh_groups.append((submesh_count, submesh_total_count))

    def read_r7o(self):        
        self.r7o = R7O()
        self.r7o.read(self.br)
        #print(self.br.tell())
