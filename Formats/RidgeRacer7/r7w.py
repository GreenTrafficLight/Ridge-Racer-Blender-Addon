from .r7o import *

class R7W:
    
    def __init__(self, br):
        self.br = br

        self.offset_list = []
        self.lod_offsets = []
        self.body_part_offsets = []

        self.lods = {
            "LOD0" : None,
            "LOD1" : None,
            "LOD2" : None,
            "LOD3" : None
        }

        self.br.seek(4, 1) # zeros
        
        self.get_offsets()
        self.read_lods()

    def get_offsets(self):        
        for lod_offset in range(4): # Get lods offset
            self.lod_offsets.append(self.br.readUInt())
        
    def read_lods(self):
        # Read LOD meshes
        lod_number = 0
        for lod_offset in self.lod_offsets:
            if lod_offset != 0:
                R7W_part = R7W.R7W_PART(self.br, lod_offset)
                self.lods["LOD" + str(lod_number)] = R7W_part
            lod_number += 1

    class R7W_PART(object):
        def __init__(self, br, part_offset):
            super().__init__()
            self.br = br
            self.submeshes = []

            submesh_offsets1 = []
            submesh_offsets2 = []

            br.seek(part_offset, 0)
            br.seek(4, 1)
            count1 = br.readUShort() # count of submesh ?
            count2 = br.readUShort() # count of submesh ?
            br.seek(32, 1)  # zeros ?

            self.get_submesh_offsets(submesh_offsets1, count1, part_offset)
            self.get_submesh_offsets(submesh_offsets2, count2, part_offset)

            self.read_r7o(submesh_offsets1)
            self.read_r7o(submesh_offsets2)

        def get_submesh_offsets(self, list, count, part_offset):
            for i in range(count):
                self.br.readUInt() # ?
                self.br.readUInt() # ?
                submesh_offset = self.br.readUInt()
                if submesh_offset != 0:
                    list.append(part_offset + submesh_offset) # offset to submesh data

        def read_r7o(self, submesh_offsets):
            for offset in submesh_offsets:
                self.br.seek(offset, 0)
                r7o = R7O()
                r7o.read(self.br)
                self.submeshes.append(r7o)