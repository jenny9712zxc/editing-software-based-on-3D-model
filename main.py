# -*- coding: utf-8 -*-

import sys 	
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget , QFileDialog 
from Ui_MainForm import Ui_MainWindow  
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure # For Matplotlib Figure Object
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import numpy as np
from stl import mesh
import stl
import os.path
from objloader import *
from opengl_plot import *

def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

class MainForm( QMainWindow , Ui_MainWindow, QWidget): 
	def __init__(self):  
		super(MainForm,self).__init__()  
		self.setupUi(self) 
		# 菜单的点击事件，当点击关闭菜单时连接槽函数 close()     
		self.fileCloseAction.triggered.connect(self.close)  
		# 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()     
		self.fileOpenAction.triggered.connect(self.openMsg)    
		# 菜单的点击事件，当点击儲存菜单时连接槽函数 saveMsg()     
		self.fileSaveAction.triggered.connect(self.saveMsg) 
		# 菜单的点击事件，当点击新建菜单时连接槽函数 newMsg()     
		self.fileNewAction.triggered.connect(self.newMsg)
		       
        
		self.object = Window()
		Layout=self.gridLayout
		Layout.addWidget(self.object, 0, 0) #adding the QWidget
        
		self.secondConvas=ConfigWidget()
		Layout2=self.gridLayout_2
		Layout2.addWidget(self.secondConvas, 1, 0)#adding the QWidget
        
        
        #菜單_編輯
		#立體圖型
		self.actionnull.triggered.connect(self.add_base0)
		self.actioncuboid.triggered.connect(self.add_base1)
		self.actioncylinder.triggered.connect(self.add_base2)

        
        
		
        


	def openMsg(self):  
		fileName, filetype = QFileDialog.getOpenFileName(self,"打開","C:/","All Files (*);;Text Files (*.txt);;STL Files (*.stl);;OBJ Files (*.obj)") 
		# 在状态栏显示文件地址  		
		self.statusbar.showMessage(fileName)   
		print('fileName:', fileName, '\nfiletype:', filetype)
		print(type(fileName))
		print(type(filetype))
		if filetype=="OBJ Files (*.obj)":
		    print("read obj file")
		    obj = OBJ(fileName, swapyz=True)
		    fileName="objLoader_save.stl"
		    print("convert obj to stl")
		
		self.secondConvas.show_model(fileName)
		self.object.glWidget.openFile(fileName)
		
	def saveMsg(self): 
		fileName, filetype= QFileDialog.getSaveFileName(self,"儲存","C:/","All Files (*);;Text Files (*.txt);;STL Files (*.stl)") 
		# 在状态栏显示文件地址  		
		print('fileName:', fileName, '\nfiletype:', filetype)
		self.statusbar.showMessage(fileName)
		self.secondConvas.saveModel(fileName)
        
        
	def newMsg(self):
		self.secondConvas.ThreeDWin.renew()
		self.object.glWidget.newFile()
        
	def add_base0(self):
		self.secondConvas.ThreeDWin.base=0
		self.secondConvas.ThreeDWin.plot_base(self.secondConvas.ThreeDWin.buttom_point)
		self.object.glWidget.plotbase(self.secondConvas.ThreeDWin.base)
		
	def add_base1(self):
		self.secondConvas.ThreeDWin.base=1
		self.secondConvas.ThreeDWin.plot_base(self.secondConvas.ThreeDWin.buttom_point)
		self.object.glWidget.plotbase(self.secondConvas.ThreeDWin.base)
		
	def add_base2(self):
		self.secondConvas.ThreeDWin.base=2
		self.secondConvas.ThreeDWin.plot_base(self.secondConvas.ThreeDWin.buttom_point) 
		self.object.glWidget.plotbase(self.secondConvas.ThreeDWin.base)
        
class ThreeDSurface_GraphWindow(FigureCanvas): #Class for 3D window
    
    def __init__(self):
        self.fig =plt.figure(figsize=(10,10), dpi=100)
        FigureCanvas.__init__(self, self.fig) #creating FigureCanvas
        self.axes = self.fig.gca(projection='3d')#generates 3D Axes object
        #self.axes.hold(False)#clear axes on each run
        self.axes.clear()
        self.setWindowTitle("Main") # sets Window title  
        self.axes.set_aspect('equal') 
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        self.axes.set_zlabel('z')
        self.mainBody=None
        self.base=0
        self.buttom_point=[0, 0, 0]
        self.x0, self.x1, self.y0, self.y1, self.z0, self.z1=0, 0.1, 0, 0.1, 0, 0.1
        
    def renew(self):
        self.axes.clear()
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        self.axes.set_zlabel('z')
        

    def DrawGraph(self, x, y, z):#Fun for Graph plotting
        self.axes.clear()#clear the axes before plotting
        self.axes.plot_surface(x, y, z) #plots the 3D surface plot
        self.draw()
            
    def PlotGragh(self, file_mesh):
        if self.mainBody==None:
            self.mainBody=file_mesh
        self.axes.clear()#clear the axes before plotting
        self.axes.add_collection3d(mplot3d.art3d.Poly3DCollection(file_mesh.vectors))
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        self.axes.set_zlabel('z')
        #求buttom_point
        min=100
        index1=0
        index2=0
        i=-1
        j=-1
        center_x=center_y=0
        for tri in file_mesh.vectors:
            for v in tri:
                center_x=center_x+v[0]
                center_y=center_y+v[1]
                if v[2]<min:
                    i=index1
                    j=index2
                    min=v[2]
                index2=index2+1
            index2=0
            index1=index1+1
        self.x0, self.x1, self.y0, self.y1, self.z0, self.z1=find_mins_maxs(file_mesh)
        center_x=(self.x0+self.x1)/2#center_x/index1
        center_y=(self.y0+self.y1)/2#center_y/index1
        self.buttom_point=[center_x, center_y, self.z0]

  
    def combine(self, file_mesh):
        if self.base==1:
            append=mesh.Mesh.from_file('cuboid_buttom.stl')
        elif  self.base==2:
            append=mesh.Mesh.from_file('cylinder_buttom.stl')
            
        append=mesh.Mesh.from_file('cylinder_buttom.stl')
        combined = mesh.Mesh(np.concatenate([file_mesh.data, append.data]))
        combined.save('combined.stl', mode=stl.Mode.ASCII)  # save as ASCII
        return combined
        
    def plot_base(self, center): 
        length = abs(self.x1-self.x0)*1.5         
        width = abs(self.y1-self.y0)* 1.5
        r=(length+width)/4#常和寬的平均  再取一半
        height = 4
        self.PlotGragh(self.mainBody)


        if self.base==1:
            result=self.base_cuboid(center, length, width, height) 
        elif  self.base==2:
            result=self.base_cylinder(center, r,height) 

        
    def base_cuboid(self,center, l, w, h): 
            ox, oy, oz = center 

            x=l
            y=w
            z=h/100
            ox=ox-x/2
            oy=oy-y/2
            oz=oz+0
            # Create 6 faces of a cube, 2 triagles per face
            data = np.zeros(12, dtype=mesh.Mesh.dtype)
            # Top of the cube
            data['vectors'][0] = np.array([[ox+0, oy+y, oz+z],[ox+x,oy+ 0,oz+ z],[ox+0,oy+ 0, oz+z]])
            data['vectors'][1] = np.array([[ox+x, oy+0, oz+z],[ox+0, oy+y, oz+z],[ox+x, oy+y, oz+z]])
            # Right face
            data['vectors'][2] = np.array([[ox+x, oy+0, oz+0],[ox+x, oy+0, oz+z],[ox+x, oy+y, oz+0]])
            data['vectors'][3] = np.array([[ox+x, oy+y, oz+z],[ox+x, oy+0, oz+z],[ox+x, oy+y, oz+0]])
            # Left face
            data['vectors'][4] = np.array([[ox+0, oy+0, oz+0],[ox+x, oy+0, oz+0],[ox+x, oy+0, oz+z]])
            data['vectors'][5] = np.array([[ox+0, oy+0, oz+0],[ox+0, oy+0, oz+z],[ox+x, oy+0, oz+z]])
            # Bottem of the cube
            data['vectors'][6] = np.array([[ox+0, oy+y, oz+0],[ox+x, oy+0, oz+0],[ox+0, oy+0, oz+0]])
            data['vectors'][7] = np.array([[ox+x, oy+0, oz+0],[ox+0, oy+y, oz+0],[ox+x, oy+y, oz+0]])
            # Right back
            data['vectors'][8] = np.array([[ox+0, oy+0, oz+0],[ox+0, oy+0,oz+ z],[ox+0, oy+y, oz+0]])
            data['vectors'][9] = np.array([[ox+0, oy+y, oz+z],[ox+0, oy+0, oz+z],[ox+0, oy+y, oz+0]])
            # Left back 
            data['vectors'][10] = np.array([[ox+0, oy+y, oz+0],[ox+x, oy+y, oz+0],[ox+x, oy+y, oz+z]])
            data['vectors'][11] = np.array([[ox+0, oy+y, oz+0],[ox+0, oy+y, oz+z],[ox+x, oy+y, oz+z]])
            
            _mesh = [mesh.Mesh(data.copy())   for _ in range(1)]
            for m in _mesh:
                self.axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))
            
            #save
            total_length_data = 0
            for i in range(len(_mesh)):
                total_length_data += len(_mesh[i].data)  

            data = np.zeros(total_length_data, dtype = mesh.Mesh.dtype)
            data['vectors'] = np.array(_mesh).reshape((-1, 9)).reshape((-1, 3, 3))
            mesh_final = mesh.Mesh(data.copy())
            mesh_final.save('cuboid_buttom.stl')
            
    def base_cylinder(self,center, r, h): 
            ox, oy, oz = center 
            theta = np.linspace(0, 2*np.pi, 100)
            x_list=r*np.cos(theta)
            y_list=r*np.sin(theta)
            z=-h/100
            ox=ox
            oy=oy
            oz=oz-z
            # Create 6 faces of a cube, 2 triagles per face
            data = np.zeros(400, dtype=mesh.Mesh.dtype)
            for i in range(100):
                x1=x_list[i]
                y1=y_list[i]
                if i==99:
                    i=-1
                x2=x_list[i+1]
                y2=y_list[i+1]
                # Bottem face
                data['vectors'][4*i+0] = np.array([[ox+x2, oy+y2, oz+0],[ox+x1, oy+y1, oz+0],[ox+0, oy+0, oz+0]])
                # Top face
                data['vectors'][4*i+1] = np.array([[ox+x2, oy+y2, oz+z],[ox+x1, oy+y1, oz+z],[ox+0, oy+0, oz+z]])
                # outside face
                data['vectors'][4*i+2] = np.array([[ox+x2, oy+y2, oz+0],[ox+x1, oy+y1, oz+0],[ox+x1, oy+y1, oz+z]])
                data['vectors'][4*i+3] = np.array([[ox+x2, oy+y2, oz+z],[ox+x1, oy+y1, oz+z],[ox+x2, oy+y2, oz+0]])
                
            
            
            _mesh = [mesh.Mesh(data.copy())   for _ in range(1)]
            for m in _mesh:
                self.axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))
            
            #save
            total_length_data = 0
            for i in range(len(_mesh)):
                total_length_data += len(_mesh[i].data)  

            data = np.zeros(total_length_data, dtype = mesh.Mesh.dtype)
            data['vectors'] = np.array(_mesh).reshape((-1, 9)).reshape((-1, 3, 3))
            mesh_final = mesh.Mesh(data.copy())
            mesh_final.save('cylinder_buttom.stl')      
            
class ConfigWidget(QWidget):# The QWidget in which the 3D window is been embedded
    def __init__(self, parent=None):
        super(ConfigWidget, self).__init__(parent)
        self.ThreeDWin = ThreeDSurface_GraphWindow()#creating 3D Window
        MainLayout =QtWidgets.QGridLayout()# Layout for Main Tab Widget
        MainLayout.setRowMinimumHeight(0, 5) #setting layout parameters
        MainLayout.setRowMinimumHeight(2, 10)
        MainLayout.setRowMinimumHeight(4, 5)
        #MainLayout.addWidget(self.Combo, 1, 1)#add GroupBox to Main layout
        MainLayout.addWidget(self.ThreeDWin,1,1)#add 3D Window to Main layout
        self.setLayout(MainLayout) #sets Main layout
        
        
        #o=os.path.exists(r"C:\Users\F64054049\.....").....路徑含有"\"前面要加r
        #o=os.path.exists("C:/Users/F64054049/Desktop/PyQt5-master/Chapter03/mainWin/gear-new_Rescaled0.2.stl")
        #if o==True:
            #your_mesh = mesh.Mesh.from_file(r"C:\Users\F64054049\Desktop\PyQt5-master\Chapter03\mainWingear-new_Rescaled0.2.stl")
        #else:
            #print("no such file\n")
            #your_mesh = mesh.Mesh.from_file('gear-new_Rescaled0.2.stl')
            
    def  show_model(self,file):    
        print(file)
        #plot 3d
        # Load the STL files and add the vectors to the plot
        #your_mesh = mesh.Mesh.from_file(r"C:\Users\F64054049\Desktop\PyQt5-master\Chapter03\mainWingear-new_Rescaled0.2.stl")
        self.your_mesh = mesh.Mesh.from_file(file)
        self.ThreeDWin.PlotGragh(self.your_mesh)
        #self.saveModel('numpy_save.stl')
        """        
        x=np.linspace(-6,6,30) #X coordinates
        y=np.linspace(-6,6,30) #Y coordinates
        X,Y=np.meshgrid(x,y) #Forming MeshGrid
        Z=self.f(X,Y)
        self.ThreeDWin.DrawGraph(X,Y,Z)#call Fun for Graph plot
        """ 

    def f(self,x,y):#For Generating Z coordinates
        return np.sin(np.sqrt(x**2+y**2))
        
    def saveModel(self,filename ):
        if self.your_mesh==None:
            print('no mesh')
            return
        elif self.ThreeDWin==0:
            self.your_mesh.save(filename )
        else:
            model=self.ThreeDWin.combine(self.your_mesh)
            model.save(filename )

    
if __name__=="__main__":  
	app = QApplication(sys.argv)  
	win = MainForm()  
	win.__init__()
	win.show()  
	sys.exit(app.exec_()) 
