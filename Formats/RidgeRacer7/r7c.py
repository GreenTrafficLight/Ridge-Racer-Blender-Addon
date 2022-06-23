from ...Utilities import *

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
    
    def __init__(self):
        self.offsets = []
        self.lod_offsets = []
        self.body_part_offsets = []

        self.lods = {
            "LOD0" : None,
            "LOD1" : None,
            "LOD2" : None,
            "LOD3" : None
        }

        self.transformations = {}

    def read(self, binaryReader):

        binaryReader.seek(4, 1) # zeros
        
        # offset 1 to 5 : lod offsets
        # offset 8 : transformations offsets
        self.get_offsets(binaryReader)
        
        self.read_lods(binaryReader)

        self.read_transformations(binaryReader)

    def get_offsets(self, binaryReader):        
        for offset in range(16):
            self.offsets.append(binaryReader.readUInt())

    def read_lods(self, binaryReader):
        # Read LOD meshes
        lod_number = 0
        for i in range(1, 5):
            if self.offsets[i] != 0:
                R7C_lod = R7C.LOD()
                R7C_lod.read(binaryReader, self.offsets[i])
                self.lods["LOD" + str(lod_number)] = R7C_lod
            
            lod_number += 1

    def read_transformations(self, binaryReader):

        if self.offsets[8] != 0:
            binaryReader.seek(self.offsets[8], 0)
            transformation_count = binaryReader.readUInt()
            for i in range(transformation_count):

                transformation = R7C.TRANSFORMATION()
                transformation.read_transformation(binaryReader)
                self.transformations[transformation.mesh_index] = transformation

    class LOD(object):
        
        def __init__(self):
            super().__init__()

            self.hierarchy_dictionary = {car_hierarchy[p]: [] for p in range(len(car_hierarchy))}
            self.part_offsets = []

        def read(self, binaryReader, lod_offset):

            binaryReader.seek(lod_offset, 0)
            self.get_part_mesh_offsets(binaryReader, lod_offset)
            self.read_parts(binaryReader)

        def get_part_mesh_offsets(self, binaryReader, lod_offset):

            for offset in range(26): # get offset of each body parts
                part_offset = binaryReader.readUInt()
                if part_offset == 0:
                    self.part_offsets.append(0)
                else:
                    self.part_offsets.append(lod_offset + part_offset)

        def read_parts(self, binaryReader):
            part_index = 0
            for part_offset in self.part_offsets:
                if part_offset != 0:
                    part = R7C.PART()
                    part.read(binaryReader, part_offset, part_index, self.hierarchy_dictionary)
                part_index += 1

    class PART(object):
        def __init__(self):
            super().__init__()

            self.indexes1 = []
            self.indexes2 = []

            self.submesh_offsets1 = []
            self.submesh_offsets2 = []

        def read(self, binaryReader, part_offset, part_index, hierarchy_dictionary):
            
            binaryReader.seek(part_offset, 0)
            binaryReader.seek(4, 1)
            count1 = binaryReader.readUShort() # count of submesh ?
            count2 = binaryReader.readUShort() # count of submesh ?
            binaryReader.seek(32, 1)  # zeros ?

            self.get_submesh_offsets(binaryReader, self.submesh_offsets1, self.indexes1, count1, part_offset)
            self.get_submesh_offsets(binaryReader, self.submesh_offsets2, self.indexes2, count2, part_offset)

            self.read_r7o(binaryReader, self.submesh_offsets1, self.indexes1, part_index, hierarchy_dictionary)
            self.read_r7o(binaryReader, self.submesh_offsets2, self.indexes2, part_index, hierarchy_dictionary)

        def get_submesh_offsets(self, binaryReader, list, indexes, count, part_offset):
            
            for i in range(count):
                indexes.append((binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort()))
                submesh_offset = binaryReader.readUInt()
                if submesh_offset != 0:
                    list.append(part_offset + submesh_offset) # offset to submesh data

        def read_r7o(self, binaryReader, submesh_offsets, indexes, part_index, hierarchy_dictionary):
            
            for i in range(len(submesh_offsets)):
                binaryReader.seek(submesh_offsets[i], 0)
                r7o = R7O()
                r7o.read(binaryReader)
                hierarchy_dictionary[car_hierarchy[part_index]].append((r7o, indexes[i]))

    class TRANSFORMATION:
        
        def __init__(self):
            self.mesh_index = 0
            self.parent_mesh_index = 0
            self.unknown = None
            self.unknown2 = None
            self.translation = None
            self.unknown3 = None
            self.unknown4 = None
            self.scale = None

        def read_transformation(self, binaryReader):

            self.mesh_index = binaryReader.readUShort()
            self.parent_mesh_index = binaryReader.readUShort()
            binaryReader.seek(4, 1)
            translation = Vector3.fromBytes(binaryReader.readBytes(12), ">")
            self.translation = Vector((translation[0], -translation[2], translation[1]))
            binaryReader.seek(52, 1)