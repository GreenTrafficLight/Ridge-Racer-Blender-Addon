from .r7o import *

from ...Utilities.binaryReader import BinaryReader

class MeshGroup:
    def __init__(self) -> None:
        self.subMeshCount: int = 0
        self.startIndex: int = 0

class R7M:
    def __init__(self):
        self.MeshGroups = []
        self.r7o = None

    def read(self, br: BinaryReader):
        R7M_pos = br.tell()
        header = br.bytesToString(br.readBytes(4)).replace("\0", "")
        br.seek(4, 1) # zeros ?

        offsets = []
        for i in range(3):
            # offset 1 = mesh groups
            # offset 2 = ?
            # offest 3 = r7o
            offsets.append(R7M_pos + br.readUInt())

        br.seek(offsets[0], 0)
        self.readMeshGroups(br)
        br.seek(offsets[2], 0)
        self.read_r7o(br)

    def readMeshGroups(self, br: BinaryReader):
        """
        Number of mesh linked to matrix transformation in map file
        """
        br.seek(4, 1)  # zeros ?
        count = br.readUInt() # submesh group count

        for i in range(count):
            meshGroup = MeshGroup()
            meshGroup.subMeshCount = br.readUInt()
            meshGroup.startIndex = br.readUInt()
            self.MeshGroups.append(meshGroup)

    def read_r7o(self, binaryReader):        
        self.r7o = R7O()
        self.r7o.read(binaryReader)
