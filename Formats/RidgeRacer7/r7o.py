from mathutils import *

from ...Utilities.binaryReader import BinaryReader

from typing import List

class VertexBufferInformation :
    def __init__(self) -> None:
        self.vertexBufferOffset: int = 0
        self.vertexAttributes: int = 0
        self.vertexCount: int = 0

class FaceBufferInformation :
    def __init__(self) -> None:
        self.faceBufferOffset: int = 0
        self.faceCount: int = 0

class R7O:

    def __init__(self):
        self.vertexBuffers = []
        self.faceBuffers = []
        
    def read(self, br: BinaryReader):
        R7O_pos = br.tell()
        header = br.bytesToString(br.readBytes(4)).replace("\0", "")
        br.seek(4, 1)  # zeros ?

        offsets = []
        for i in range(4):
            # offset 1 = ?
            # offset 2 = ?
            # offest 3 = vertex buffers informations
            # offest 4 = face buffers informations
            offsets.append(R7O_pos + br.readUInt())

        br.seek(offsets[0], 0) # Position to matrices ?
        self.read_unknown(br)
        br.seek(offsets[2], 0) # Position to vertex buffers
        self.read_vertex_buffers_informations(br)
        br.seek(offsets[3], 0) # Position to face buffers
        self.read_face_buffers_informations(br)

    def read_unknown(self, br: BinaryReader):
        br.seek(4, 1)  # zeros ?
        matrixCount = br.readUInt() # matrix count ?

    def read_vertex_buffers_informations(self, br: BinaryReader):
        vertex_information_position = br.tell()
        br.seek(4, 1)  # zeros ?
        bufferCount = br.readUInt() # buffers count
        
        vertexBufferInformations = []
        for buffer in range(bufferCount): 
            vertexBufferInformation = VertexBufferInformation()
            vertexBufferInformation.vertexBufferOffset = vertex_information_position + br.readUInt() # offset to buffer
            vertexBufferInformation.vertexAttributes = br.readUInt() # vertex attributes
            vertexBufferInformation.vertexCount = br.readUInt()

            vertexBufferInformations.append(vertexBufferInformation)

        self.get_vertex_buffers(br, vertexBufferInformations)

    def get_vertex_buffers(self, br: BinaryReader, vertexBufferInformations):
        vertexBufferInformation : VertexBufferInformation
        for vertexBufferInformation in vertexBufferInformations:

            vertexBuffer = {
                "positions" : [],
                "colors" : [],
                "normals" : [],
                "texCoords" : []
            }

            #0x000D8022 = Stride 24

            #print(hex(vertex_buffer_information.vertexAttributes))
            if vertexBufferInformation.vertexAttributes == 0xD8022:
                print("test3")
                print(br.tell())

            br.seek(vertexBufferInformation.vertexBufferOffset)
            
            for i in range(vertexBufferInformation.vertexCount):

                # (0x00000002) 2 = Positions (Float)
                # (0x00000003) 3 = Positions (Half-Float)

                if vertexBufferInformation.vertexAttributes & 0xF == 3:
                    vertexBuffer["positions"].append([br.readHalfFloat(), br.readHalfFloat(), br.readHalfFloat()])
                elif vertexBufferInformation.vertexAttributes & 0xF == 2:
                    vertexBuffer["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])

                # (0x00000020) 2 = Colors

                if ((vertexBufferInformation.vertexAttributes >> 4) & 0xF) == 2:
                    vertexBuffer["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                # (0x00000400) 4 = Normals (Float)
                # (0x00000600) 6 = Normals (Half-Float)
                
                if ((vertexBufferInformation.vertexAttributes >> 8) & 0xF) == 6:
                    vertexBuffer["normals"].append(Vector((br.readHalfFloat(), br.readHalfFloat(), br.readHalfFloat())).normalized())
                elif ((vertexBufferInformation.vertexAttributes >> 8) & 0xF) == 4:
                    vertexBuffer["normals"].append(Vector((br.readFloat(), br.readFloat(), br.readFloat())).normalized())
            
                # (0x00010000) 10 = texCoords (Float)
                # (0x00012000) 12 = texCoords (Float)
                # (0x00018000) 18 = texCoords (Half-Float)
                # (0x0001B000) 1B = texCoords (Half-Float)
                
                if vertexBufferInformation.vertexAttributes >> 12 == 0x1B:
                    br.seek(6, 1)
                    vertexBuffer["texCoords"].append([br.readHalfFloat(), br.readHalfFloat()])
                
                elif vertexBufferInformation.vertexAttributes >> 12 == 0x18:
                    vertexBuffer["texCoords"].append([br.readHalfFloat(), br.readHalfFloat()])

                elif vertexBufferInformation.vertexAttributes >> 12 == 0xD8: # ???
                    br.seek(8, 1)
                
                elif vertexBufferInformation.vertexAttributes >> 12 == 0x12:
                    br.seek(12, 1)
                    vertexBuffer["texCoords"].append([br.readFloat(), br.readFloat()])
                
                elif vertexBufferInformation.vertexAttributes >> 12 == 0x10:
                    vertexBuffer["texCoords"].append([br.readFloat(), br.readFloat()])

            self.vertexBuffers.append(vertexBuffer)

    def read_face_buffers_informations(self, br: BinaryReader):
        face_information_position = br.tell()
        br.seek(4, 1)  # zeros ?
        bufferCount = br.readUInt() # buffers count
        
        faceBufferInformations = []
        for buffer in range(bufferCount):
            faceBufferInformation = FaceBufferInformation()
            faceBufferInformation.faceBufferOffset = face_information_position + br.readUInt() # offset to buffer
            faceBufferInformation.faceCount = br.readUInt()

            faceBufferInformations.append(faceBufferInformation)

        self.get_face_buffers(br, faceBufferInformations)

    def get_face_buffers(self, binaryReader: BinaryReader, faceBufferInformations: List[FaceBufferInformation]):
        faceBufferInformation: FaceBufferInformation
        for faceBufferInformation in faceBufferInformations:
            faceBuffer = []
            for i in range(faceBufferInformation.faceCount):
                faceBuffer.append(binaryReader.readUShort())

            self.faceBuffers.append(faceBuffer)