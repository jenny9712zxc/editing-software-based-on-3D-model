# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\F64054049\Desktop\final\MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(657, 887)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 601, 371))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(30, 450, 591, 381))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_E = QtWidgets.QMenu(self.menubar)
        self.menu_E.setObjectName("menu_E")
        self.menu_4 = QtWidgets.QMenu(self.menu_E)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.fileOpenAction = QtWidgets.QAction(MainWindow)
        self.fileOpenAction.setObjectName("fileOpenAction")
        self.fileNewAction = QtWidgets.QAction(MainWindow)
        self.fileNewAction.setObjectName("fileNewAction")
        self.fileCloseAction = QtWidgets.QAction(MainWindow)
        self.fileCloseAction.setObjectName("fileCloseAction")
        self.fileSaveAction = QtWidgets.QAction(MainWindow)
        self.fileSaveAction.setObjectName("fileSaveAction")
        self.actionand = QtWidgets.QAction(MainWindow)
        self.actionand.setObjectName("actionand")
        self.actionor = QtWidgets.QAction(MainWindow)
        self.actionor.setObjectName("actionor")
        self.actionnot = QtWidgets.QAction(MainWindow)
        self.actionnot.setObjectName("actionnot")
        self.linearAction = QtWidgets.QAction(MainWindow)
        self.linearAction.setObjectName("linearAction")
        self.curveAction = QtWidgets.QAction(MainWindow)
        self.curveAction.setObjectName("curveAction")
        self.planeAction = QtWidgets.QAction(MainWindow)
        self.planeAction.setObjectName("planeAction")
        self.actioncuboid = QtWidgets.QAction(MainWindow)
        self.actioncuboid.setObjectName("actioncuboid")
        self.actioncylinder = QtWidgets.QAction(MainWindow)
        self.actioncylinder.setObjectName("actioncylinder")
        self.actionnull = QtWidgets.QAction(MainWindow)
        self.actionnull.setObjectName("actionnull")
        self.menu.addAction(self.fileOpenAction)
        self.menu.addAction(self.fileNewAction)
        self.menu.addAction(self.fileCloseAction)
        self.menu.addAction(self.fileSaveAction)
        self.menu_4.addAction(self.actioncuboid)
        self.menu_4.addAction(self.actioncylinder)
        self.menu_4.addAction(self.actionnull)
        self.menu_E.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_E.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "文件(&F)"))
        self.menu_E.setTitle(_translate("MainWindow", "编辑(&E)"))
        self.menu_4.setTitle(_translate("MainWindow", "立體圖形"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.fileOpenAction.setText(_translate("MainWindow", "打開"))
        self.fileOpenAction.setToolTip(_translate("MainWindow", "打開"))
        self.fileOpenAction.setShortcut(_translate("MainWindow", "Alt+O"))
        self.fileNewAction.setText(_translate("MainWindow", "新建"))
        self.fileNewAction.setShortcut(_translate("MainWindow", "Alt+N"))
        self.fileCloseAction.setText(_translate("MainWindow", "關閉"))
        self.fileCloseAction.setToolTip(_translate("MainWindow", "關閉"))
        self.fileCloseAction.setShortcut(_translate("MainWindow", "Alt+C"))
        self.fileSaveAction.setText(_translate("MainWindow", "儲存"))
        self.fileSaveAction.setToolTip(_translate("MainWindow", "儲存"))
        self.fileSaveAction.setShortcut(_translate("MainWindow", "Alt+S"))
        self.actionand.setText(_translate("MainWindow", "and"))
        self.actionor.setText(_translate("MainWindow", "or"))
        self.actionnot.setText(_translate("MainWindow", "not"))
        self.linearAction.setText(_translate("MainWindow", "直線"))
        self.linearAction.setToolTip(_translate("MainWindow", "直線"))
        self.curveAction.setText(_translate("MainWindow", "弧線"))
        self.curveAction.setToolTip(_translate("MainWindow", "弧線"))
        self.planeAction.setText(_translate("MainWindow", "平面圖形"))
        self.planeAction.setToolTip(_translate("MainWindow", "平面圖形"))
        self.actioncuboid.setText(_translate("MainWindow", "cuboid"))
        self.actioncylinder.setText(_translate("MainWindow", "cylinder"))
        self.actionnull.setText(_translate("MainWindow", "null"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())