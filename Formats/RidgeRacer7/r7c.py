from .r7o import *

car_hierarchy = [
    "Body",

    "Hood_STOCK",
    "Hood_QUOX'S",
    "Hood_ARKBIRD",
    "Hood_DIG_DUG",
    "Hood_DRAGON_SABER",

    "Front_STOCK",
    "Front_QUOX'S",
    "Front_ARKBIRD",
    "Front_DIG_DUG",
    "Front_DRAGON_SABER",

    "Side_STOCK",
    "Side_QUOX'S",
    "Side_ARKBIRD",
    "Side_DIG_DUG",
    "Side_DRAGON_SABER",

    "Rear_STOCK",
    "Rear_QUOX'S",
    "Rear_ARKBIRD",
    "Rear_DIG_DUG",
    "Rear_DRAGON_SABER",

    "Wing_STOCK",
    "Wing_QUOX'S",
    "Wing_ARKBIRD",
    "Wing_DIG_DUG",
    "Wing_DRAGON_SABER"
]

class R7C:
    
    def __init__(self, br):
        self.br = br

        self.offsets = []
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
        self.offsets.append(self.br.readUInt())
        
        for lod_offset in range(4): # Get lods offset
            self.lod_offsets.append(self.br.readUInt())
        
        for offset in range(11):
            self.offsets.append(self.br.readUInt())

    def read_lods(self):
        # Read LOD meshes
        lod_number = 0
        for lod_offset in self.lod_offsets:
            if lod_offset != 0:
                R7C_lod = R7C.LOD(self.br, lod_offset)
                self.lods["LOD" + str(lod_number)] = R7C_lod
            lod_number += 1

    class LOD(object):
        def __init__(self, br, lod_offset):
            super().__init__()
            self.br = br

            self.hierarchy_dictionary = {car_hierarchy[p]: [] for p in range(len(car_hierarchy))}
            self.part_offsets = []

            br.seek(lod_offset, 0)
            self.get_part_mesh_offsets(lod_offset)
            self.read_parts()

        def get_part_mesh_offsets(self, lod_offset):

            for offset in range(26): # get offset of each body parts
                part_offset = self.br.readUInt()
                if part_offset == 0:
                    self.part_offsets.append(0)
                else:
                    self.part_offsets.append(lod_offset + part_offset)

        def read_parts(self):
            part_index = 0
            for part_offset in self.part_offsets:
                if part_offset != 0:
                    R7C.PART(self.br, part_offset, part_index, self.hierarchy_dictionary)
                part_index += 1

    class PART(object):
        def __init__(self, br, part_offset, part_index, hierarchy_dictionary):
            super().__init__()
            self.br = br

            self.submesh_offsets1 = []
            self.submesh_offsets2 = []

            br.seek(part_offset, 0)
            br.seek(4, 1)
            count1 = br.readUShort() # count of submesh ?
            count2 = br.readUShort() # count of submesh ?
            br.seek(32, 1)  # zeros ?

            self.get_submesh_offsets(self.submesh_offsets1, count1, part_offset)
            self.get_submesh_offsets(self.submesh_offsets2, count2, part_offset)

            self.read_r7o(self.submesh_offsets1, part_index, hierarchy_dictionary)
            self.read_r7o(self.submesh_offsets2, part_index, hierarchy_dictionary)

        def get_submesh_offsets(self, list, count, part_offset):
            for i in range(count):
                self.br.readUInt() # ?
                self.br.readUInt() # ?
                submesh_offset = self.br.readUInt()
                if submesh_offset != 0:
                    list.append(part_offset + submesh_offset) # offset to submesh data

        def read_r7o(self, submesh_offsets, part_index, hierarchy_dictionary):
            for offset in submesh_offsets:
                self.br.seek(offset, 0)
                r7o = R7O(self.br)
                hierarchy_dictionary[car_hierarchy[part_index]].append(r7o)
