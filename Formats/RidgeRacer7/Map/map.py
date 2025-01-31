from ....Utilities.binaryReader import *

from .information import *

class MAP:

    def __init__(self):
        self.objects_information = {}

    def read(self, br: BinaryReader):
        br.readUInt()
        offset1 = br.readUInt()
        offset2 = br.readUInt()
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
            name = br.bytesToString(br.readBytes(32)).replace("\0", "")
            information = ObjectInformation()
            information.read(br)
            self.objects_information[name] = information

        
