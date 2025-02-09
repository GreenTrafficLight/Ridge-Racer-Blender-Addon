from ...Utilities.binaryReader import BinaryReader

class NDVI:
    def __init__(self, offset):
        self.offset = offset

        self.size = 0
        self.unk1 = 0
        self.count1 = 0

        self.meshInformations = []
        self.meshes = []

    class Header:
        def __init__(self, offset):
            self.offset = offset

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
            br.readVector4f()

    @property
    def faceBufferOffset(self):
        return 48 + self.size1
    
    @property
    def vertexBufferOffset(self):
        return self.faceBufferOffset + self.faceBufferSize
    
    @property
    def namesOffset(self):
        return self.vertexBufferOffset + self.vertexBufferSize
    
    class Mesh:
        def __init__(self):
            self.name: str = ""
            self.subMeshes = []

        class Information:
            def __init__(self, ndviOffset: int):
                self.ndviOffset = ndviOffset
                self.nameOffset = 0
                self.subMeshCount = 0
                self.bufferInformationsOffset = 0
                
                self.subMeshInformations = []

            def read(self, br: BinaryReader):
                br.readVector4f()
                br.readVector4f()
                self.nameOffset = br.readUInt()
                br.seek(4, 1)
                br.readShort()
                self.subMeshCount = br.readUShort()
                self.bufferInformationsOffset = br.readUInt()
                
                savePos = br.tell()

                self.readSubMeshInformations(br)

                br.seek(savePos)

            def readSubMeshInformations(self, br: BinaryReader):
                br.seek(self.ndviOffset + self.bufferInformationsOffset, 0)
                for i in range(self.subMeshCount):
                    subMeshBufferInformation = NDVI.SubMesh.Information()
                    subMeshBufferInformation.read(br)
                    self.subMeshInformations.append(subMeshBufferInformation)
    
    class SubMesh:
        def __init__(self):
            self.faceBuffer = []
            self.vertexBuffer = {
                "positions" : [],
                "colors" : [],
                "normals" : [],
                "texCoords" : []
            }

        class Information:
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
                self.faceCount = br.readUInt()
                br.seek(12, 1)

        def readFaceBuffer(self, br: BinaryReader, subMeshInformation: Information):
            for i in range(subMeshInformation.faceCount):
                self.faceBuffer.append(br.readUShort())

        def readVertexBuffer(self, br: BinaryReader, subMeshInformation: Information):
            for i in range(subMeshInformation.vertexCount):
                self.vertexBuffer["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                br.seek(8, 1)
                self.vertexBuffer["texCoords"].append([br.readUShort() / 65535, br.readUShort() / 65535])
                if subMeshInformation.stride == 0x1206:
                    self.vertexBuffer["colors"].append([br.readByte() / 127, br.readByte() / 127, br.readByte() / 127, br.readByte() / 127])

    def read(self, br: BinaryReader):
        br.seek(self.offset)
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
        br.readVector4f()

        for i in range(self.count1):
            meshInformation = NDVI.Mesh.Information(self.ndviOffset)
            meshInformation.read(br)
            self.meshInformations.append(meshInformation)

        self.readMeshes(br)

        print("Read all mesh of NDVI")
            
    def readMeshes(self, br: BinaryReader):
        meshInformation : NDVI.Mesh.Information
        for meshInformation in self.meshInformations:
            mesh = NDVI.Mesh()

            subMeshInformation : NDVI.SubMesh.Information
            for subMeshInformation in meshInformation.subMeshInformations:
                subMesh = NDVI.SubMesh()

                br.seek(self.ndviOffset + self.faceBufferOffset + subMeshInformation.faceOffset)
                subMesh.readFaceBuffer(br, subMeshInformation)
                br.seek(self.ndviOffset + self.vertexBufferOffset + subMeshInformation.vertexOffset)
                subMesh.readVertexBuffer(br, subMeshInformation)

                mesh.subMeshes.append(subMesh)
            
            br.seek(self.ndviOffset + self.namesOffset + meshInformation.nameOffset)
            mesh.name = br.readString()

            self.meshes.append(mesh)

            
