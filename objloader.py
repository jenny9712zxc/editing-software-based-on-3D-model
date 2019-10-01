import pygame
from OpenGL.GL import *
from write_stl import ASCII_STL_Writer
import os
from stl import mesh
import numpy as np
import stl

def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        #elif mtl is None:
            #print('mtl is None')
            #raise ValueError, "mtl file doesn't start with newmtl stmt"
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        else:
            mtl[values[0]] = map(float, values[1:])
    return contents

class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.stlList=[]

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        
        print('len(self.faces)', len(self.faces))
        for face in self.faces:#self.faces=35472
            vertices, normals, texture_coords, material = face
            #print(vertices)
            self.vertexList=[]
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):#len(vertices)=3
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
                
                #print(self.vertices[vertices[i] - 1])
                self.vertexList.append(self.vertices[vertices[i] - 1])                         
                
            glEnd()
            self.dealList()
            
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.save2stl()
        
        
        
    def dealList(self):
        List=[]
        #print('dealList')

        for i in range(len(self.vertexList)):
            v=self.vertexList[i]
            v0=(v[0], v[1], v[2])
            if i==0:
                v1=v0
            elif i==1:
                v2=v0
            elif i==2:
                v3=v0
            else:
                return
                """
                v1, v2, v3=v0, v1, v2
                list_tmp=[]
                list_tmp.append(tuple(v1))
                list_tmp.append(tuple(v2))
                list_tmp.append(tuple(v3))
                #print(list_tmp)
                List.append(list_tmp)
                """
        list_tmp=[]
        list_tmp.append(tuple(v1))
        list_tmp.append(tuple(v2))
        list_tmp.append(tuple(v3))    
        self.stlList.append(list_tmp)

        
    def save2stl(self):
        print('save2stl')
        with open('objLoader_save.stl', 'w') as fp:
            writer = ASCII_STL_Writer(fp)
            writer.add_faces(self.stlList)
            writer.close()
            
