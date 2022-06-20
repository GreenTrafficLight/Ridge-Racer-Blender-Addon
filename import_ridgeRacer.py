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

def build_r6c_hierarchy(data):
    for structure, r6o in data.structures.items():

        if r6o != None:
            structure_empty = add_empty(structure, None)

            build_r6c(r6o[0], structure_empty)

def build_r6c(data, parent):

    for submesh in range(len(data.vertex_buffers)):

        mesh = bpy.data.meshes.new(parent.name + "_" + str(submesh))
        obj = bpy.data.objects.new(parent.name + "_" + str(submesh), mesh)
        obj.rotation_euler = (radians(90), 0, 0)

        if bpy.app.version >= (2, 80, 0):
            parent.users_collection[0].objects.link(obj)
        else:
            parent.users_collection[0].objects.link(obj)

        obj.parent = parent

        vertexList = {}
        facesList = []
        normals = []

        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Set vertices
        for j in range(len(data.vertex_buffers[submesh]["positions"])):
            vertex = bm.verts.new(data.vertex_buffers[submesh]["positions"][j])
            
            if data.vertex_buffers[submesh]["normals"] != []:
                vertex.normal = data.vertex_buffers[submesh]["normals"][j]
                normals.append(data.vertex_buffers[submesh]["normals"][j])
            
            vertex.index = j

            vertexList[j] = vertex

        faces = StripToTriangle(data.face_buffers[submesh], "cba")     

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
                l[uv_layer1].uv =  [data.vertex_buffers[submesh]["texCoords"][l.vert.index][0], 1 - data.vertex_buffers[submesh]["texCoords"][l.vert.index][1]]

        bm.to_mesh(mesh)
        bm.free()

        mesh.use_auto_smooth = True
        if normals != []:
            mesh.normals_split_custom_set_from_vertices(normals)


# Ridge Racer 7

def build_r7c_hierarchy(data):
    for lod, hierarchy in data.lods.items():
        
        if hierarchy :
            lod_empty = add_empty(lod, None)
            hood_empty = add_empty("Hood", lod_empty)
            front_empty = add_empty("Front", lod_empty)
            rear_empty = add_empty("Rear", lod_empty)
            side_empty = add_empty("Side", lod_empty)
            wing_empty = add_empty("Wing", lod_empty)

            for part, mesh in hierarchy.hierarchy_dictionary.items():

                if mesh :
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

                    count = 0
                    for submesh in mesh:
                        build_r7_model(lod, submesh, part_node, count)
                        count += 1

def build_r7w_hierarchy(data):

    for lod, part in data.lods.items():
        
        if part:
            lod_empty = add_empty(lod, None)

            count = 0
            for submesh in part.submeshes:
                build_r7_model(None, submesh, lod_empty, count)
                count += 1

def build_arcl_hierarchy(data):

    for i in range(len(data.R7M_list)):

        r7m_name = data.paths[i].split("\\")[-1]
        empty = add_empty(r7m_name[:-4], None)

        build_r7_model(None, data.R7M_list[i].r7o, empty, None)

def build_r7_model(lod, submesh, part_empty, count):

    for buffer in range(len(submesh.vertex_buffers)):

        mesh_name = part_empty.name + "_" + str(buffer)
        if lod != None:
            mesh_name = lod + "_" + mesh_name
        if count != None:
            mesh_name = mesh_name + "_" + str(count)

        mesh = bpy.data.meshes.new(mesh_name)
        obj = bpy.data.objects.new(mesh_name, mesh)
        
        obj.rotation_euler = (radians(90), 0, 0)

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

    file = open(filepath, 'rb')
    filename =  filepath.split("\\")[-1]
    bs = BinaryReader(file, ">")
    header = bs.bytesToString(bs.readBytes(4)).replace("\0", "")
    
    if filename == "Model":
        if header == "ArcL":
            arcl = ARCL(bs)
            arcl.read_paths()
            arcl.read_R7M()
            build_arcl_hierarchy(arcl)
        else:
            R6M_datas = []

            R6M_count = bs.readUInt()
            R6M_list_offset = bs.readUInt()
            
            bs.seek(R6M_list_offset, 0)
            for offset in range(R6M_count):
                R6M_datas.append((bs.readUInt(), bs.readUInt()))

    elif header == "R7C":
        r7c = R7C(bs)
        build_r7c_hierarchy(r7c)
    elif header == "R7W":
        r7w = R7W(bs)
        build_r7w_hierarchy(r7w)
    elif header == "R6C":
        r6c = R6C(bs)
        build_r6c_hierarchy(r6c)
    
    return {'FINISHED'}

if __name__ == '__main__':
    main()
