# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: primitives_window.py
Date: 2019.02.09
Revision: 2019.02.09
Copyright: Copyright Jaime Rivera 2019 | www.jaimervq.com
           The program(s) herein may be used, modified and/or distributed in accordance with the terms and conditions
           stipulated in the Creative Commons license under which the program(s) have been registered. (CC BY-SA 4.0)

Brief:

'''

__author__ = 'Jaime Rivera <jaime.rvq@gmail.com>'
__copyright__ = 'Copyright 2019, Jaime Rivera'
__credits__ = []
__license__ = 'Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)'
__maintainer__ = 'Jaime Rivera'
__email__ = 'jaime.rvq@gmail.com'
__status__ = 'Testing'


from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
import os
import math
import random
import time

import maya_geo_methods

class GeosGraphicsScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.primitive = maya_geo_methods.get_geometry()

        timer = QtCore.QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.draw_geometry)
        timer.start()

        self.projection_distance = -950
        self.angular_rot_increment = (7 * math.radians(360) / 60.0)  * (20.0/1000.0)
        self.geo_rotation = 0

        self.draw_geometry()

    def draw_geometry(self):

        self.clear()

        self.geo_rotation += self.angular_rot_increment
        self.geo_rotation = 0 if math.degrees(self.geo_rotation) >= 360 else self.geo_rotation

        # 3D transformation
        for edge in self.primitive:

            x1 = edge[0][0]
            y1 = edge[0][1]
            z1 = edge[0][2]

            transformed_x1 = z1 * math.sin(self.geo_rotation) + x1 * math.cos(self.geo_rotation)
            transformed_y1 = y1
            transformed_z1 = z1 * math.cos(self.geo_rotation) - x1 * math.sin(self.geo_rotation)- 10

            x1_flat = (self.projection_distance / transformed_z1) * transformed_x1
            y1_flat = (self.projection_distance / transformed_z1) * transformed_y1

            # ------------------------------------------------------------------------------------

            x2 = edge[1][0]
            y2 = edge[1][1]
            z2 = edge[1][2]

            transformed_x2 = z2 * math.sin(self.geo_rotation) + x2 * math.cos(self.geo_rotation)
            transformed_y2 = y2
            transformed_z2 = z2 * math.cos(self.geo_rotation) - x2 * math.sin(self.geo_rotation)- 10

            x2_flat = (self.projection_distance / transformed_z2) * transformed_x2
            y2_flat = (self.projection_distance / transformed_z2) * transformed_y2

            # ------------------------------------------------------------------------------------

            self.addLine(QtCore.QLineF(x1_flat, y1_flat, x2_flat, y2_flat), QtGui.QPen(QtCore.Qt.green, 0.6))

    def change_primitive(self, primitive, sx, sy, sz=0):

        if primitive == 'sphere':
            self.projection_distance = -950
        elif primitive == 'cube':
            self.projection_distance = -1200
        elif primitive == 'cylinder':
            self.projection_distance = -700
        elif primitive == 'cone':
            self.projection_distance = -820
        elif primitive == 'torus':
            self.projection_distance = -720
        elif primitive == 'plane':
            self.projection_distance = -1500

        self.primitive = maya_geo_methods.get_geometry(primitive, sx, sy, sz)

    def update_speed(self, new_rpm):
        self.angular_rot_increment = (new_rpm * math.radians(360) / 60.0)  * (20.0/1000.0)


class FancyPrimitivesCreator(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path).replace('\\', '/')
        file = QtCore.QFile(dir_path+'/fancy_primitives.ui')
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        loader.load(file,self)

        # MAIN CONFIG OF THE WINDOW
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setWindowTitle('Fancy primitives')
        self.setFixedSize(271,531)

        # ICONS
        self.polySphere_icon = QtGui.QIcon(':/polySphere.png')
        self.polyCube_icon = QtGui.QIcon(':/polyCube.png')
        self.polyCylinder_icon = QtGui.QIcon(':/polyCylinder.png')
        self.polyCone_icon = QtGui.QIcon(':/polyCone.png')
        self.polyTorus_icon = QtGui.QIcon(':/polyTorus.png')
        self.polyPlane_icon = QtGui.QIcon(':/polyMesh.png')

        # ELEMENTS
        self.geo_option = self.findChild(QtWidgets.QComboBox, 'geo_option')

        self.rpm_slider = self.findChild(QtWidgets.QSlider, 'rpm_slider')

        self.grid_ly = self.findChild(QtWidgets.QGridLayout, 'grid_ly')
        self.sx = self.findChild(QtWidgets.QSpinBox, 'sx')
        self.sx_label = self.findChild(QtWidgets.QLabel, 'sx_label')
        self.sy = self.findChild(QtWidgets.QSpinBox, 'sy')
        self.sy_label = self.findChild(QtWidgets.QLabel, 'sy_label')
        self.sz = self.findChild(QtWidgets.QSpinBox, 'sz')
        self.sz_label = self.findChild(QtWidgets.QLabel, 'sz_label')

        self.create_btn = self.findChild(QtWidgets.QPushButton, 'create_btn')

        # Graphics scene
        self.scene = GeosGraphicsScene(parent=self)
        self.gw = self.findChild(QtWidgets.QGraphicsView, 'gw')
        self.gw.setScene(self.scene)


        self.setup_style()
        self.make_connections()
        self.show()

    def setup_style(self):
        self.geo_option.setItemIcon(0, self.polySphere_icon)
        self.geo_option.setItemIcon(1, self.polyCube_icon)
        self.geo_option.setItemIcon(2, self.polyCylinder_icon)
        self.geo_option.setItemIcon(3, self.polyCone_icon)
        self.geo_option.setItemIcon(4, self.polyTorus_icon)
        self.geo_option.setItemIcon(5, self.polyPlane_icon)


        self.grid_ly.setColumnMinimumWidth(0,170)

        self.sz.setStyleSheet('background:rgba(0,0,0,0); color:rgba(0,0,0,0)')

    def make_connections(self):
        self.rpm_slider.valueChanged.connect(lambda: self.scene.update_speed(self.rpm_slider.value()))
        self.geo_option.currentIndexChanged.connect(self.change_geo_type)

        self.sx.valueChanged.connect(self.update_geo)
        self.sy.valueChanged.connect(self.update_geo)
        self.sz.valueChanged.connect(self.update_geo)

        self.create_btn.clicked.connect(self.generate_geo)

    def change_geo_type(self, index):

        self.rpm_slider.setValue(7)

        if index == 0:
            self.sx.setMinimum(3)
            self.sx.setValue(8)
            self.sx_label.setText('Axis subdivisions')
            self.sy.setMinimum(3)
            self.sy.setValue(8)
            self.sz.setMinimum(0)
            self.sz.setValue(0)
            self.sz.setDisabled(True)
            self.sz.setStyleSheet('background:rgba(0,0,0,0); color:rgba(0,0,0,0)')
            self.sz_label.setText('')
            self.scene.change_primitive('sphere', 8, 8)

        if index == 1:
            self.sx.setMinimum(1)
            self.sx.setValue(1)
            self.sx_label.setText('Width subdivisions')
            self.sy.setMinimum(1)
            self.sy.setValue(1)
            self.sz.setValue(1)
            self.sz.setEnabled(True)
            self.sz.setStyleSheet('')
            self.sz_label.setText('Depth subdivisions')
            self.scene.change_primitive('cube', 1, 1)

        if index == 2:
            self.sx.setMinimum(3)
            self.sx.setValue(8)
            self.sx_label.setText('Axis subdivisions')
            self.sy.setMinimum(1)
            self.sy.setValue(1)
            self.sz.setMinimum(0)
            self.sz.setValue(0)
            self.sz.setEnabled(True)
            self.sz.setStyleSheet('')
            self.sz_label.setText('Cap subdivisions')
            self.scene.change_primitive('cylinder', 8, 1, 0)

        if index == 3:
            self.sx.setMinimum(3)
            self.sx.setValue(8)
            self.sx_label.setText('Axis subdivisions')
            self.sy.setMinimum(1)
            self.sy.setValue(1)
            self.sz.setMinimum(0)
            self.sz.setValue(0)
            self.sz.setEnabled(True)
            self.sz.setStyleSheet('')
            self.sz_label.setText('Cap subdivisions')
            self.scene.change_primitive('cone', 8, 1, 0)

        if index == 4:
            self.sx.setMinimum(3)
            self.sx.setValue(8)
            self.sx_label.setText('Axis subdivisions')
            self.sy.setMinimum(3)
            self.sy.setValue(8)
            self.sz.setMinimum(0)
            self.sz.setValue(0)
            self.sz.setDisabled(True)
            self.sz.setStyleSheet('background:rgba(0,0,0,0); color:rgba(0,0,0,0)')
            self.sz_label.setText('')
            self.scene.change_primitive('torus', 8, 8)

        if index == 5:
            self.sx.setMinimum(1)
            self.sx.setValue(1)
            self.sx_label.setText('Width subdivisions')
            self.sy.setMinimum(1)
            self.sy.setValue(1)
            self.sz.setMinimum(0)
            self.sz.setValue(0)
            self.sz.setDisabled(True)
            self.sz.setStyleSheet('background:rgba(0,0,0,0); color:rgba(0,0,0,0)')
            self.sz_label.setText('')
            self.scene.change_primitive('plane', 1, 1)


    def update_geo(self):
        self.scene.change_primitive(self.geo_option.currentText().lower(), self.sx.value(), self.sy.value(), self.sz.value())

    def generate_geo(self):
        maya_geo_methods.create_geometry(self.geo_option.currentText().lower(), self.sx.value(), self.sy.value(), self.sz.value())

