from .r7o import *

from ...Utilities.binaryReader import BinaryReader

class R7W:
    
    def __init__(self):

        self.offset_list = []
        self.lod_offsets = []
        self.body_part_offsets = []

        self.lods = {
            "LOD0" : None,
            "LOD1" : None,
            "LOD2" : None,
            "LOD3" : None
        }

    def read(self, br: BinaryReader):

        br.seek(4, 1) # zeros
        
        self.get_offsets(br)
        self.read_lods(br)

    def get_offsets(self, br: BinaryReader):        
        for lod_offset in range(4): # Get lods offset
            self.lod_offsets.append(br.readUInt())
        
    def read_lods(self, br: BinaryReader):
        # Read LOD meshes
        lod_number = 0
        for lod_offset in self.lod_offsets:
            if lod_offset != 0:
                R7W_part = R7W.PART(br, lod_offset)
                self.lods["LOD" + str(lod_number)] = R7W_part
            lod_number += 1

    class PART(object):
        def __init__(self):
            super().__init__()
            
            self.submeshes = []

        def read(self, br: BinaryReader, part_offset):

            submesh_offsets1 = []
            submesh_offsets2 = []

            br.seek(part_offset, 0)
            br.seek(4, 1)
            count1 = br.readUShort() # count of submesh ?
            count2 = br.readUShort() # count of submesh ?
            br.seek(32, 1)  # zeros ?

            self.get_submesh_offsets(br, submesh_offsets1, count1, part_offset)
            self.get_submesh_offsets(br, submesh_offsets2, count2, part_offset)

            self.read_r7o(submesh_offsets1)
            self.read_r7o(submesh_offsets2)

        def get_submesh_offsets(self, br: BinaryReader, list, count, part_offset):
            for i in range(count):
                br.readUInt() # ?
                br.readUInt() # ?
                submesh_offset = br.readUInt()
                if submesh_offset != 0:
                    list.append(part_offset + submesh_offset) # offset to submesh data

        def read_r7o(self, br: BinaryReader, submesh_offsets):
            for offset in submesh_offsets:
                br.seek(offset, 0)
                r7o = R7O()
                r7o.read(br)
                self.submeshes.append(r7o)