import bpy
import struct
import bmesh
import os

from math import *
from mathutils import *

from ...Utilities import *
from ...Formats import *


def build_r7c_hierarchy(data: R7C):
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
                        
                        # if mesh[1][0] in data.transformations:
                        #     #empty_parent.location = data.transformations[mesh[1][0]].translation
                        #     empty_parent = add_empty(str(mesh[1][0]), part_node, data.transformations[mesh[1][0]].translation, data.transformations[mesh[1][0]].rotation)
                        # else:
                        #     empty_parent = add_empty(str(mesh[1][0]), part_node)

                        build_r7o(lod, mesh[0], part_node, index)
                        index += 1
                    
def build_r7w_hierarchy(data: R7W):

    for lod, part in data.lods.items():
        
        if part:
            lod_empty = add_empty(lod, None)

            count = 0
            for submesh in part.submeshes:
                build_r7o(None, submesh, lod_empty, count)
                count += 1

def build_arcl_hierarchy(data: ARCL):

    for i in range(len(data.R7M_list)):

        r7m_name = data.paths[i].split("\\")[-1]
        empty = add_empty(r7m_name[:-4], None)

        for r7m in data.R7M_list:
            print("test")

        #build_r7o(None, data.R7M_list[i].r7o, empty, None)

def build_r7o(lod: str, submesh: R7O, part_empty, count: int):

    for buffer in range(len(submesh.vertexBuffers)):

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
        for j in range(len(submesh.vertexBuffers[buffer]["positions"])):
            vertex = bm.verts.new(submesh.vertexBuffers[buffer]["positions"][j])
            
            if submesh.vertexBuffers[buffer]["normals"] != []:
                vertex.normal = submesh.vertexBuffers[buffer]["normals"][j]
                normals.append(submesh.vertexBuffers[buffer]["normals"][j])
            
            vertex.index = j

            vertexList[j] = vertex

        faces = StripToTriangle(submesh.faceBuffers[buffer], "cba")     

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
        if submesh.vertexBuffers[buffer]["texCoords"] != []:
            for f in bm.faces:
                uv_layer1 = bm.loops.layers.uv.verify()
                for l in f.loops:
                    l[uv_layer1].uv =  [submesh.vertexBuffers[buffer]["texCoords"][l.vert.index][0], 1 - submesh.vertexBuffers[buffer]["texCoords"][l.vert.index][1]]

        bm.to_mesh(mesh)
        bm.free()

        if normals != []:
            mesh.normals_split_custom_set_from_vertices(normals)
