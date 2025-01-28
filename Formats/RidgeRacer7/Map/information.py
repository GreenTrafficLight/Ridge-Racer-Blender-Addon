from ....Utilities.binaryReader import *

class MAP_INFORMATION_CONTAINER:
    def __init__(self):
        self.offset = 0
        self.count = 0

class MAP_INFORMATION:

    def __init__(self):
        self.name = ""
        self.type = ""
        self.containers = []

    def read(self, br: BinaryReader):
        self.name = br.bytesToString(br.readBytes(32)).replace("\0", "")
        self.type = br.bytesToString(br.readBytes(32)).replace("\0", "")

        for i in range(4):
            # map_information_data 1 = objet transformations
            # map_information_data 2 = ?
            # map_information_data 3 = ?
            # map_information_data 4 = ?
            
            map_information_container = MAP_INFORMATION_CONTAINER()
            map_information_container.offset = br.readUInt()
            map_information_container.count = br.readUInt()

            self.containers.append(map_information_container)