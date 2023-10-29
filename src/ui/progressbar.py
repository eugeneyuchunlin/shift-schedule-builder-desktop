import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QVBoxLayout, QWidget, QGraphicsLineItem
from PySide6.QtCore import QTimer, Qt, QObject, Signal, Slot
from PySide6.QtGui import QColor, QFont

class ProgressBar(QWidget, QObject):


    def __init__(self):
        print("Progess bar init")
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 150)
        layout = QVBoxLayout()

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.updateProgress)
        # self.timer.start(1000)  # 1-second interval

        self.state = 0

        self.circle_radius = 20
        self.circle_spacing = 100
        self.line_length = 60
        self.state_names = ["Received", "Compiling", "Solving", "Finished"]
        self.setLayout(layout)
        self.drawCirclesAndLines()

    def drawCirclesAndLines(self):
        self.scene.clear()

        for i in range(4):
            x = i * self.circle_spacing + self.circle_spacing / 2
            y = 75

            # Draw circle
            circle = QGraphicsEllipseItem(x - self.circle_radius, y - self.circle_radius, self.circle_radius * 2, self.circle_radius * 2)
            circle.setPen(QColor(0, 0, 0))
            if i >= self.state:
                circle.setBrush(Qt.NoBrush)  # Make the circle hollow
            else:
                circle.setBrush(QColor(0, 0, 0))
            self.scene.addItem(circle)

            # Add state name inside the circle
            text = QGraphicsTextItem(self.state_names[i])
            font = QFont()
            font.setPixelSize(12)
            text.setFont(font)
            text.setDefaultTextColor(QColor(0, 0, 0))
            text.setPos(x - self.circle_radius - 3, y - 2*self.circle_radius)
            self.scene.addItem(text)

            if i < 3:
                # Draw lines connecting circles outside of the circles
                line = QGraphicsLineItem(x + self.circle_radius, y, x + self.circle_radius + self.line_length, y)
                line.setPen(QColor(0, 0, 0))
                self.scene.addItem(line)

    def clearState(self):
        self.state = 0
        self.drawCirclesAndLines() 

    def updateProgress(self, state):
        print(state)
        if self.state <= 3:
            self.state += 1
        else:
            self.state = 0

        self.drawCirclesAndLines()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec_())
