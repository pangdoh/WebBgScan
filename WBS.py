from core.gui import window
from core.utils import Logger
from view import MainWindow
from PyQt5 import QtWidgets
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    w = MainWindow.Ui_MainWindow()
    w.setupUi(mw)

    win_msd = window.WinMsd(w)
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
