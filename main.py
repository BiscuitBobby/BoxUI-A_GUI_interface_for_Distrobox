import sys
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #212121")
        layout = QtWidgets.QHBoxLayout(self)
        # Create a label with an image
        self.image_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("debian.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

        # Set the fixed size and size policy
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # set text labels
        self.info = QtWidgets.QLabel(self)
        self.info.setText("name: distro_name\nstatus: status\nid: id\nimage: image")

        # set button labels
        self.start = QtWidgets.QPushButton("start distro")
        self.delete = QtWidgets.QPushButton("remove distro")
        self.open = QtWidgets.QPushButton("open in terminal")
        button_list = (self.start, self.delete, self.open)

        # Set the layouts and add the labels to it
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.image_label)
        right_layout.addWidget(self.info)
        for i in button_list:
            right_layout.addWidget(i)

        # Adding the layouts to main layout
        layout.addLayout(right_layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())
