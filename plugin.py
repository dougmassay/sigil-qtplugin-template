import os
import sys

# Import top level Qt Modules, as needed, from plugin_utils to automatically handle Qt5 vs Qt6
from plugin_utils import QtCore, QtWidgets  # , QtGui, QtNetwork, QtPrintSupport, QtSvg, QtWebChannel
# from plugin_utils import QtWebEngineCore, QtWebEngineWidgets
# Special case imports to handle discrepancies between Qt5 and Qt6
from plugin_utils import Qt  # , QAction, loadUi, Slot, Signal
# Subclassed QApplication to make many tedious tasks easier
from plugin_utils import PluginApplication
# Utilities from plugin_utils
from plugin_utils import iswindows  # , ismacos, qVersion
from plugin_utils import _t  # Alias to QtCore.QCoreApplication.translate to wrap text to be translated


# Subclass QMainWindw to customize your plugin's main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_t('MainWindow', 'My Template'))
        # Get plugin bk object and any preferences
        app = PluginApplication.instance()
        self.bk = app.bk
        self.prefs = app.bk.getPrefs()
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        lbl_desc = QtWidgets.QLabel()
        lbl_desc.setText(_t('MainWindow', 'Example Label'))
        lbl_desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_desc)

        button = QtWidgets.QPushButton(_t('MainWindow', 'Press Me'))
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        layout.addWidget(button)

        # try to get previous window geometry from plugin prefernces
        if 'windowGeometry' in self.prefs and self.prefs['windowGeometry'] is not None:
            try:
                self.restoreGeometry(QtCore.QByteArray.fromHex(self.prefs['windowGeometry'].encode('ascii')))
            except Exception:
                pass
        self.show()

    def the_button_was_clicked(self):
        print(_t('MainWindow', 'Clicked!'))

    def closeEvent(self, event):
        # Save current window geometry to plugin prefernces
        self.prefs['windowGeometry'] = self.saveGeometry().toHex().data().decode('ascii')
        self.bk.savePrefs(self.prefs)
        event.accept()  # let the window close

def run(bk):
    # Path to icon to be used for all application Windows
    icon = os.path.join(bk._w.plugin_dir, bk._w.plugin_name, 'plugin.png')
    # Platforms other than Windows will typically already match darkmode
    mdp = True if iswindows else False
    app = PluginApplication(sys.argv, bk, app_icon=icon, match_dark_palette=mdp)
    window = MainWindow()  # noqa: F841
    app.exec()

    return 0

def main():
    return -1
