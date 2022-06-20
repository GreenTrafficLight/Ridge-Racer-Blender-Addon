class MAP:

    def __init__(self, br):
        self.br = br

        offsets = []
        for i in range(2):
            # offset 1 = map informations
            # offset 2 = ?
            offsets.append(self.br.readUInt())

        file_size = self.br.readUInt()

        self.br.seek(offsets[0], 0)
        self.read_map_informations()


    def read_map_informations(self):
        
        map_information_offsets = []

        map_information_count = self.br.readUInt()
        map_information_list_offset = self.br.readUInt()

        self.br.seek(map_information_list_offset, 0)

        for i in range(map_information_count):
            map_information_offsets.append(self.br.readUInt())

class MAP_INFORMATION:

    def __init__(self, br):
        self.br = br
        self.name = ""
        self.type = ""
        
        self.name = self.br.bytesToString(self.br.readBytes(32)).replace("\0", "")
        self.type = self.br.bytesToString(self.br.readBytes(32)).replace("\0", "")

        map_information_datas = []

        for i in range(4):
            # map_information_data 1 = objet transformations
            # map_information_data 2 = ?
            # map_information_data 3 = ?
            # map_information_data 4 = ?
            
            map_information_data = {
                "offset" : [],
                "count" : []
            }

            map_information_data.offset = self.br.readUInt()
            map_information_data.count = self.br.readUInt()

            map_information_datas.append(map_information_data)

    def read_transformations(self, map_information_data_offset, map_information_data_count):
        
        self.br.seek(map_information_data_offset, 0)

    class TRANSFORMATION:

        def __init__(self, br):
            super.__init__()
            self.br = br

            self.unknown_vector4_2 = None
            self.unknown_vector4_1 = None
            self.transformation_matrix = None

        
