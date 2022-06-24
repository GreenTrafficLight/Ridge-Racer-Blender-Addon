bl_info = {
	"name": "Ridge Racer Modern Era Models format",
	"description": "Import Ridge Racer Modern Era Model",
	"author": "GreenTrafficLight",
	"version": (1, 0),
	"blender": (2, 80, 0),
	"location": "File > Import > Ridge Racer Modern Era Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

import bpy
import struct

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, PointerProperty
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


class ImportRidgeRacer(Operator, ImportHelper):
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
        from . import  import_ridgeRacer
        return import_ridgeRacer.main(self.filepath, self.clear_scene)

class MyProperties(PropertyGroup):

    path : StringProperty(
        name="",
        description="Path to Directory",
        default="",
        subtype='FILE_PATH')

class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "OBJECT_PT_my_panel"
    bl_label = "Ridge Racer Importer"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Ridge Racer Importer"


    def draw(self, context):
        layout = self.layout
        scn = context.scene
        my_tool = scn.my_tool
        
        col = layout.column(align=True)
        col.label(text = "Test")
        col.prop(my_tool, "path", text="")
        
        


classes = (MyProperties, ImportRidgeRacer, OBJECT_PT_CustomPanel)

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportRidgeRacer.bl_idname, text="Ridge Racer")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
