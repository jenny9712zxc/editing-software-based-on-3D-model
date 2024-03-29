#from load_stl import *

import sys
import math
import os

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,QWidget)
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL as gl
from PyQt5.QtWidgets import QPushButton
from load_stl import loader
from write_stl import ASCII_STL_Writer



class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()

        self.xSlider = self.createSlider()
        self.ySlider = self.createSlider()
        self.zSlider = self.createSlider()

        self.xSlider.valueChanged.connect(self.glWidget.setXRotation)
        self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        self.ySlider.valueChanged.connect(self.glWidget.setYRotation)
        self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        self.zSlider.valueChanged.connect(self.glWidget.setZRotation)
        self.glWidget.zRotationChanged.connect(self.zSlider.setValue)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        mainLayout.addWidget(self.xSlider)
        mainLayout.addWidget(self.ySlider)
        mainLayout.addWidget(self.zSlider)
        self.setLayout(mainLayout)

        self.xSlider.setValue(15 * 16)
        self.ySlider.setValue(345 * 16)
        self.zSlider.setValue(0 * 16)

        self.setWindowTitle("Hello GL")
        
        """
        pybutton = QPushButton('base', self)
        pybutton.resize(100,32)
        pybutton.move(0, 0)        
        pybutton.clicked.connect(self.clickMethod)
        """
        

    def createSlider(self):
        slider = QSlider(Qt.Vertical)

        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        return slider


class GLWidget(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        
        self.size=2
        

    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        print(self.getOpenglInfo())

        self.setClearColor(self.trolltechPurple.darker())
        #self.object = self.makeObject()
        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        
    def openFile(self, file):
        if glIsList(1)==1:
            glDeleteLists(1, 1)
            self.object=0
            print('delete list1')        

        self.object = self.makeObject(file)

        
    def newFile(self):
        if glIsList(1)==1:
            glDeleteLists(1, 1)
        if glIsList(2)==1:
            glDeleteLists(2, 1)


        
    def paintGL(self):
        print("paintGL")
        
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        if  glIsList(1)==1:
            gl.glCallList(self.object)#body        
        if  glIsList(2)==1:
            gl.glCallList(2)#base cuboid
        if  glIsList(3)==1:
            gl.glCallList(3)#base cylindr
        
    def resizeGL(self, width, height):
        self.w= width
        self.h=height
        print("resizeGL")
        side = min(width, height)
        if side < 0:
            return
        """
        if  self.size<0.1:
            self.size=0.1
        if  self.size>5:
            self.size=5
        """    
        size=1


        gl.glViewport((width - side) // 2, (height - side) // 2, side,side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-1*size*width/height, +1*size*width/height, +1*size, -1*size, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()
    """    
    def wheelEvent(self, event):
        delta=event.angleDelta()
        y=delta.y()
        print(y)
        if  y>0:
            self.size=self.size+1
            glScale(1.2, 1.2, 1.2)
        else:
            self.size=self.size-1
            glScale(0.8, 0.8, 0.8)
        #self.resizeGL(self.w, self.h)
        #gluLookAt (0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    """
        

    def makeObject(self, file):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)
        
        model=loader()
        model.load_stl(file)
        #model.load_stl(os.path.abspath('')+'/bunny.stl')
        model.draw()
        
        gl.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.setColor(self.trolltechGreen)

        gl.glVertex3d(x1, y1, -0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x3, y3, -0.05)
        gl.glVertex3d(x4, y4, -0.05)

        gl.glVertex3d(x4, y4, +0.05)
        gl.glVertex3d(x3, y3, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        gl.glVertex3d(x1, y1, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())
        


          
    def plotbase(self, base):
        if glIsList(2)==1:
            glDeleteLists(2, 1)
        print('base', base)
        if  base==0:
            return
            
        model=loader()
        if  base==1:
            model.load_stl(os.path.abspath('')+'/cuboid_buttom.stl')    

        elif  base==2:         
            model.load_stl(os.path.abspath('')+'/cylinder_buttom.stl')  

        glNewList(2, gl.GL_COMPILE)        
        base_list=model.draw()
        glEndList()
        del model


        with open('opengl_save.stl', 'w') as fp:
            writer = ASCII_STL_Writer(fp)
            writer.add_faces(base_list)
            writer.close()
               

