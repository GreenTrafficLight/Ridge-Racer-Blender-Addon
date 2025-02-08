from ....Utilities.binaryReader import *

from typing import List

class ObjectInformationContainer:
    def __init__(self):
        self.offset = 0
        self.count = 0

    def read(self, br: BinaryReader):
        self.offset = br.readUInt()
        self.count = br.readUInt()

    def isNull(self):
        return self.offset == 0 and self.count == 0

class ObjectTransformation:

    def __init__(self):
        self.unknown_vector4_1 = None
        self.unknown_vector4_2 = None
        self.transformation_matrix = None

    def read(self, br: BinaryReader):
        self.unknown_vector4_1 = br.readVector4f()
        self.unknown_vector4_2 = br.readVector4f()
        self.transformation_matrix = br.readMatrix4x4f()

class ObjectInformation:

    def __init__(self):
        self.type = ""
        self.containers: List[ObjectInformationContainer] = []
        self.transformations: List[ObjectTransformation] = []

    def read(self, br: BinaryReader):
        self.type = br.bytesToString(br.readBytes(32)).replace("\0", "")

        for i in range(4):
            # 1 = offset that contains objet transformations
            # 2 = ?
            # 3 = ?
            # 4 = ?
            
            map_information_container = ObjectInformationContainer()
            map_information_container.read(br)

            self.containers.append(map_information_container)

        if not self.containers[0].isNull():
            br.seek(self.containers[0].offset, 0)
            self.readObjetTransformations(br)

    def readObjetTransformations(self, br: BinaryReader):
        unkOffset1 = br.readUInt()
        br.seek(unkOffset1, 0)
        br.readUInt()
        objectTransformationsOffset = br.readUInt()
        objectTransformationsCount = br.readUInt()
        br.seek(objectTransformationsOffset, 0)
        for objectTransformation in range(objectTransformationsCount):
            transformation = ObjectTransformation()
            transformation.read(br)
            self.transformations.append(transformation)
