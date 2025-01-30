from ....Utilities.binaryReader import *

from .information import *

class MAP:

    def __init__(self):
        pass

    def read(self, br: BinaryReader):
        offset1 = br.readUInt()
        br.readUInt()

        file_size = br.readUInt()

        br.seek(offset1, 0)
        
        object_information_offsets = []
        object_informations_count = br.readUInt()
        object_informations_offset = br.readUInt()

        br.seek(object_informations_offset, 0)

        for i in range(object_informations_count):
            object_information_offsets.append(br.readUInt())

        for offset in object_information_offsets:
            br.seek(offset, 0)
            information = ObjectInformation()
            information.read(br)

        
