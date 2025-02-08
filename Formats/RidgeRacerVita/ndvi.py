from ...Utilities.binaryReader import BinaryReader

class NDVI:
    def __init__(self):
        self.size = 0
        self.unk1 = 0
        self.count1 = 0

        self.subMeshInformations = []
        self.subMeshes = []

    @property
    def faceBufferOffset(self):
        return self.size1
    
    @property
    def vertexBufferOffset(self):
        return self.faceBufferOffset + self.faceBufferSize
    
    class SubMesh:
        def __init__(self):
            self.faceBuffer = []
            self.vertexBuffer = []
    
        class Information:
            def __init__(self, ndviOffset: int):
                self.ndviOffset = ndviOffset
                self.subMeshCount = 0
                self.bufferInformationsOffset = 0
                
                self.bufferInformations = []

            def read(self, br: BinaryReader, i: int):
                br.readVector4f()
                br.readVector4f()
                if i < 1:
                    br.readVector4f()
                br.seek(8, 1)
                br.readShort()
                self.subMeshCount = br.readUShort()
                self.bufferInformationsOffset = br.readUInt()
                
                savePos = br.tell()

                self.readBufferInformations(br)

                br.seek(savePos)

            def readBufferInformations(self, br: BinaryReader):
                br.seek(self.ndviOffset + self.bufferInformationsOffset, 0)
                for i in range(self.subMeshCount):
                    subMeshBufferInformation = NDVI.SubMesh.BufferInformation()
                    subMeshBufferInformation.read(br)
                    self.bufferInformations.append(subMeshBufferInformation)
    
        class BufferInformation:
            def __init__(self):
                self.faceOffset = 0
                self.vertexOffset = 0
                self.vertexCount = 0
                self.stride = 0
                self.offset1 = 0
                self.unk1 = 0

            def read(self, br: BinaryReader):
                self.faceOffset = br.readUInt()
                self.vertexOffset = br.readUInt()
                br.seek(4, 1)
                self.vertexCount = br.readUShort()
                self.stride = br.readUShort()
                self.offset1 = br.readUInt()
                self.unk1 = br.readUInt()
                br.seek(8, 1)
                self.faceCount = br.readUShort()
                br.seek(12, 1)

        def readFaceBuffer(self, br: BinaryReader, bufferInformation: BufferInformation):
            for i in range(bufferInformation.faceCount):
                self.faceBuffer.append(br.readUShort())

        def readVertexBuffer(self, br: BinaryReader, bufferInformation: BufferInformation):
            pass

    def read(self, br: BinaryReader):
        self.ndviOffset = br.tell()
        br.readBytesToString(4).replace("\0", "")
        self.size = br.readUInt()
        self.unk1 = br.readUShort()
        self.count1 = br.readUShort()
        br.seek(4, 1)
        self.size1 = br.readUInt()
        self.faceBufferSize = br.readUInt()
        self.vertexBufferSize = br.readUInt()
        br.seek(4, 1)

        for i in range(self.count1):
            subMeshInformation = NDVI.SubMesh.Information(self.ndviOffset)
            subMeshInformation.read(br, i)
            self.subMeshInformations.append(subMeshInformation)

        self.readSubMeshs(br)
            
    def readSubMeshs(self, br: BinaryReader):
        information : NDVI.SubMesh.Information
        for information in self.subMeshInformations:
            bufferInformation : NDVI.SubMesh.BufferInformation
            for bufferInformation in information.bufferInformations:
                subMesh = NDVI.SubMesh()

                br.seek(self.ndviOffset + self.faceBufferOffset + bufferInformation.faceOffset)
                subMesh.readFaceBuffer(br, bufferInformation)
                br.seek(self.ndviOffset + self.vertexBufferOffset + bufferInformation.vertexOffset)
                subMesh.readVertexBuffer(br, bufferInformation)
            
                self.subMeshes.append(subMesh)