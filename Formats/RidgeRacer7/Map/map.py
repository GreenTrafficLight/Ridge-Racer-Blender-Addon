from ....Utilities.binaryReader import *

class MAP:

    def __init__(self):
        pass

    def read(self, br: BinaryReader):
        object_informations_offset = br.readUInt()
        br.readUInt()

        file_size = br.readUInt()

        br.seek(object_informations_offset, 0)
        
        object_information_offsets = []
        object_informations_count = br.readUInt()
        object_informations_offset = br.readUInt()

        br.seek(object_informations_offset, 0)

        for i in range(object_informations_count):
            object_information_offsets.append(br.readUInt())

        
