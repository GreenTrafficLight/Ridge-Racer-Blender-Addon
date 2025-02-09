from ...Utilities.binaryReader import BinaryReader

from .ndvi import *

class RNC:
    def __init__(self):
        self.lods = {}
        
    class LOD:
        def __init__(self, offset):
            self.offset = offset
            self.ndviInformations = []
            self.ndviList = []

        class NDVI_Information:
            def __init__(self):
                self.unk1 = 0
                self.unk2 = 0
                self.offset = 0

            def read(self, br: BinaryReader):
                self.unk1 = br.readUInt()
                self.unk2 = br.readUInt()
                self.offset = br.readUInt()

        def read(self, br: BinaryReader):
            br.seek(self.offset)
            self.readNDVIInformations(br)
            self.readNDVIs(br)

        def readNDVIInformations(self, br: BinaryReader):
            count = br.readUInt()
            for i in range(count):
                ndviInformation = RNC.LOD.NDVI_Information()
                ndviInformation.read(br)
                self.ndviInformations.append(ndviInformation)

        def readNDVIs(self, br: BinaryReader):
            ndviInformation: RNC.LOD.NDVI_Information
            for ndviInformation in self.ndviInformations:
                ndvi = NDVI(ndviInformation.offset)
                ndvi.read(br)

                self.ndviList.append(ndvi)

    def read(self, br: BinaryReader):
        br.seek(4, 1)
        offset1 = br.readUInt()
        texturesOffset = br.readUInt()
        lodOffsets = []
        for i in range(4):
            lodOffsets.append(br.readUInt())

        for lodIndex, lodOffset in enumerate(lodOffsets):
            if lodOffset != 0:
                lod = RNC.LOD(lodOffset)
                lod.read(br)
                self.lods[f'LOD{lodIndex}'] = lod

        print("Read all LODs")
            