from .r7o import *

class R7M:
    def __init__(self):
        self.submesh_groups = []
        self.r7o = None

    def read(self, binaryReader):

        offsets = []

        R7M_pos = binaryReader.tell()
        header = binaryReader.bytesToString(binaryReader.readBytes(4)).replace("\0", "")
        binaryReader.seek(4, 1) # zeros ?

        for i in range(3):
            # offset 1 = submesh groups
            # offset 2 = ?
            # offest 3 = r7o
            offsets.append(R7M_pos + binaryReader.readUInt())

        binaryReader.seek(offsets[0], 0)
        self.read_submesh_groups(binaryReader)
        binaryReader.seek(offsets[2], 0)
        self.read_r7o(binaryReader)

    def read_submesh_groups(self, binaryReader):
        """
        Number of submesh linked to matrix transformation in map file
        """
        
        binaryReader.seek(4, 1)  # zeros ?
        count = binaryReader.readUInt() # submesh group count

        for i in range(count):
            submesh_count = binaryReader.readUInt()
            submesh_total_count = binaryReader.readUInt()
            self.submesh_groups.append((submesh_count, submesh_total_count))

    def read_r7o(self, binaryReader):        
        
        self.r7o = R7O()
        self.r7o.read(binaryReader)
