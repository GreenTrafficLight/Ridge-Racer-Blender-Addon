import bpy

from ...Utilities import *
from ..utils.ImportModelRidgeRacer6 import *
from ..utils.ImportModelRidgeRacer7 import *
from ...Formats.RidgeRacer7.Map.map import MAP

class RR_OT_Map_Import(bpy.types.Operator):
        """Load a Ridge Racer model file"""
        bl_idname = "import_rr.mapimport_operator"
        bl_label = "Import Ridge Racer map"

        def execute(self, context):   
            props = context.scene.my_map_properties

            if props.map_model_folder == "":
                return {'FINISHED'}
            
            importMap(props.map_info_folder, props.map_model_folder, props.clear_scene)

            return {'FINISHED'}
        
def importMap(mapFilePath: str, modelFilePath: str, clear_scene: bool):
    if clear_scene:
        clearScene()

    map = None
    with open(mapFilePath + "Map", "rb") as mapFile:
        bs = BinaryReader(mapFile, ">")

        map = MAP()
        map.read(bs)

    with open(modelFilePath + "Model", "rb") as modelFile:
        bs = BinaryReader(modelFile, ">")
        header = bs.bytesToString(bs.readBytes(4)).replace("\0", "")

        if header == "ArcL":
            arcl = ARCL(bs)
            arcl.read(bs)
            build_arcl_hierarchy(arcl, map)