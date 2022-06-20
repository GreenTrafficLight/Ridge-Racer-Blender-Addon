import bpy

def clearScene():
    
    for object in bpy.context.scene.objects:
        bpy.data.objects.remove(object, do_unlink=True)

    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

    for image in bpy.data.images:
        bpy.data.images.remove(image)

def add_empty(name, parent_name):
    
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    empty = bpy.context.active_object
    empty.empty_display_size = 0.1
    empty.name = name
    if parent_name:
        empty.parent = parent_name

    return empty
