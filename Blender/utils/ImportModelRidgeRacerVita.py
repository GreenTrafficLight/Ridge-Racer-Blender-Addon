import bpy
import struct
import bmesh
import os

from math import *
from mathutils import *

from ...Utilities import *
from ...Formats import *

def buildRNC(rnc: RNC, emptyParentName: str):

    emptyParent = add_empty(emptyParentName, empty_rotation=(radians(90), 0, 0))

    ndvi: NDVI
    for ndvi in rnc.ndviList:

        mesh: NDVI.Mesh
        for mesh in ndvi.meshes:

            meshName = mesh.name
            meshEmpty = add_empty(meshName, emptyParent)

            subMesh: NDVI.SubMesh
            for subMeshIndex, subMesh in enumerate(mesh.subMeshes):

                subMeshName = f'{meshName}_{subMeshIndex}'

                mesh = bpy.data.meshes.new(subMeshName)
                obj = bpy.data.objects.new(subMeshName, mesh)

                if bpy.app.version >= (2, 80, 0):
                    meshEmpty.users_collection[0].objects.link(obj)
                else:
                    meshEmpty.users_collection[0].objects.link(obj)

                obj.parent = meshEmpty

                vertexList = {}
                facesList = []
                normals = []

                bm = bmesh.new()
                bm.from_mesh(mesh)

                # Set vertices
                for j in range(len(subMesh.vertexBuffer["positions"])):
                    vertex = bm.verts.new(subMesh.vertexBuffer["positions"][j])
                    
                    if subMesh.vertexBuffer["normals"] != []:
                        vertex.normal = subMesh.vertexBuffer["normals"][j]
                        normals.append(subMesh.vertexBuffer["normals"][j])
                    
                    vertex.index = j

                    vertexList[j] = vertex

                faces = StripToTriangle(subMesh.faceBuffer)     

                # Set faces
                for j in range(0, len(faces)):
                    try:
                        face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
                        face.smooth = True
                    except:
                        for Face in facesList:
                            if set([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]) == set(Face[1]):
                                face = Face[0].copy(verts=False, edges=True)
                                face.normal_flip()
                                face.smooth = True
                                break

                    facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])

                bm.to_mesh(mesh)
                bm.free()

                if normals != []:
                    mesh.normals_split_custom_set_from_vertices(normals)
