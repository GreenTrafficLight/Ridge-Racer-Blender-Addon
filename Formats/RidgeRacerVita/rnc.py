from ...Utilities.binaryReader import BinaryReader

from .ndvi import *

class RNC:
    def __init__(self):
        pass

    def read(self, br: BinaryReader):
        br.seek(4, 1)
        offset1 = br.readUInt()
        texturesOffset = br.readUInt()
        
        modelOffset = br.readUInt()
        
        model = RNC.Model()
        br.seek(modelOffset)
        model.read(br)

    class Model:
        def __init__(self):
            self.meshInformations = []
            self.meshes = []

        class Mesh:
            def __init__(self):
                pass

            class Information:
                def __init__(self):
                    self.unk1 = 0
                    self.unk2 = 0
                    self.offset = 0

                def read(self, br: BinaryReader):
                    self.unk1 = br.readUInt()
                    self.unk2 = br.readUInt()
                    self.offset = br.readUInt()

            def read(self, br: BinaryReader):
                ndvi = NDVI()
                ndvi.read(br)

        def read(self, br: BinaryReader):
            count = br.readUInt()
            for i in range(count):
                meshInformation = RNC.Model.Mesh.Information()
                meshInformation.read(br)
                self.meshInformations.append(meshInformation)

            self.readMeshes(br)

        def readMeshes(self, br: BinaryReader):
            information: RNC.Model.Mesh.Information
            for information in self.meshInformations:
                mesh = RNC.Model.Mesh()

                br.seek(information.offset)
                mesh.read(br)
            