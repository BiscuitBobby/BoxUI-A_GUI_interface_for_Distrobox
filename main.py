from Data.processes import *
icon_size = 200
details_font_size = int(icon_size/13.333333333)


def CheckIfUp(stop_button):
    if not ("Up " in info.text()):
        stop_button.setEnabled(False)
        stop_button.setStyleSheet("color: grey")
    else:
        stop_button.setEnabled(True)
        stop_button.setStyleSheet("color: white")


class button(QtWidgets.QPushButton):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.setFixedSize(icon_size, icon_size)
        self.setStyleSheet("background-color: #444654; border-radius: 10px")
        try:
            pixmap = QtGui.QPixmap(dists[id]["icon"])
        except TypeError:
            pixmap = QtGui.QPixmap('')
        # Connect the clicked signal to a function
        self.clicked.connect(lambda: self.updateDetails(id, pixmap))

        if pixmap:
            self.setIcon(pixmap)
            self.setIconSize(QtCore.QSize(icon_size, icon_size))
        else:
            self.setText(id)

    def updateDetails(self, id, pixmap):
        global button_list
        #print(f'\n\n{dists}')
        if pixmap:
            pixmap = pixmap.scaled(icon_size+140, icon_size+140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            try:
                image_label.setText(dists["name"])
            except:
                image_label.setText("cannot retrieve image")
        self.update_info(id)
        name = dists[id]['name']
        for i in button_list:
            i.deleteLater()
        stop = QtWidgets.QPushButton("stop distro")
        CheckIfUp(stop)
        open = QtWidgets.QPushButton("open in terminal")
        delete = QtWidgets.QPushButton("remove distro")
        button_list = (open, stop, delete)

        stop.clicked.connect(lambda: stop_distro(name))
        open.clicked.connect(lambda: enter_distro(name))  # Pass the name parameter to the clicked signal
        delete.clicked.connect(lambda: remove_distro(name, id))
        for i in button_list:
            i.clicked.connect(lambda: self.update_info(id))
            details_layout.addWidget(i)
            i.setFont(QtGui.QFont("Arial", details_font_size))

    def update_info(self, id):
        global dists
        dists = DistroList()
        try:
            info.setText(
                f"Name: {dists[id]['name']}\nDistro:{dists[id]['distro']}\nStatus: {dists[id]['status']}\nID: {id}\n")
            info.setFont(QtGui.QFont("Arial", details_font_size))
            CheckIfUp(button_list[1])

        except:
            info.setText("[Deleted]\n")
            self.deleteLater()
            for i in button_list:
                i.setEnabled(False)
                i.setStyleSheet("color: grey")
                UpdateGrid(widget)



class ScrollArea(QtWidgets.QScrollArea):
    def __init__(self, layout):
        super().__init__()
        self.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setLayout(layout)
        self.setWidget(scroll_widget)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)


def clearLayout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        del item


def create_update(self):
    thread = create_distro()
    try:
        #crt_diag = Dialog('creating new container', 2)
        thread.join()
    except AttributeError:
        pass
    UpdateGrid(self)


def UpdateGrid(self):
    global dists
    dists = DistroList()
    lst, lnum = [], 0
    wspace = int((self.width() - 440) / icon_size)
    r, c = 0, 0
    clearLayout(self.left_layout)

    for i in dists:  # rearranges icons
        lst.append(button(i))
        self.left_layout.addWidget(lst[lnum], r, c)
        lnum += 1
        if c < (wspace - 1):
            c += 1
        else:
            r += 1
            c = 0
    new_butt = QtWidgets.QPushButton("+")
    new_butt.setFixedSize(icon_size, icon_size)
    new_butt.setStyleSheet("background-color: #444654; border-radius: 10px")
    new_butt.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
    new_butt.clicked.connect(lambda: create_update(self))
    self.left_layout.addWidget(new_butt, r, c)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Box UI")
        EmptyWinIcon(self)

        self.setStyleSheet("background-color: #212121; color: white")
        main_layout = QtWidgets.QHBoxLayout(self)

        # Create a label with an image
        pixmap = QtGui.QPixmap().scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

        # Set the fixed size and size policy
        image_label.setMinimumSize(icon_size+160, 300)
        image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # set text labels
        info.setText("")

        # Set the layouts and add the labels to it
        right_layout = QtWidgets.QWidget()
        right_layout.setStyleSheet("background-color: #444654")
        right_layout.setLayout(details_layout)
        right_layout.setMaximumWidth(icon_size+160)
        details_layout.addWidget(image_label)
        details_layout.addWidget(info)

        self.left_layout = QtWidgets.QGridLayout()
        left_container = ScrollArea(self.left_layout)
        self.setMinimumSize(462+icon_size, icon_size+412)
        self.resize(1240, self.height())

        # Adding the layouts to main layout
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_layout)
        self.left_layout.rowStretch(1)

        # Set alignment of main layout to top center
        details_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        left_container.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.resizeEvent = self.OnResize

    def OnResize(self, event):
        UpdateGrid(self)


if __name__ == "__main__":
    if InitialCheck():
        image_label = QtWidgets.QLabel()
        info = QtWidgets.QLabel()
        stop = QtWidgets.QPushButton("stop distro")
        open = QtWidgets.QPushButton("open in terminal")
        delete = QtWidgets.QPushButton("remove distro")
        button_list = (open, stop, delete)
        details_layout = QtWidgets.QVBoxLayout()

        widget = MainWidget()
    else:
        widget = DistroboxNotDetectedWidget()
    widget.show()
    sys.exit(app.exec())