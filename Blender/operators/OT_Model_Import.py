import bpy

from bpy.types import Operator
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        CollectionProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        )

from ...Utilities import *
from ..utils.ImportModelRidgeRacer6 import *
from ..utils.ImportModelRidgeRacer7 import *

from ...Formats.RidgeRacerVita.rnc import *

class RR_OT_Model_Import(Operator, ImportHelper):
        """Load a Ridge Racer model file"""
        bl_idname = "import_rr.data"
        bl_label = "Import Ridge Racer model"

        filename_ext = ""
        filter_glob: StringProperty(default="*", options={'HIDDEN'}, maxlen=255,)

        clear_scene: BoolProperty(
            name="Clear scene",
            description="Clear the scene",
            default=False,
        )

        def execute(self, context):   
            importModel(self.filepath, self.clear_scene)

            return {'FINISHED'}
        
def importModel(filepath: str, clear_scene: bool):
    if clear_scene:
        clearScene()

    file = open(filepath, 'rb')
    filename =  filepath.split("\\")[-1]
    br = BinaryReader(file, ">")
    header = br.bytesToString(br.readBytes(4)).replace("\0", "")
    
    if filename == "Model":
        
        if header == "ArcL":
            arcl = ARCL(br)
            arcl.read(br)
            build_arcl_hierarchy(arcl)
        else:
            R6M_datas = []

            br.seek(0, 0)

            R6M_count = br.readUInt()
            R6M_list_offset = br.readUInt()
            
            br.seek(R6M_list_offset, 0)
            for offset in range(R6M_count):
                R6M_datas.append((br.readUInt(), br.readUInt()))

    elif header == "R6C":
        r6c = R6C()
        r6c.read(br)
        build_r6c_hierarchy(r6c)
    elif header == "R7C":
        r7c = R7C()
        r7c.read(br)
        build_r7c(r7c)
    elif header == "R7W":
        r7w = R7W()
        r7w.read(br)
        build_r7w_hierarchy(r7w)
    elif header == "RNC":
        br.endian = "<"
        rnc = RNC()
        rnc.read(br)
    
    return {'FINISHED'}