import time
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtOpenGL, QtCore
from OpenGL.GL import *
from PyQt5.QtGui import *
from hetool.include.hetool import Hetool
from hetool.geometry.point import Point
from mymodel import AppCurveCollector


class AppCanvas(QtOpenGL.QGLWidget):
    mesh = None
    hetool_points = None

    def __init__(self, scale_factor=1.0):
        super(AppCanvas, self).__init__()
        self.m_w = 0
        self.m_h = 0
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.m_collector = AppCurveCollector()
        self.m_state = "View"
        self.m_mousePt = QtCore.QPointF(0.0, 0.0)
        self.m_heTol = 10.0
        self.m_scale_factor = scale_factor

    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)

    def resizeGL(self, _w, _h):
        self.m_w = _w
        self.m_h = _h

        if Hetool.isEmpty():
            self.scaleWorldWindow(1.0)
        else:
            self.fitWorldToViewport()

        glViewport(0, 0, _w, _h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glShadeModel(GL_SMOOTH)
        patches = Hetool.getPatches()
        for patch in patches:
            if patch.isDeleted:
                glColor3f(0.0, 0.0, 0.0)
            elif patch.isSelected():
                glColor3f(5.00, 0., 1.32)
            else:
                glColor3f(4.75, 0.65, 0.00)

            triangs = Hetool.tessellate(patch)
            for triangle in triangs:
                glBegin(GL_TRIANGLES)
                for pt in triangle:
                    glVertex2d(pt.getX(), pt.getY())
                glEnd()

        segments = Hetool.getSegments()
        for segment in segments:
            pts = segment.getPointsToDraw()
            if segment.isSelected():
                glColor3f(0.0, 5.0, 0.23)
            else:
                glColor3f(1.0, 0.0, 2.0)
            glBegin(GL_LINE_STRIP)
            for pt in pts:
                glVertex2f(pt.getX(), pt.getY())
            glEnd()

        points = Hetool.getPoints()
        for point in points:
            if point.isSelected():
                glColor3f(1.53, 5.23, 0.0)
            else:
                glColor3f(0.0, 6.74, 1.23)
            glPointSize(3)
            glBegin(GL_POINTS)
            glVertex2f(point.getX(), point.getY())
            glEnd()

        if self.m_collector.isActive():
            tempCurve = self.m_collector.getCurveToDraw()
            if len(tempCurve) > 0:
                glColor3f(1.35, 0.0, 6.23)
                glBegin(GL_LINE_STRIP)
                for pti in tempCurve:
                    glVertex2f(pti[0], pti[1])
                glEnd()

    def fitWorldToViewport(self):
        if Hetool.isEmpty():
            return

        self.m_L, self.m_R, self.m_B, self.m_T = Hetool.getBoundBox()
        self.scaleWorldWindow(1.1)

    def scaleWorldWindow(self, _scaleFactor):
        cx = 0.5 * (self.m_L + self.m_R)
        cy = 0.5 * (self.m_B + self.m_T)
        dx = (self.m_R - self.m_L) * _scaleFactor
        dy = (self.m_T - self.m_B) * _scaleFactor

        ratioVP = self.m_h / self.m_w
        if dy > dx * ratioVP:
            dx = dy / ratioVP
        else:
            dy = dx * ratioVP

        self.m_L = cx - 0.5 * dx
        self.m_R = cx + 0.5 * dx
        self.m_B = cy - 0.5 * dy
        self.m_T = cy + 0.5 * dy

        self.m_heTol = 0.005 * (dx + dy)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setState(self, _state, _varg="default"):
        self.m_collector.deactivateCollector()
        if _state == "Select":
            self.m_state = "Select"
        elif _state == "SelectMultiple":
            self.m_state = "SelectMultiple"
        elif _state == "View":
            self.m_state = "View"
            Hetool.unSelectAll()
        elif _state == "Collect":
            self.m_state = "Collect"
            self.m_collector.activateCollector(_varg)
        elif _state == "CreateMesh":
            self.m_state = "CreateMesh"
            patch = Hetool.getSelectedPatches()[0]
            self.createMesh(patch, _varg)
        elif _state == "ExportMesh":
            self.m_state = "ExportMesh"
            self.exportMesh()
        else:
            self.m_state = "View"

    def mouseMoveEvent(self, _event):
        pt = _event.pos()
        self.m_mousePt = pt

        if self.m_collector.isActive():
            pt = self.convertPtCoordsToUniverse(pt)
            self.m_collector.update(pt.x(), pt.y())
            self.update()

    def mouseReleaseEvent(self, _event):
        pt = _event.pos()
        if self.m_collector.isActive():
            pt_univ = self.convertPtCoordsToUniverse(pt)
            snaped, xs, ys = Hetool.snapToPoint(pt_univ.x(), pt_univ.y(), self.m_heTol)
            if snaped:
                isComplete = self.m_collector.collectPoint(xs, ys)
            else:
                snaped, xs, ys = Hetool.snapToSegment(
                    pt_univ.x(), pt_univ.y(), self.m_heTol
                )
                if snaped:
                    isComplete = self.m_collector.collectPoint(xs, ys)
                else:
                    isComplete = self.m_collector.collectPoint(pt_univ.x(), pt_univ.y())

            if isComplete:
                self.setMouseTracking(False)
                curve = self.m_collector.getCurve()
                heSegment = []
                for pt in curve:
                    heSegment.append(pt[0])
                    heSegment.append(pt[1])
                Hetool.insertSegment(heSegment)
                self.update()
            else:
                self.setMouseTracking(True)

        if self.m_state == "Select":
            pt_univ = self.convertPtCoordsToUniverse(pt)
            Hetool.selectPick(pt_univ.x(), pt_univ.y(), self.m_heTol)
            self.update()

        if self.m_state == "SelectMultiple":
            pt_univ = self.convertPtCoordsToUniverse(pt)
            Hetool.selectPick(pt_univ.x(), pt_univ.y(), self.m_heTol, True)
            self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scaleWorldWindow(0.9)
        else:
            self.scaleWorldWindow(1.1)
        self.update()

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * self.m_scale_factor * dX / self.m_w
        mY = (self.m_h - _pt.y() * self.m_scale_factor) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x, y)

    # Create Mesh
    def createMesh(self, _patch, _distance):
        # Get the bounding box of the selected patch
        xMin, xMax, yMin, yMax = _patch.getBoundBox()

        # Print the bounding box
        print("Bounding Box: ", xMin, xMax, yMin, yMax)
        print("Distance Between Points: ", _distance)

        # Get all points inside the bounding box
        all_points = []
        for x in range(int(xMin), int(xMax), int(_distance)):
            for y in range(int(yMin), int(yMax), int(_distance)):
                all_points.append([x, y])

        # Get all points inside the patch
        mesh_coords = []
        hetool_points = []

        for point in all_points:
            hetool_point = Point(point[0], point[1])
            if _patch.isPointInside(hetool_point):
                mesh_coords.append(point)
                hetool_points.append(hetool_point)
                Hetool.insertPoint(hetool_point)

        # Calculate adjacent points for each point and save them to the mesh_connect array identifying by the point index
        mesh_connect = []

        for point in mesh_coords:
            adjacent_points = []
            for i in range(0, len(mesh_coords)):
                if i != mesh_coords.index(point):
                    if (
                        abs(point[0] - mesh_coords[i][0]) <= _distance
                        and abs(point[1] - mesh_coords[i][1]) <= _distance
                    ):
                        adjacent_points.append(i)
            mesh_connect.append([len(adjacent_points), *adjacent_points])

        # Export the mesh
        mesh_export = {
            "coords": mesh_coords,
            "connect": mesh_connect,
        }

        # Save mesh to canvas
        self.mesh = mesh_export
        self.hetool_points = hetool_points

    def exportMesh(self):
        if self.mesh and self.hetool_points:
            initial_values = []
            boundary_values = []

            for point in self.hetool_points:
                if not len(point.attributes):
                    initial_values.append([0, 0])
                    boundary_values.append([0, 0])

                for attribute in point.attributes:
                    if attribute[0] == "Initial Value":
                        initial_values.append(attribute[1])
                    else:
                        initial_values.append([0, 0])

                    if attribute[0] == "Boundary Value":
                        boundary_values.append(attribute[1])
                    else:
                        boundary_values.append([0, 0])

            mesh_export = {
                "coords": self.mesh["coords"],
                "connect": self.mesh["connect"],
                "initial_values": initial_values,
                "boundary_values": boundary_values,
            }

            # Export the mesh
            with open(f"export/export_{time.strftime()}.json", "w") as outfile:
                json.dump(mesh_export, outfile)
