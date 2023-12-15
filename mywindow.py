from PyQt5.QtWidgets import *
from OpenGL.GL import *
from PyQt5.QtGui import *
from hetool.include.hetool import Hetool
from trabProgCien.mycanvas import AppCanvas
from dialogs import *


class AppWindow(QMainWindow):
    def __init__(self, scale_factor=1.0):
        super(AppWindow, self).__init__()
        self.setGeometry(150, 100, 600, 400)
        self.setWindowTitle("MyGLDrawer")
        self.m_canvas = AppCanvas(scale_factor=scale_factor)
        self.setCentralWidget(self.m_canvas)

        tb = self.addToolBar("ToolBar")

        select = QAction("Select", self)
        tb.addAction(select)

        selectMultiple = QAction("Select Varios", self)
        tb.addAction(selectMultiple)

        addLine = QAction("Line", self)
        tb.addAction(addLine)

        addBezier2 = QAction("Bezier", self)
        tb.addAction(addBezier2)

        addRectangular = QAction("Retangulo", self)
        tb.addAction(addRectangular)

        createMesh = QAction("Criar Mesh", self)
        tb.addAction(createMesh)

        addBoundaryValues = QAction("Add Valores Limites", self)
        tb.addAction(addBoundaryValues)

        addInitialValues = QAction("Add Valores Iniciais", self)
        tb.addAction(addInitialValues)

        exportMesh = QAction("Export Mesh", self)
        tb.addAction(exportMesh)

        fit = QAction("Fit View", self)
        tb.addAction(fit)

        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self, _action):
        if _action.text() == "Select":
            self.m_canvas.setState("Select")

        elif _action.text() == "Select Multiple":
            self.m_canvas.setState("SelectMultiple")

        elif _action.text() == "Line":
            self.m_canvas.setState("Collect", "Line")

        elif _action.text() == "Bezier":
            self.m_canvas.setState("Collect", "Bezier2")

        elif _action.text() == "Retangulo":
            self.m_canvas.setState("Collect", "Rectangular")

        elif _action.text() == "Create Mesh":
            if len(Hetool.getSelectedPatches()) == 0:
                NoPatchSelectedDialog().exec_()
            else:
                dialog = CreateMeshDialog()
                dialog.exec_()
                distance = dialog.getDistance()

                if distance >= 25:
                    self.m_canvas.setState("CreateMesh", distance)

        elif _action.text() == "Add Valores Limites":
            selected_points = Hetool.getSelectedPoints()
            if len(selected_points) == 0:
                NoPointsSelectedDialog().exec_()
            else:
                dialog = AddBoundaryValuesDialog()
                dialog.exec_()
                value = dialog.getValue()
                if value != 0:
                    for point in selected_points:
                        point.attributes.append(["Boundary Value", value])
                    Hetool.unSelectAll()
                    self.m_canvas.update()

        elif _action.text() == "Add Valores Iniciais":
            selected_points = Hetool.getSelectedPoints()
            if len(selected_points) == 0:
                NoPointsSelectedDialog().exec_()
            else:
                dialog = AddInitialValuesDialog()
                dialog.exec_()
                value = dialog.getValue()
                if value != 0:
                    for point in selected_points:
                        point.attributes.append(["Initial Value", value])
                    Hetool.unSelectAll()
                    self.m_canvas.update()

        elif _action.text() == "Export Mesh":
            self.m_canvas.setState("ExportMesh")

        elif _action.text() == "Fit View":
            self.m_canvas.fitWorldToViewport()
            self.m_canvas.update()
