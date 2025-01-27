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

class RR_OT_Model_Import(Operator, ImportHelper):
        """Load a Ridge Racer model file"""
        bl_idname = "import_rr.data"
        bl_label = "Import Ridge Racer model"

        filename_ext = ""
        filter_glob: StringProperty(default="*", options={'HIDDEN'}, maxlen=255,)

        clear_scene: BoolProperty(
            name="Clear scene",
            description="Example Tooltip",
            default=True,
        )

        def execute(self, context):   
                importModel(self.filepath, self.clear_scene)

                return {'FINISHED'}
        
def importModel(filepath: str, clear_scene: bool):
    if clear_scene:
        clearScene()

    file = open(filepath, 'rb')
    filename =  filepath.split("\\")[-1]
    bs = BinaryReader(file, ">")
    header = bs.bytesToString(bs.readBytes(4)).replace("\0", "")
    
    if filename == "Model":
        
        if header == "ArcL":
            arcl = ARCL(bs)
            arcl.read(bs)
            build_arcl_hierarchy(arcl)
        else:
            R6M_datas = []

            bs.seek(0, 0)

            R6M_count = bs.readUInt()
            R6M_list_offset = bs.readUInt()
            
            bs.seek(R6M_list_offset, 0)
            for offset in range(R6M_count):
                R6M_datas.append((bs.readUInt(), bs.readUInt()))

    elif header == "R7C":
        r7c = R7C()
        r7c.read(bs)
        build_r7c_hierarchy(r7c)
    elif header == "R7W":
        r7w = R7W()
        r7w.read(bs)
        build_r7w_hierarchy(r7w)
    elif header == "R6C":
        r6c = R6C()
        r6c.read(bs)
        build_r6c_hierarchy(r6c)
    
    return {'FINISHED'}