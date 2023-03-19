import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from Data.FetchData import *
icon_size = 200


class button(QtWidgets.QPushButton):
    def __init__(self, id):
        super().__init__()
        self.setFixedSize(icon_size, icon_size)
        self.setStyleSheet("background-color: #444654; border-radius: 10px")
        pixmap = QtGui.QPixmap(dists[id]["icon"])
        # Connect the clicked signal to a function
        self.clicked.connect(lambda: self.updateDetails(pixmap, id))



        if pixmap:
            self.setIcon(pixmap)
            self.setIconSize(QtCore.QSize(icon_size, icon_size))
        else:
            self.setText(id)

    def updateDetails(self, pixmap, text):
        global selected
        if pixmap:
            pixmap = pixmap.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText(text)
        info.setText(f"name: {dists[text]['name']}\nstatus: {dists[text]['status']}\nid: {text}\n")
        if not selected:
            # set button labels
            start = QtWidgets.QPushButton("start distro")
            start.clicked.connect(lambda: print(widget.size()))
            delete = QtWidgets.QPushButton("remove distro")
            open = QtWidgets.QPushButton("open in terminal")
            button_list = (start, delete, open)
            for i in button_list:
                details_layout.addWidget(i)
            selected = True
class ScrollArea(QtWidgets.QScrollArea):
    def __init__(self, layout):
        super().__init__()
        self.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setLayout(layout)
        self.setWidget(scroll_widget)
        #scroll_widget.setStyleSheet("background-color: #444654")
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)


def clearLayout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        del item



class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #212121")
        main_layout = QtWidgets.QHBoxLayout(self)

        # Create a label with an image
        pixmap = QtGui.QPixmap().scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

        # Set the fixed size and size policy
        image_label.setMinimumSize(400, 300)
        image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # set text labels
        info.setText("")

        # Set the layouts and add the labels to it
        right_layout = QtWidgets.QWidget()
        right_layout.setStyleSheet("background-color: #444654")
        right_layout.setLayout(details_layout)
        right_layout.setMaximumWidth(400)

        details_layout.addWidget(image_label)
        details_layout.addWidget(info)

        self.left_layout = QtWidgets.QGridLayout()
        left_container = ScrollArea(self.left_layout)
        self.setMinimumSize(462+icon_size, 0)
        self.resize(1210, 600)

        # Adding the layouts to main layout
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_layout)
        self.left_layout.rowStretch(1)

        # Set alignment of main layout to top center
        details_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        left_container.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.resizeEvent = self.onResize



    def onResize(self, event):
        lst, lnum = [], 0
        wspace = int((self.width() - 440) / icon_size)
        r, c = 0, 0
        clearLayout(self.left_layout)

        for i in dists:  # rearranges icons
            lst.append(button(i))
            self.left_layout.addWidget(lst[lnum], r, c)
            lnum += 1
            if c < (wspace-1):
                c += 1
            else:
                r += 1
                c = 0
        new_butt = QtWidgets.QPushButton("+")
        new_butt.setFixedSize(icon_size, icon_size)
        new_butt.setStyleSheet("background-color: #444654; border-radius: 10px")
        new_butt.clicked.connect(lambda: print('new'))
        self.left_layout.addWidget(new_butt, r, c)

        '''print(self.width(), self.height())
        print('space=', wspace)'''




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    image_label = QtWidgets.QLabel()
    info = QtWidgets.QLabel()
    details_layout = QtWidgets.QVBoxLayout()
    widget = MainWidget()

    widget.show()
    sys.exit(app.exec())
