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

    clear_scene: bpy.props.BoolProperty(
        name="Clear scene",
        description="Clear the scene",
        default=False,
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
        layout.prop(props, "map_info_folder", text="")
        
        layout.label(text="Map Model Folder")
        layout.prop(props, "map_model_folder", text="")

        row = layout.row()
        row.prop(props, "clear_scene")

        layout.separator()  # Adds spacing

        # Button that calls the operator
        layout.operator("import_rr.mapimport_operator", text="Import Map") 