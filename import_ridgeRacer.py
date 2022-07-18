import bpy
import struct
import bmesh
import os

from math import *
from mathutils import *
from io import BytesIO

from .Blender import *
from .Utilities import *
from .Formats import *

# Ridge Racer 6

def build_r6c_hierarchy(r6c):
    for structure, r6o in r6c.structures.items():

        if r6o != None:
            
            structure_empty = add_empty(structure, empty_rotation=(radians(90), 0, 0))

            for i in range(len(r6o[1])):
                
                empty_parent = None
                
                if r6o[1][i][0] in r6c.transformations:
                    empty_parent = add_empty(str(r6o[1][i][0]), structure_empty, r6c.transformations[r6o[1][i][0]].translation, r6c.transformations[r6o[1][i][0]].rotation)
                else:
                    empty_parent = add_empty(str(r6o[1][i][0]), structure_empty)

                """
                if r6o[1][i][0] == 0:
                    body_empty = add_empty("0", structure_empty)
                    empty_parent = body_empty
                else:
                    empty_parent = structure_empty
                """

                build_r6o(r6o[0], i, empty_parent)

def build_r6o(data, index, parent):
    
    mesh = bpy.data.meshes.new(parent.name + "_" + str(index))
    obj = bpy.data.objects.new(parent.name + "_" + str(index), mesh)

    if bpy.app.version >= (2, 80, 0):
        parent.users_collection[0].objects.link(obj)
    else:
        parent.users_collection[0].objects.link(obj)

    obj.parent = parent

    vertex_buffer = data.vertex_buffers[index]
    face_buffer = data.face_buffers[index]
    r6o_material = data.materials[index]

    vertexList = {}
    facesList = []
    normals = []

    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Set vertices
    for j in range(len(vertex_buffer["positions"])):
        vertex = bm.verts.new(vertex_buffer["positions"][j])
        
        if vertex_buffer["normals"] != []:
            vertex.normal = vertex_buffer["normals"][j]
            normals.append(vertex_buffer["normals"][j])
        
        vertex.index = j

        vertexList[j] = vertex

    faces = StripToTriangle(face_buffer, "cba")     

    # Set faces
    for j in range(0, len(faces)):
        try:
            face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
            face.smooth = True
            facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
        except:
            pass
            # print(shape.geomName)

    # Set uv
    for f in bm.faces:
        uv_layer1 = bm.loops.layers.uv.verify()
        for l in f.loops:
            l[uv_layer1].uv =  [vertex_buffer["texCoords"][l.vert.index][0], 1 - vertex_buffer["texCoords"][l.vert.index][1]]

    bm.to_mesh(mesh)
    bm.free()

    mesh.use_auto_smooth = True
    if normals != []:
        mesh.normals_split_custom_set_from_vertices(normals)

    """
    material = bpy.data.materials.get(r6o_material.name)
    if not material:
        material = bpy.data.materials.new(r6o_material.name)

    mesh.materials.append(material)
    """


# Ridge Racer 7

def build_r7c_hierarchy(data):
    for lod, hierarchy in data.lods.items():
        
        if hierarchy :
            
            lod_empty = add_empty(lod, empty_rotation=(radians(90), 0, 0))
            hood_empty = add_empty("Hood", lod_empty)
            front_empty = add_empty("Front", lod_empty)
            rear_empty = add_empty("Rear", lod_empty)
            side_empty = add_empty("Side", lod_empty)
            wing_empty = add_empty("Wing", lod_empty)

            for part, meshes in hierarchy.hierarchy_dictionary.items():

                if meshes :
                    part_node = add_empty(part, None)
                    if "Hood" in part:
                        part_node.parent = hood_empty
                    elif "Front" in part:
                        part_node.parent = front_empty
                    elif "Rear" in part:
                        part_node.parent = rear_empty
                    elif "Side" in part:
                        part_node.parent = side_empty
                    elif "Wing" in part:
                        part_node.parent = wing_empty
                    else:
                        part_node.parent = lod_empty

                    index = 0
                    for mesh in meshes:
                        
                        #empty_parent = part_node
                        
                        if mesh[1][0] in data.transformations:
                            #empty_parent.location = data.transformations[mesh[1][0]].translation
                            empty_parent = add_empty(str(mesh[1][0]), part_node, data.transformations[mesh[1][0]].translation, data.transformations[mesh[1][0]].rotation)
                        else:
                            empty_parent = add_empty(str(mesh[1][0]), part_node)

                        build_r7o(lod, mesh[0], empty_parent, index)
                        index += 1
                    
def build_r7w_hierarchy(data):

    for lod, part in data.lods.items():
        
        if part:
            lod_empty = add_empty(lod, None)

            count = 0
            for submesh in part.submeshes:
                build_r7o(None, submesh, lod_empty, count)
                count += 1

def build_arcl_hierarchy(data):

    for i in range(len(data.R7M_list)):

        r7m_name = data.paths[i].split("\\")[-1]
        empty = add_empty(r7m_name[:-4], None)

        build_r7o(None, data.R7M_list[i].r7o, empty, None)

def build_r7o(lod, submesh, part_empty, count):

    for buffer in range(len(submesh.vertex_buffers)):

        if part_empty.parent != None:
            mesh_name = part_empty.parent.name + "_" + str(buffer)
        else:
            mesh_name = part_empty.name + "_" + str(buffer)
        
        
        if lod != None:
            mesh_name = lod + "_" + mesh_name
        if count != None:
            mesh_name = mesh_name + "_" + str(count)

        mesh = bpy.data.meshes.new(mesh_name)
        obj = bpy.data.objects.new(mesh_name, mesh)
        
        #obj.rotation_euler = (radians(90), 0, 0)

        if bpy.app.version >= (2, 80, 0):
            part_empty.users_collection[0].objects.link(obj)
        else:
            part_empty.users_collection[0].objects.link(obj)

        obj.parent = part_empty

        vertexList = {}
        facesList = []
        normals = []

        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Set vertices
        for j in range(len(submesh.vertex_buffers[buffer]["positions"])):
            vertex = bm.verts.new(submesh.vertex_buffers[buffer]["positions"][j])
            
            if submesh.vertex_buffers[buffer]["normals"] != []:
                vertex.normal = submesh.vertex_buffers[buffer]["normals"][j]
                normals.append(submesh.vertex_buffers[buffer]["normals"][j])
            
            vertex.index = j

            vertexList[j] = vertex

        faces = StripToTriangle(submesh.face_buffers[buffer], "cba")     

        # Set faces
        for j in range(0, len(faces)):
            try:
                face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
            except:
                pass
                # print(shape.geomName)

        # Set uv
        if submesh.vertex_buffers[buffer]["texCoords"] != []:
            for f in bm.faces:
                uv_layer1 = bm.loops.layers.uv.verify()
                for l in f.loops:
                    l[uv_layer1].uv =  [submesh.vertex_buffers[buffer]["texCoords"][l.vert.index][0], 1 - submesh.vertex_buffers[buffer]["texCoords"][l.vert.index][1]]

        bm.to_mesh(mesh)
        bm.free()

        mesh.use_auto_smooth = True
        if normals != []:
            mesh.normals_split_custom_set_from_vertices(normals)


# Main

def main(filepath, clear_scene):
    if clear_scene:
        clearScene()

    test = bpy.context.scene.my_tool.path

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

if __name__ == '__main__':
    main()
