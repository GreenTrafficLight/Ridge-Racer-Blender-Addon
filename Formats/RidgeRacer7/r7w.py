from .r7o import *

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

    def read(self, binaryReader):

        binaryReader.seek(4, 1) # zeros
        
        self.get_offsets(binaryReader)
        self.read_lods(binaryReader)

    def get_offsets(self, binaryReader):        
        for lod_offset in range(4): # Get lods offset
            self.lod_offsets.append(binaryReader.readUInt())
        
    def read_lods(self, binaryReader):
        # Read LOD meshes
        lod_number = 0
        for lod_offset in self.lod_offsets:
            if lod_offset != 0:
                R7W_part = R7W.R7W_PART(binaryReader, lod_offset)
                self.lods["LOD" + str(lod_number)] = R7W_part
            lod_number += 1

    class R7W_PART(object):
        def __init__(self):
            super().__init__()
            
            self.submeshes = []

        def read(self, binaryReader, part_offset):

            submesh_offsets1 = []
            submesh_offsets2 = []

            binaryReader.seek(part_offset, 0)
            binaryReader.seek(4, 1)
            count1 = binaryReader.readUShort() # count of submesh ?
            count2 = binaryReader.readUShort() # count of submesh ?
            binaryReader.seek(32, 1)  # zeros ?

            self.get_submesh_offsets(binaryReader, submesh_offsets1, count1, part_offset)
            self.get_submesh_offsets(binaryReader, submesh_offsets2, count2, part_offset)

            self.read_r7o(submesh_offsets1)
            self.read_r7o(submesh_offsets2)

        def get_submesh_offsets(self, binaryReader, list, count, part_offset):
            for i in range(count):
                binaryReader.readUInt() # ?
                binaryReader.readUInt() # ?
                submesh_offset = binaryReader.readUInt()
                if submesh_offset != 0:
                    list.append(part_offset + submesh_offset) # offset to submesh data

        def read_r7o(self, binaryReader, submesh_offsets):
            for offset in submesh_offsets:
                binaryReader.seek(offset, 0)
                r7o = R7O()
                r7o.read(binaryReader)
                self.submeshes.append(r7o)