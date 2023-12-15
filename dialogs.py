from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class NoPatchSelectedDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.botao = QPushButton("Ok", self)
        self.botao.clicked.connect(self.exitDialog)

        self.label = QLabel("Nada selecionado")

        self.line = QLineEdit()

        self.grid = QGridLayout()

        self.grid.addWidget(self.label, 0, 0)
        self.grid.addWidget(self.botao, 1, 0)

        self.setLayout(self.grid)

        self.setWindowTitle("ERROR")
        self.setWindowModality(Qt.ApplicationModal)

    def exitDialog(self):
        self.close()


class CreateMeshDialog(QDialog):
    distance = 25

    def __init__(self):
        super().__init__()
        self.botaoPontos = QPushButton("Ok", self)
        self.botaoCancelar = QPushButton("Cancela", self)

        self.botaoCancelar.clicked.connect(self.exitDialog)
        self.botaoPontos.clicked.connect(self.validateDistance)

        self.label = QLabel(f"distancia entre pontos")

        self.line = QLineEdit()
        self.line.setText(f"25")

        self.grid = QGridLayout()

        self.grid.addWidget(self.label, 0, 0)
        self.grid.addWidget(self.line, 1, 0)
        self.grid.addWidget(self.botaoPontos, 3, 0)
        self.grid.addWidget(self.botaoCancelar, 4, 0)

        self.setLayout(self.grid)

        self.setWindowTitle("Create Mesh")
        self.setWindowModality(Qt.ApplicationModal)

    def exitDialog(self):
        self.distance = 0
        self.close()

    def setDistance(self):
        self.distance = int(self.line.text())

    def getDistance(self):
        return self.distance

    def validateDistance(self):
        distance = self.line.text()
        if distance.isdigit() and int(distance) >= 25:
            self.setDistance()
            self.close()
        else:
            self.errorLabel = QLabel(
                f"distancia invalida. precisa se maior que 25."
            )
            self.grid.addWidget(self.errorLabel, 2, 0)


class NoPointsSelectedDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.botao = QPushButton("Ok", self)
        self.botao.clicked.connect(self.exitDialog)

        self.label = QLabel("nenhum ponto selecionado")

        self.line = QLineEdit()

        self.grid = QGridLayout()

        self.grid.addWidget(self.label, 0, 0)
        self.grid.addWidget(self.botao, 1, 0)

        self.setLayout(self.grid)

        self.setWindowTitle("ERRO")
        self.setWindowModality(Qt.ApplicationModal)

    def exitDialog(self):
        self.close()


class AddInitialValuesDialog(QDialog):
    xValue = 0
    yValue = 0

    def __init__(self):
        super().__init__()
        self.botaoPontos = QPushButton("Ok", self)
        self.botaoCancelar = QPushButton("Cancela", self)

        self.botaoCancelar.clicked.connect(self.exitDialog)
        self.botaoPontos.clicked.connect(self.validateValue)

        self.xLabel = QLabel(f"Valor Inicial X")
        self.xLine = QLineEdit()
        self.xLine.setText("0")

        self.yLabel = QLabel(f"Valor Inicial Y")
        self.yLine = QLineEdit()
        self.yLine.setText("0")

        self.grid = QGridLayout()

        self.grid.addWidget(self.xLabel, 0, 0)
        self.grid.addWidget(self.xLine, 1, 0)
        self.grid.addWidget(self.yLabel, 2, 0)
        self.grid.addWidget(self.yLine, 3, 0)
        self.grid.addWidget(self.botaoPontos, 5, 0)
        self.grid.addWidget(self.botaoCancelar, 6, 0)

        self.setLayout(self.grid)

        self.setWindowTitle("Add Valores Iniciais")
        self.setWindowModality(Qt.ApplicationModal)

    def exitDialog(self):
        self.xValue = 0
        self.yValue = 0
        self.close()

    def setValue(self):
        self.xValue = float(self.xLine.text())
        self.yValue = float(self.yLine.text())

    def getValue(self):
        return [self.xValue, self.yValue]

    def validateValue(self):
        xValue = self.xLine.text()
        yValue = self.yLine.text()
        if xValue.isdigit() and yValue.isdigit():
            self.setValue()
            self.close()
        else:
            self.errorLabel = QLabel(
                f"Valores invalidos"
            )
            self.grid.addWidget(self.errorLabel, 4, 0)


class AddBoundaryValuesDialog(QDialog):
    xValue = 0
    yValue = 0

    def __init__(self):
        super().__init__()
        self.botaoPontos = QPushButton("Ok", self)
        self.botaoCancelar = QPushButton("Cancela", self)

        self.botaoCancelar.clicked.connect(self.exitDialog)
        self.botaoPontos.clicked.connect(self.validateValue)

        self.xLabel = QLabel(f"Valor limite X")
        self.xLine = QLineEdit()
        self.xLine.setText("0")

        self.yLabel = QLabel(f"Valor limite Y")
        self.yLine = QLineEdit()
        self.yLine.setText("0")

        self.grid = QGridLayout()

        self.grid.addWidget(self.xLabel, 0, 0)
        self.grid.addWidget(self.xLine, 1, 0)
        self.grid.addWidget(self.yLabel, 2, 0)
        self.grid.addWidget(self.yLine, 3, 0)
        self.grid.addWidget(self.botaoPontos, 5, 0)
        self.grid.addWidget(self.botaoCancelar, 6, 0)

        self.setLayout(self.grid)

        self.setWindowTitle("Add Valores Limites")
        self.setWindowModality(Qt.ApplicationModal)

    def exitDialog(self):
        self.xValue = 0
        self.yValue = 0
        self.close()

    def setValue(self):
        self.xValue = float(self.xLine.text())
        self.yValue = float(self.yLine.text())

    def getValue(self):
        return [self.xValue, self.yValue]

    def validateValue(self):
        xValue = self.xLine.text()
        yValue = self.yLine.text()
        if xValue.isdigit() and yValue.isdigit():
            self.setValue()
            self.close()
        else:
            self.errorLabel = QLabel(
                f"Valores invalidos"
            )
            self.grid.addWidget(self.errorLabel, 4, 0)
