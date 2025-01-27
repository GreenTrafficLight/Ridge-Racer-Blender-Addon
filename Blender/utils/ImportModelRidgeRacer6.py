import bpy
import struct
import bmesh
import os

from math import *
from mathutils import *

from ...Utilities import *
from ...Formats import *

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

    if normals != []:
        mesh.normals_split_custom_set_from_vertices(normals)

    """
    material = bpy.data.materials.get(r6o_material.name)
    if not material:
        material = bpy.data.materials.new(r6o_material.name)

    mesh.materials.append(material)
    """
