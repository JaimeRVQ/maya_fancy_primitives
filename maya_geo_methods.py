# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: maya_geo_methods.py
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


from maya import cmds

def get_geometry(geo_type='sphere', sx=8, sy=8, sz=0):

    the_primitive = 'Fancy_geo_primitive'
    output_edges = []

    if geo_type == 'sphere':
         cmds.polySphere(name= the_primitive, sx=sx, sy=sy)
         cmds.rotate(10,0,20, the_primitive)

    elif geo_type == 'cube':
        cmds.polyCube(name=the_primitive,sx=sx, sy=sy, sz=sz)
        cmds.rotate(30, 0, 10, the_primitive)

    elif geo_type == 'cylinder':
        cmds.polyCylinder(name=the_primitive,sx=sx, sy=sy, sz=sz)
        cmds.rotate(10, 0, 20, the_primitive)

    elif geo_type == 'cone':
        cmds.polyCone(name=the_primitive,sx=sx, sy=sy, sz=sz)
        cmds.move(0, -0.2, 0, the_primitive)
        cmds.rotate(170, 0, 10, the_primitive)

    elif geo_type == 'torus':
         cmds.polyTorus(name= the_primitive, sx=sx, sy=sy)
         cmds.rotate(30,0,40, the_primitive)

    elif geo_type == 'plane':
         cmds.polyPlane(name= the_primitive, sx=sx, sy=sy)
         cmds.rotate(30,0,45, the_primitive)

    edge_count = cmds.polyEvaluate(the_primitive)['edge']
    for i in range(edge_count):
        all_edges = cmds.polyListComponentConversion('{0}.e[{1}]'.format(the_primitive, i), tv=True)
        edge_start_end = cmds.ls(all_edges, flatten=True)
        output_edges.append([cmds.pointPosition(edge_start_end[0]), cmds.pointPosition(edge_start_end[1])])

    cmds.delete(the_primitive)

    return output_edges


def create_geometry(geo_type, sx, sy, sz=0):

    if geo_type == 'sphere':
         cmds.polySphere(sx=sx, sy=sy)

    elif geo_type == 'cube':
        cmds.polyCube(sx=sx, sy=sy, sz=sz)

    elif geo_type == 'cylinder':
        cmds.polyCylinder(sx=sx, sy=sy, sz=sz)

    elif geo_type == 'cone':
        cmds.polyCone(sx=sx, sy=sy, sz=sz)

    elif geo_type == 'torus':
         cmds.polyTorus(sx=sx, sy=sy)

    elif geo_type == 'plane':
         cmds.polyPlane(sx=sx, sy=sy)