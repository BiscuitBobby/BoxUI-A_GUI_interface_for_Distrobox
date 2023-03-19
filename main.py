import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from Data.FetchData import *


class button(QtWidgets.QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setFixedSize(250, 250)
        pixmap = QtGui.QPixmap(dists[text]["icon"])
        self.setStyleSheet("background-color: #999999; border-radius: 10px")

        # Connect the clicked signal to a slot (function)
        self.clicked.connect(lambda: print(text))
        if pixmap:
            self.setIcon(pixmap)
            self.setIconSize(QtCore.QSize(250, 250))
        else:
            self.setText(text)
class ScrollArea(QtWidgets.QScrollArea):
    def __init__(self, layout):
        super().__init__()
        self.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setLayout(layout)
        self.setWidget(scroll_widget)
        #scroll_widget.setStyleSheet("background-color: #444654")
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #212121")
        main_layout = QtWidgets.QHBoxLayout(self)

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
        self.start.clicked.connect(lambda: print(widget.size()))
        self.delete = QtWidgets.QPushButton("remove distro")
        self.open = QtWidgets.QPushButton("open in terminal")
        button_list = (self.start, self.delete, self.open)

        # Set the layouts and add the labels to it
        details_layout = QtWidgets.QVBoxLayout()
        right_layout = QtWidgets.QWidget()
        right_layout.setStyleSheet("background-color: #444654")
        right_layout.setLayout(details_layout)

        details_layout.addWidget(self.image_label)
        details_layout.addWidget(self.info)
        for i in button_list:
            details_layout.addWidget(i)

        self.left_layout = QtWidgets.QGridLayout()
        left_container = ScrollArea(self.left_layout)
        self.setMinimumSize(1000, 600)
        self.setBaseSize(1025, 800)

        # Adding the layouts to main layout
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_layout)
        self.left_layout.rowStretch(1)

        # Set alignment of main layout to top center
        details_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        left_container.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.resizeEvent = self.onResize

        right_layout.setMaximumWidth(400)

    def onResize(self, event):
        lst = []
        lnum = 0
        wspace = int((self.width() - 440) / 250)
        r = 1
        c = 1
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            del item

        for i in (dists):
            lst.append(button(i))
            # button(i).clicked.connect(lambda: self.image_label.setPixmap(icons((i.split(':'))[0])).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.left_layout.addWidget(lst[lnum], r, c)
            lnum += 1
            if c < wspace:
                c += 1
            else:
                r += 1

        print(self.width(), self.height())
        print('space=', wspace)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())
