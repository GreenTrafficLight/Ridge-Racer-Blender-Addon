import bpy
import struct

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, PointerProperty
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

from .Blender.operators.OT_Model_Import import *
from .Blender.operators.OT_Map_Import import *
from .Blender.panels.PT_Map_Importer import *

bl_info = {
	"name": "Ridge Racer Modern Era Models format",
	"description": "Import Ridge Racer Modern Era Model",
	"author": "GreenTrafficLight",
	"version": (1, 1),
	"blender": (4, 0, 0),
	"location": "File > Import > Ridge Racer Modern Era Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}


classes = [
    MapProperties,
    RR_OT_Model_Import,
    RR_OT_Map_Import,
    RR_PT_Map_Importer
]

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(RR_OT_Model_Import.bl_idname, text="Ridge Racer")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_map_properties = bpy.props.PointerProperty(type=MapProperties)
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
