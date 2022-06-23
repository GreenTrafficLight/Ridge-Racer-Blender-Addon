from mathutils import *

from ...Utilities import *

import binascii

class R6O:

    def __init__(self, indexes):
        self.vertex_buffers = []
        self.face_buffers = []
        self.materials = []

    def read(self, binaryReader, indexes):

        offsets = []

        R6O_pos = binaryReader.tell()
        header = binaryReader.bytesToString(binaryReader.readBytes(4)).replace("\0", "")
        binaryReader.seek(4, 1)  # zeros ?

        for i in range(4):
            # offset 1 = ?
            # offset 2 = material informations
            # offest 3 = vertex buffers informations
            # offest 4 = face buffers informations
            offsets.append(R6O_pos + binaryReader.readUInt())

        binaryReader.seek(offsets[0], 0) # Position to matrices ?
        self.read_unknown(binaryReader)
        binaryReader.seek(offsets[1], 0) # Position to material informations
        self.read_material_informations(binaryReader)
        
        binaryReader.seek(offsets[2], 0) # Position to vertex buffers
        self.read_vertex_buffers_informations(binaryReader)
        binaryReader.seek(offsets[3], 0) # Position to face buffers
        self.read_face_buffers_informations(binaryReader)        

    def read_unknown(self, binaryReader):
        binaryReader.seek(4, 1)  # zeros ?
        matrixCount = binaryReader.readUInt() # matrix count ?

    def read_material_informations(self, binaryReader):
        material_information_offsets = []

        material_information_position = binaryReader.tell()

        binaryReader.seek(4, 1)  # zeros ?
        count = binaryReader.readUInt() # material information count

        for i in range(count):
            material_information_offsets.append(material_information_position + binaryReader.readUInt())

        self.get_materials(binaryReader, material_information_offsets)

    def get_materials(self, binaryReader, material_information_offsets):

        for material_information_offset in material_information_offsets:

            binaryReader.seek(material_information_offset)

            material_information = R6O.Material_Information()
            material_information.read(binaryReader)

            self.materials.append(material_information)


    def read_vertex_buffers_informations(self, binaryReader):
        vertex_buffer_informations = []

        vertex_information_position = binaryReader.tell()

        binaryReader.seek(4, 1)  # zeros ?
        buffer_count = binaryReader.readUInt() # buffers count
        
        for buffer in range(buffer_count):

            vertex_buffer_information = R6O.Vertex_Buffer_Information()

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

            # 0x00201201 = Stride 40
            # 0x00200001 = Stride 16
            # 0x00200009 = ???
            print("test : " + hex(vertex_buffer_information.vertex_attributes))
            print(binaryReader.tell())
            print(vertex_buffer_information.vertex_number)
            
            binaryReader.seek(vertex_buffer_information.vertex_buffer_offset)
            for i in range(vertex_buffer_information.vertex_number):

                # (0x00000001) 1 = Positions (Float)
                if vertex_buffer_information.vertex_attributes & 0xF == 1:
                    vertex_buffer["positions"].append([binaryReader.readFloat(), binaryReader.readFloat(), binaryReader.readFloat()])

                # (0x00000200) 2 = Normals (Float)
                if ((vertex_buffer_information.vertex_attributes >> 8) & 0xF) == 2:
                    vertex_buffer["normals"].append(Vector((binaryReader.readFloat(), binaryReader.readFloat(), binaryReader.readFloat())).normalized())

                # (0x00001000) 1 = ???
                if ((vertex_buffer_information.vertex_attributes >> 12) & 0xF) == 1:
                    binaryReader.seek(12, 1)

                # (0x00200000) 2 = texCoords (Half-Float)
                if ((vertex_buffer_information.vertex_attributes >> 20) & 0xF) == 2:
                    vertex_buffer["texCoords"].append([binaryReader.readHalfFloat(), binaryReader.readHalfFloat()])

            self.vertex_buffers.append(vertex_buffer)

    def read_face_buffers_informations(self, binaryReader):
        face_buffer_informations = []

        face_information_position = binaryReader.tell()

        binaryReader.seek(4, 1)  # zeros ?
        buffer_count = binaryReader.readUInt() # buffers count
        
        for buffer in range(buffer_count):
            
            face_buffer_information = R6O.Face_Buffer_Information()

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

    class Material_Information:
        def __init__(self) -> None:
            self.name = 0
            
            self.textures = []

        def read(self, binaryReader):

            binaryReader.seek(4, 1) # zeros ?
            self.name = str(binascii.hexlify(binaryReader.readBytes(4)), 'ascii') # ?
            binaryReader.readUInt()
            float_count = binaryReader.readUInt()
            unknonwn_count = binaryReader.readUInt()
            texture_count = binaryReader.readUInt()
            
            for i in range(texture_count):
                binaryReader.readUInt() # texture index ?

            for i in range(float_count):
                binaryReader.readFloat()

            for i in range(unknonwn_count):
                binaryReader.readUInt()
                binaryReader.readUInt()

            self.read_texture_informations(binaryReader, texture_count)

        def read_texture_informations(self, binaryReader, texture_count):

            for i in range(texture_count):

                texture_information = R6O.Material_Information.Texture_Information()
                texture_information.read(binaryReader)
                self.textures.append(texture_information)

        class Texture_Information:
            def __init__(self) -> None:
                self.texture_hash = None

            def read(self, binaryReader):
                self.texture_hash = str(binascii.hexlify(binaryReader.readBytes(4)), 'ascii')
                binaryReader.seek(16, 1) # ? 

    class Vertex_Buffer_Information :
        def __init__(self):
            self.vertex_buffer_offset = 0
            self.vertex_attributes = 0
            self.vertex_number = 0

    class Face_Buffer_Information :
        def __init__(self):
            self.face_buffer_offset = 0
            self.face_number = 0