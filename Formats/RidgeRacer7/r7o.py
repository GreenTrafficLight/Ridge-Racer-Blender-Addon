from mathutils import *

class Vertex_Buffer_Information :
    def __init__(self):
        self.vertex_buffer_offset = 0
        self.vertex_attributes = 0
        self.vertex_number = 0

class Face_Buffer_Information :
    def __init__(self):
        self.face_buffer_offset = 0
        self.face_number = 0

class R7O:

    def __init__(self):

        self.vertex_buffers = []
        self.face_buffers = []
        
    def read(self, binaryReader):

        offsets = []

        R7O_pos = binaryReader.tell()
        header = binaryReader.bytesToString(binaryReader.readBytes(4)).replace("\0", "")
        binaryReader.seek(4, 1)  # zeros ?

        for i in range(4):
            # offset 1 = ?
            # offset 2 = ?
            # offest 3 = vertex buffers informations
            # offest 4 = face buffers informations
            offsets.append(R7O_pos + binaryReader.readUInt())

        binaryReader.seek(offsets[0], 0) # Position to matrices ?
        self.read_unknown(binaryReader)
        binaryReader.seek(offsets[2], 0) # Position to vertex buffers
        self.read_vertex_buffers_informations(binaryReader)
        binaryReader.seek(offsets[3], 0) # Position to face buffers
        self.read_face_buffers_informations(binaryReader)

    def read_unknown(self, binaryReader):
        
        binaryReader.seek(4, 1)  # zeros ?
        matrixCount = binaryReader.readUInt() # matrix count ?

    def read_vertex_buffers_informations(self, binaryReader):
        
        vertex_buffer_informations = []

        vertex_information_position = binaryReader.tell()

        binaryReader.seek(4, 1)  # zeros ?
        buffer_count = binaryReader.readUInt() # buffers count
        
        for buffer in range(buffer_count): 

            vertex_buffer_information = Vertex_Buffer_Information()

            vertex_buffer_information.vertex_buffer_offset = vertex_information_position + binaryReader.readUInt() # offset to buffer
            vertex_buffer_information.vertex_attributes = binaryReader.readUInt() # vertex attributes
            vertex_buffer_information.vertex_number = binaryReader.readUInt()

            vertex_buffer_informations.append(vertex_buffer_information)

        self.get_vertex_buffers(binaryReader, vertex_buffer_informations)

    def get_vertex_buffers(self, binaryReader, vertex_buffer_informations):

        for vertex_buffer_information in vertex_buffer_informations:

            vertex_buffer = {
            "positions" : [],
            "colors" : [],
            "normals" : [],
            "texCoords" : []
            }

            #0x000D8022 = Stride 24

            #print(hex(vertex_buffer_information.vertex_attributes))
            if vertex_buffer_information.vertex_attributes == 0xD8022:
                print("test3")
                print(binaryReader.tell())

            binaryReader.seek(vertex_buffer_information.vertex_buffer_offset)
            
            for i in range(vertex_buffer_information.vertex_number):

                # (0x00000002) 2 = Positions (Float)
                # (0x00000003) 3 = Positions (Half-Float)

                if vertex_buffer_information.vertex_attributes & 0xF == 3:
                    vertex_buffer["positions"].append([binaryReader.readHalfFloat(), binaryReader.readHalfFloat(), binaryReader.readHalfFloat()])
                elif vertex_buffer_information.vertex_attributes & 0xF == 2:
                    vertex_buffer["positions"].append([binaryReader.readFloat(), binaryReader.readFloat(), binaryReader.readFloat()])

                # (0x00000020) 2 = Colors

                if ((vertex_buffer_information.vertex_attributes >> 4) & 0xF) == 2:
                    vertex_buffer["colors"].append([binaryReader.readUByte() / 255, binaryReader.readUByte() / 255, binaryReader.readUByte() / 255, binaryReader.readUByte() / 255])

                # (0x00000400) 4 = Normals (Float)
                # (0x00000600) 6 = Normals (Half-Float)
                
                if ((vertex_buffer_information.vertex_attributes >> 8) & 0xF) == 6:
                    vertex_buffer["normals"].append(Vector((binaryReader.readHalfFloat(), binaryReader.readHalfFloat(), binaryReader.readHalfFloat())).normalized())
                elif ((vertex_buffer_information.vertex_attributes >> 8) & 0xF) == 4:
                    vertex_buffer["normals"].append(Vector((binaryReader.readFloat(), binaryReader.readFloat(), binaryReader.readFloat())).normalized())
            
                # (0x00010000) 10 = texCoords (Float)
                # (0x00012000) 12 = texCoords (Float)
                # (0x00018000) 18 = texCoords (Half-Float)
                # (0x0001B000) 1B = texCoords (Half-Float)
                
                if vertex_buffer_information.vertex_attributes >> 12 == 0x1B:
                    binaryReader.seek(6, 1)
                    vertex_buffer["texCoords"].append([binaryReader.readHalfFloat(), binaryReader.readHalfFloat()])
                
                elif vertex_buffer_information.vertex_attributes >> 12 == 0x18:
                    vertex_buffer["texCoords"].append([binaryReader.readHalfFloat(), binaryReader.readHalfFloat()])

                elif vertex_buffer_information.vertex_attributes >> 12 == 0xD8: # ???
                    binaryReader.seek(8, 1)
                
                elif vertex_buffer_information.vertex_attributes >> 12 == 0x12:
                    binaryReader.seek(12, 1)
                    vertex_buffer["texCoords"].append([binaryReader.readFloat(), binaryReader.readFloat()])
                
                elif vertex_buffer_information.vertex_attributes >> 12 == 0x10:
                    vertex_buffer["texCoords"].append([binaryReader.readFloat(), binaryReader.readFloat()])

            self.vertex_buffers.append(vertex_buffer)

    def read_face_buffers_informations(self, binaryReader):
        face_buffer_informations = []

        face_information_position = binaryReader.tell()

        binaryReader.seek(4, 1)  # zeros ?
        bufferCount = binaryReader.readUInt() # buffers count
        
        for buffer in range(bufferCount):
            
            face_buffer_information = Face_Buffer_Information()

            face_buffer_information.face_buffer_offset = face_information_position + binaryReader.readUInt() # offset to buffer
            face_buffer_information.face_number = binaryReader.readUInt()

            face_buffer_informations.append(face_buffer_information)

        self.get_face_buffers(binaryReader, face_buffer_informations)

    def get_face_buffers(self, binaryReader, face_buffer_informations):

        for face_buffer_information in face_buffer_informations:

            face_buffer = []
        
            for i in range(face_buffer_information.face_number):
                
                face_buffer.append(binaryReader.readUShort())

            self.face_buffers.append(face_buffer)