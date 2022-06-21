from Utilities.vector import Vector3
from .r6o import *

class R6C:

    def __init__(self, br):
        self.br = br

        self.structures = {
            "LOD0" : None,
            "LOD1" : None,
            "LOD2" : None,
            "LOD3" : None,
            "SHADOW" : None
        }

        self.br.seek(8, 1) # ???

        self.offsetList = []

        self.get_offsets(6)

        self.br.seek(12, 1) # ???
        self.br.seek(28, 1) # ???
        self.br.seek(4, 1) # zeros ?

        self.get_offsets(5)

        # offset 1 to 5 : lods information offset
        # offset 9 : transformation information offset

        self.read_lods()

        self.read_shadow()

    def get_offsets(self, count):
        for i in range(count):
            self.offsetList.append(self.br.readUInt())

    def read_transformations(self):
        self.seek(self.offsetList[9], 0)
        transformation_count = self.br.readUInt()
        for i in range(transformation_count):
            self.br.readBytes(72)

    def read_lods(self):
        lod_number = 0
        for i in range(1,5):
            indexes = []
            if self.offsetList[i] != 0:
                self.br.seek(self.offsetList[i], 0)
                count1 = self.br.readUShort() # submesh count
                count2 = self.br.readUShort() # submesh count
                r6o_offset = self.br.readUInt()

                for j in range(count1):
                    indexes.append((self.br.readUShort(), self.br.readUShort(), self.br.readUShort(), self.br.readUShort()))

                for j in range(count2):
                    indexes.append((self.br.readUShort(), self.br.readUShort(), self.br.readUShort(), self.br.readUShort()))
     
                self.br.seek(r6o_offset, 0)
                
                r6o = R6O(self.br)
                self.structures["LOD" + str(lod_number)] = (r6o, indexes)
                
                lod_number += 1
        
    def read_shadow(self):
        indexes = []
        self.br.seek(self.offsetList[5], 0)
        count1 = self.br.readUShort() # submesh count
        count2 = self.br.readUShort() # submesh count
        r6o_offset = self.br.readUInt()

        for j in range(count1):
            indexes.append((self.br.readUShort(), self.br.readUShort(), self.br.readUShort(), self.br.readUShort()))

        for j in range(count2):
            indexes.append((self.br.readUShort(), self.br.readUShort(), self.br.readUShort(), self.br.readUShort()))

        self.br.seek(r6o_offset, 0)
        
        r6o = R6O(self.br)
        self.structures["SHADOW"]  = (r6o, indexes)

class R6C_TRANSFORMATION:
    
    def __init__(self, binaryReader):
        self.mesh_index = 0
        self.unknown = None
        self.unknown2 = None
        self.translation = None
        self.unknown3 = None
        self.unknown4 = None
        self.scale = None

    def read_transformation(self, binaryReader):

        self.mesh_index = binaryReader.readUShort()
        binaryReader.seek(6, 1)
        self.translation = Vector3.fromBytes(binaryReader.readBytes(12))
