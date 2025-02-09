from ...Utilities.binaryReader import BinaryReader

from .ndvi import *

class RNC:
    def __init__(self):
        
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
        br.seek(4, 1)
        offset1 = br.readUInt()
        texturesOffset = br.readUInt()
        ndvisOffset = br.readUInt()
        
        br.seek(ndvisOffset)
        count = br.readUInt()
        for i in range(count):
            ndviInformation = RNC.NDVI_Information()
            ndviInformation.read(br)
            self.ndviInformations.append(ndviInformation)
        
        self.readNDVIs(br)

    def readNDVIs(self, br: BinaryReader):
        ndviInformation: RNC.NDVI_Information
        for ndviInformation in self.ndviInformations:
            ndvi = NDVI()

            br.seek(ndviInformation.offset)
            ndvi.read(br)

            self.ndviList.append(ndvi)

        print("Read all NDVI")
            