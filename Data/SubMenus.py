import sys
import threading
try:
    from PySide6.QtGui import QPalette, QColor
    from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QPushButton, QLineEdit
    from Data.FetchData import dists
    from PySide6 import QtWidgets, QtGui, QtCore
    from PySide6.QtCore import Qt
except ModuleNotFoundError:
    print("\nPySide6 Module not found\nInstall Pyside6 with 'pip install PySide6'\n")
    sys.exit()
app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("Data/icon.ico"))


def EmptyWinIcon(self):
    self.setWindowIcon(QtGui.QIcon(''))


class Dialog(QDialog):
    def __init__(self, text='this is a dialog', option=0, title=''):
        super().__init__()
        self.setStyleSheet("background-color: #212121; color: white")
        EmptyWinIcon(self)
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)
        if option:
            QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)
        elif option == 2:
            pass
        else:
            self.buttonBox = QPushButton("OK")
            self.buttonBox.clicked.connect(self.accept)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


class NewDialog(QDialog):
    def __init__(self):
        super().__init__()
        EmptyWinIcon(self)
        self.setStyleSheet("background-color: #212121; color: white")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add first text input field
        name = QLabel("container name:")
        layout.addWidget(name)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        self.name_check = QLabel()
        self.name_check.setMaximumHeight(0)
        layout.addWidget(self.name_check)

        # Add second text input field
        distro = QLabel("distro(optional):")
        layout.addWidget(distro)
        self.distro_input = QLineEdit()
        layout.addWidget(self.distro_input)

        # Add third text input field
        version = QLabel("version(optional):")
        layout.addWidget(version)
        self.version_input = QLineEdit()
        layout.addWidget(self.version_input)

        # Add OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.check(self.name_input.text()))
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "distro": self.distro_input.text(),
            "version": self.version_input.text(),
        }

    def check(self, name='new_container'):
        duplicate = False
        if name == '':
            name = 'new_container'
        for i in dists:
            if dists[i]["name"].strip() == name.strip():
                duplicate = True
                self.name_check.setText(f"{name} already exists")
                self.name_check.setMaximumHeight(self.height())
                palette = self.name_check.palette()
                palette.setColor(QPalette.WindowText, Qt.red)
                self.name_check.setPalette(palette)
                break
        if not duplicate:
            self.accept()


class DistroboxNotDetectedWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        EmptyWinIcon(self)
        self.setStyleSheet("background-color: #212121; color: white")
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        label = QLabel("             Could not detect Distrobox installation.\n"
                       "Refer to Distrobox official github page for install guide:", self)
        link = QLabel('<a href="https://github.com/89luca89/distrobox#readme">https://github.com/89luca89/distrobox</a>'
                      , self)
        link.setOpenExternalLinks(True)
        link.setTextFormat(Qt.RichText)
        palette = QPalette()
        palette.setColor(QPalette.Link, QColor('#0083ff'))
        link.setAlignment(Qt.AlignCenter)
        button = QPushButton("OK", self)
        button.clicked.connect(self.close)
        main_layout.addWidget(label)
        main_layout.addWidget(link)
        main_layout.addWidget(button)
