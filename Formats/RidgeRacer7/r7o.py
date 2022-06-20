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

    def __init__(self, binaryReader):
        self.br = binaryReader

        self.vertex_buffers = []
        self.face_buffers = []
        
        offsets = []

        R7O_pos = self.br.tell()
        header = binaryReader.bytesToString(binaryReader.readBytes(4)).replace("\0", "")
        self.br.seek(4, 1)  # zeros ?

        for i in range(4):
            # offset 1 = ?
            # offset 2 = ?
            # offest 3 = vertex buffers informations
            # offest 4 = face buffers informations
            offsets.append(R7O_pos + self.br.readUInt())

        self.br.seek(offsets[0], 0) # Position to matrices ?
        self.read_unknown()
        self.br.seek(offsets[2], 0) # Position to vertex buffers
        self.read_vertex_buffers_informations()
        self.br.seek(offsets[3], 0) # Position to face buffers
        self.read_face_buffers_informations()

    def read_unknown(self):
        self.br.seek(4, 1)  # zeros ?
        matrixCount = self.br.readUInt() # matrix count ?

    def read_vertex_buffers_informations(self):
        vertex_buffer_informations = []

        vertex_information_position = self.br.tell()

        self.br.seek(4, 1)  # zeros ?
        buffer_count = self.br.readUInt() # buffers count
        
        for buffer in range(buffer_count): 

            vertex_buffer_information = Vertex_Buffer_Information()

            vertex_buffer_information.vertex_buffer_offset = vertex_information_position + self.br.readUInt() # offset to buffer
            vertex_buffer_information.vertex_attributes = self.br.readUInt() # vertex attributes
            vertex_buffer_information.vertex_number = self.br.readUInt()

            vertex_buffer_informations.append(vertex_buffer_information)

        self.get_vertex_buffers(vertex_buffer_informations)

    def get_vertex_buffers(self, vertex_buffer_informations):

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
                print(self.br.tell())

            self.br.seek(vertex_buffer_information.vertex_buffer_offset)
            
            for i in range(vertex_buffer_information.vertex_number):

                # (0x00000002) 2 = Positions (Float)
                # (0x00000003) 3 = Positions (Half-Float)

                if vertex_buffer_information.vertex_attributes & 0xF == 3:
                    vertex_buffer["positions"].append([self.br.readHalfFloat(), self.br.readHalfFloat(), self.br.readHalfFloat()])
                elif vertex_buffer_information.vertex_attributes & 0xF == 2:
                    vertex_buffer["positions"].append([self.br.readFloat(), self.br.readFloat(), self.br.readFloat()])

                # (0x00000020) 2 = Colors

                if ((vertex_buffer_information.vertex_attributes >> 4) & 0xF) == 2:
                    vertex_buffer["colors"].append([self.br.readUByte() / 255, self.br.readUByte() / 255, self.br.readUByte() / 255, self.br.readUByte() / 255])

                # (0x00000400) 4 = Normals (Float)
                # (0x00000600) 6 = Normals (Half-Float)
                
                if ((vertex_buffer_information.vertex_attributes >> 8) & 0xF) == 6:
                    vertex_buffer["normals"].append(Vector((self.br.readHalfFloat(), self.br.readHalfFloat(), self.br.readHalfFloat())).normalized())
                elif ((vertex_buffer_information.vertex_attributes >> 8) & 0xF) == 4:
                    vertex_buffer["normals"].append(Vector((self.br.readFloat(), self.br.readFloat(), self.br.readFloat())).normalized())
            
                # (0x00010000) 10 = texCoords (Float)
                # (0x00012000) 12 = texCoords (Float)
                # (0x00018000) 18 = texCoords (Half-Float)
                # (0x0001B000) 1B = texCoords (Half-Float)
                
                if vertex_buffer_information.vertex_attributes >> 12 == 0x1B:
                    self.br.seek(6, 1)
                    vertex_buffer["texCoords"].append([self.br.readHalfFloat(), self.br.readHalfFloat()])
                
                elif vertex_buffer_information.vertex_attributes >> 12 == 0x18:
                    vertex_buffer["texCoords"].append([self.br.readHalfFloat(), self.br.readHalfFloat()])

                elif vertex_buffer_information.vertex_attributes >> 12 == 0xD8: # ???
                    self.br.seek(8, 1)
                
                elif vertex_buffer_information.vertex_attributes >> 12 == 0x12:
                    self.br.seek(12, 1)
                    vertex_buffer["texCoords"].append([self.br.readFloat(), self.br.readFloat()])
                
                elif vertex_buffer_information.vertex_attributes >> 12 == 0x10:
                    vertex_buffer["texCoords"].append([self.br.readFloat(), self.br.readFloat()])

            self.vertex_buffers.append(vertex_buffer)

    def read_face_buffers_informations(self):
        face_buffer_informations = []

        face_information_position = self.br.tell()

        self.br.seek(4, 1)  # zeros ?
        bufferCount = self.br.readUInt() # buffers count
        
        for buffer in range(bufferCount):
            
            face_buffer_information = Face_Buffer_Information()

            face_buffer_information.face_buffer_offset = face_information_position + self.br.readUInt() # offset to buffer
            face_buffer_information.face_number = self.br.readUInt()

            face_buffer_informations.append(face_buffer_information)

        self.get_face_buffers(face_buffer_informations)

    def get_face_buffers(self, face_buffer_informations):

        for face_buffer_information in face_buffer_informations:

            face_buffer = []
        
            for i in range(face_buffer_information.face_number):
                
                face_buffer.append(self.br.readUShort())

            self.face_buffers.append(face_buffer)