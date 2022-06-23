from ...Utilities import *
from .r6o import *

from mathutils import *

class R6C:

    def __init__(self):

        self.structures = {
            "LOD0" : None,
            "LOD1" : None,
            "LOD2" : None,
            "LOD3" : None,
            "SHADOW" : None
        }

        self.transformations = {}

        self.offsetList = []

    def read(self, binaryReader):

        binaryReader.seek(8, 1) # ???

        self.get_offsets(binaryReader, 6)

        binaryReader.seek(12, 1) # ???
        binaryReader.seek(28, 1) # ???
        binaryReader.seek(4, 1) # zeros ?

        self.get_offsets(binaryReader, 5)

        # offset 1 to 5 : lods information offset
        # offset 9 : transformation information offset

        self.read_lods(binaryReader)

        self.read_shadow(binaryReader)

        self.read_transformations(binaryReader)

    def get_offsets(self, binaryReader, count):
        for i in range(count):
            self.offsetList.append(binaryReader.readUInt())

    def read_transformations(self, binaryReader):
        if self.offsetList[9] != 0:
            binaryReader.seek(self.offsetList[9], 0)
            transformation_count = binaryReader.readUInt()
            for i in range(transformation_count):
                mesh_index = binaryReader.readUShort()
                transformation = R6C.TRANSFORMATION()
                transformation.read_transformation(binaryReader)
                self.transformations[mesh_index] = transformation

    def read_lods(self, binaryReader):
        lod_number = 0
        for i in range(1,5):
            indexes = []
            if self.offsetList[i] != 0:
                binaryReader.seek(self.offsetList[i], 0)
                count1 = binaryReader.readUShort() # submesh count
                count2 = binaryReader.readUShort() # submesh count
                r6o_offset = binaryReader.readUInt()

                for j in range(count1):
                    indexes.append((binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort()))

                for j in range(count2):
                    indexes.append((binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort()))
     
                binaryReader.seek(r6o_offset, 0)
                
                r6o = R6O(indexes)
                r6o.read(binaryReader, indexes)
                self.structures["LOD" + str(lod_number)] = (r6o, indexes)
                
            lod_number += 1
        
    def read_shadow(self, binaryReader):
        indexes = []
        binaryReader.seek(self.offsetList[5], 0)
        count1 = binaryReader.readUShort() # submesh count
        count2 = binaryReader.readUShort() # submesh count
        r6o_offset = binaryReader.readUInt()

        for j in range(count1):
            indexes.append((binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort()))

        for j in range(count2):
            indexes.append((binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort(), binaryReader.readUShort()))

        binaryReader.seek(r6o_offset, 0)
        
        r6o = R6O(indexes)
        r6o.read(binaryReader, indexes)
        self.structures["SHADOW"]  = (r6o, indexes)

    class TRANSFORMATION:
        
        def __init__(self):
            self.parent_mesh_index = 0
            self.unknown2 = None
            self.translation = None
            self.rotation = None
            self.unknown4 = None
            self.scale = None

        def read_transformation(self, binaryReader):

            self.parent_mesh_index = binaryReader.readUShort()
            binaryReader.seek(4, 1)
            translation = Vector3.fromBytes(binaryReader.readBytes(12), ">")
            self.translation = Vector((translation[0], -translation[2], translation[1]))
            rotation = Vector3.fromBytes(binaryReader.readBytes(12), ">")
            self.rotation = Vector((rotation[0], -rotation[2], rotation[1]))
            binaryReader.seek(40, 1)
