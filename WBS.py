from wbs.core.gui import window
from wbs.view import MainWindow
from PyQt5 import QtWidgets
from wbs.core import *
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    w = MainWindow.Ui_MainWindow()
    w.setupUi(mw)

    win_msd = window.WinMsd(w, app)
    StaticArea.win_msd = win_msd
    # 初始化配置
    win_msd.init_window()

    # 启动扫描
    w.pushButton_start.clicked.connect(win_msd.push_start)

    # 暂停扫描
    w.pushButton_stop.clicked.connect(win_msd.push_stop)

    # 结束扫描
    w.pushButton_end.clicked.connect(win_msd.push_end)

    # 切换扫描速度
    w.comboBox_speed.currentIndexChanged.connect(win_msd.change_speed)

    mw.show()
    sys.exit(app.exec_())
