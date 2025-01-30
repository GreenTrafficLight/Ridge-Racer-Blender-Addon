import bpy


class MapProperties(bpy.types.PropertyGroup):
    map_info_folder: bpy.props.StringProperty(
        name="Map Information Folder",
        subtype='DIR_PATH'
    )
    
    map_model_folder: bpy.props.StringProperty(
        name="Map Model Folder",
        subtype='DIR_PATH'
    )

class RR_PT_Map_Importer(bpy.types.Panel):
    bl_label = "Map Importer"
    bl_idname = "RR_PT_map_importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        props = context.scene.my_map_properties
        
        layout.label(text="Map Information Folder")
        layout.prop(props, "map_info_folder")
        
        layout.label(text="Map Model Folder")
        layout.prop(props, "map_model_folder")