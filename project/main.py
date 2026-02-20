# from core.logging_system import SystemLogger
# from core.port_scanner import PortScanner
# from utils.encryptor import EncryptDecryptData
# from os import path


# encryptor = EncryptDecryptData()
# port = PortScanner('listen').connections
# encrypted_data = encryptor.encrypt(port)
# SystemLogger('info', 'for test', encrypted_data)
# print(encrypted_data)


# pathss = path.join(path.dirname(__file__), 'reports', 'logs', '2026-02-18', '17-06-13_1.log')
# decrypted_data = encryptor.decrypt(pathss)
# print(decrypted_data)

###########################

import sys
import os
from PySide6.QtWidgets import (QApplication,QMainWindow,QSizeGrip,
                               QTableWidgetItem,QVBoxLayout,
                               QWidget,QCompleter)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import (QFile,QPropertyAnimation,
                            QEasingCurve,QCoreApplication,
                            QSequentialAnimationGroup,
                            QRect,QTimer,Qt)
from PySide6.QtGui import QIcon,QPainter,QBrush,QColor,QPen
from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis)
from ui.specterUI import Ui_MainWindow
from theme.style import UI_STYLE
from utils.movable_window import frameMouseMoveEvent, frameMousePressEvent, frameMouseReleaseEvent



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #- Load UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #- hide main border -#
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #- style -#
        self.ui.main_frame.setStyleSheet(UI_STYLE['mainFrame'])
        self.ui.child_main_frame.setStyleSheet(UI_STYLE['childMainFrame'])

        #- movable window -#
        try:
            self.ui.main_frame.mousePressEvent = lambda event: frameMousePressEvent(self, event)
            self.ui.main_frame.mouseMoveEvent = lambda event: frameMouseMoveEvent(self, event)
            self.ui.main_frame.mouseReleaseEvent = lambda event: frameMouseReleaseEvent(self, event)
        except Exception:
            print('=> movable functions ERROR')





#--------------- run app ---------------#
if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
