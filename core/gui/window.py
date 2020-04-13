from core.utils import Logger
from core import *
from core import startserver
from PyQt5 import QtCore
import os


class WinMsd:
    def __init__(self, w, app):
        self.w = w
        self.app = app
        self.res_num = 0
        self.start = False
        self.stop = False
        self.end = False

    def init_window(self):
        w = self.w
        # 初始化配置
        w.checkBox_status_code_200.setChecked(False)
        w.checkBox_status_code_3XX.setChecked(False)
        w.checkBox_status_code_403.setChecked(False)
        w.checkBox_status_code_500.setChecked(False)
        w.checkBox_php.setChecked(False)
        w.checkBox_asp.setChecked(False)
        w.checkBox_aspx.setChecked(False)
        w.checkBox_jsp.setChecked(False)
        w.checkBox_others.setChecked(False)
        w.checkBox_user_defined.setChecked(False)

        Logger.log('读取初始配置信息：')
        with open('conf/wbs.config', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue
                lines = line.split('=')
                conf_key = lines[0].strip()
                conf_val = lines[1].strip()
                if conf_key == 'debug' or conf_key == 'detail':
                    if conf_val.lower() == 'true':
                        conf_val = True
                    else:
                        conf_val = False
                elif conf_key == 'status_code' or conf_key == 'suffix':
                    tmp_lst = []
                    for item in conf_val.split(','):
                        tmp_lst.append(item.strip())
                    conf_val = tmp_lst

                Logger.log('key:', conf_key, 'val:', conf_val)

                # 还原配置信息
                if conf_key == 'speed':
                    w.comboBox_speed.setCurrentIndex(int(conf_val))
                    if int(conf_val) == 0:
                        w.timeEdit_delay.setEnabled(True)
                    else:
                        w.timeEdit_delay.setEnabled(False)
                elif conf_key == 'status_code':
                    for tmp_values in conf_val:
                        if tmp_values == '200':
                            w.checkBox_status_code_200.setChecked(True)
                        elif tmp_values == '3XX':
                            w.checkBox_status_code_3XX.setChecked(True)
                        elif tmp_values == '403':
                            w.checkBox_status_code_403.setChecked(True)
                        elif tmp_values == '500':
                            w.checkBox_status_code_500.setChecked(True)
                elif conf_key == 'suffix':
                    for tmp_values in conf_val:
                        if tmp_values.lower() == 'php':
                            w.checkBox_php.setChecked(True)
                        elif tmp_values.lower() == 'asp':
                            w.checkBox_asp.setChecked(True)
                        elif tmp_values.lower() == 'aspx':
                            w.checkBox_aspx.setChecked(True)
                        elif tmp_values.lower() == 'jsp':
                            w.checkBox_jsp.setChecked(True)
                        elif tmp_values.lower() == 'others':
                            w.checkBox_others.setChecked(True)
                        elif tmp_values.lower() == 'user_defined':
                            w.checkBox_user_defined.setChecked(True)
                elif conf_key == 'detail':
                    if not conf_val:
                        w.checkBox_detail.setChecked(False)
                    else:
                        w.checkBox_detail.setChecked(True)
                elif conf_key == 'debug':
                    Options.debug = conf_val

        # 获取资源数量
        Logger.log('获取资源数量：')
        file_dir = 'dict'
        for file in os.listdir(file_dir):
            count = str(len(open('dict/%s' % file, 'r', encoding='utf-8').readlines()))
            # Logger.log(file, count)
            if file == 'php':
                w.label_php_num.setText(count)
            elif file == 'asp':
                w.label_asp_num.setText(count)
            elif file == 'aspx':
                w.label_aspx_num.setText(count)
            elif file == 'jsp':
                w.label_jsp_num.setText(count)
            elif file == 'others':
                w.label_others_num.setText(count)
            elif file == 'user_defined':
                w.label_user_defined_num.setText(count)

    # 打印日志
    def logger(self, *ss):
        s = ''
        for tmp_str in ss:
            s += str(tmp_str) + ' '
        if s.endswith(' '):
            s = s[:-1]
        if len(s) > 0:
            self.w.plainTextEdit_log.setPlainText(s)

    # 添加结果
    def add_result(self, url, status_code):
        self.res_num += 1
        r = "%d    %s        %d" % (self.res_num, url, status_code)
        self.w.listWidget_result.addItem(r)

    # 设置扫描数量信息
    def set_request_number(self, **kwargs):
        self.w.label_task_number_val.setText(str(kwargs.get('task_number')))
        self.w.label_task_queue_val.setText(str(kwargs.get('task_queue')))
        self.w.label_request_times_val.setText(str(kwargs.get('request_times')))
        self.w.label_completed_val.setText(str(kwargs.get('completed')))

    # 切换扫描速度
    def change_speed(self):
        w = self.w
        if w.comboBox_speed.currentIndex() == 0:
            w.timeEdit_delay.setEnabled(True)
        else:
            w.timeEdit_delay.setTime(QtCore.QTime(0, 0))
            w.timeEdit_delay.setEnabled(False)

    # 启动扫描
    def push_start(self):
        w = self.w
        Logger.log('--开始扫描--')
        self.start = True
        self.stop = False
        self.end = False
        # 设置控件状态
        w.pushButton_start.setEnabled(False)
        w.pushButton_stop.setEnabled(True)
        w.pushButton_end.setEnabled(True)
        w.lineEdit_target.setEnabled(False)

        w.comboBox_speed.setEnabled(False)
        w.timeEdit_delay.setEnabled(False)
        w.checkBox_status_code_200.setEnabled(False)
        w.checkBox_status_code_3XX.setEnabled(False)
        w.checkBox_status_code_403.setEnabled(False)
        w.checkBox_status_code_500.setEnabled(False)
        w.checkBox_php.setEnabled(False)
        w.checkBox_asp.setEnabled(False)
        w.checkBox_aspx.setEnabled(False)
        w.checkBox_jsp.setEnabled(False)
        w.checkBox_others.setEnabled(False)
        w.checkBox_user_defined.setEnabled(False)

        # 读取启动参数
        target = w.lineEdit_target.text()
        detail = w.checkBox_detail.isChecked()
        concurrency = w.comboBox_speed.currentIndex()
        delay = int(w.timeEdit_delay.text())

        status_code_lst = []
        if w.checkBox_status_code_200.isChecked():
            status_code_lst.append('200')
        if w.checkBox_status_code_3XX.isChecked():
            status_code_lst.append('3XX')
        if w.checkBox_status_code_403.isChecked():
            status_code_lst.append('403')
        if w.checkBox_status_code_500.isChecked():
            status_code_lst.append('500')

        languages_lst = []
        if w.checkBox_php.isChecked():
            languages_lst.append('php')
        if w.checkBox_asp.isChecked():
            languages_lst.append('asp')
        if w.checkBox_aspx.isChecked():
            languages_lst.append('aspx')
        if w.checkBox_jsp.isChecked():
            languages_lst.append('jsp')
        if w.checkBox_others.isChecked():
            languages_lst.append('others')
        if w.checkBox_user_defined.isChecked():
            languages_lst.append('user_defined')

        # 配置启动参数
        Options.target = target
        Options.detail = detail
        Options.concurrency = concurrency
        Options.delay = delay
        Options.status_code = status_code_lst
        Options.languages = languages_lst

        # 调用后台扫描
        startserver.startup()

    # 暂停扫描
    def push_stop(self):
        w = self.w
        Logger.log('--暂停扫描--')
        self.stop = True
        self.start = False
        self.end = False
        w.pushButton_stop.setEnabled(False)
        w.pushButton_end.setEnabled(True)
        w.pushButton_start.setEnabled(True)
        w.lineEdit_target.setEnabled(False)

    # 结束扫描
    def push_end(self):
        w = self.w
        Logger.log('--结束扫描--')
        self.end = True
        self.start = False
        self.stop = False
        # 设置控件状态
        w.pushButton_stop.setEnabled(False)
        w.pushButton_end.setEnabled(False)
        w.pushButton_start.setEnabled(True)
        w.lineEdit_target.setEnabled(True)

        w.comboBox_speed.setEnabled(True)
        w.timeEdit_delay.setEnabled(True)
        w.checkBox_status_code_200.setEnabled(True)
        w.checkBox_status_code_3XX.setEnabled(True)
        w.checkBox_status_code_403.setEnabled(True)
        w.checkBox_status_code_500.setEnabled(True)
        w.checkBox_php.setEnabled(True)
        w.checkBox_asp.setEnabled(True)
        w.checkBox_aspx.setEnabled(True)
        w.checkBox_jsp.setEnabled(True)
        w.checkBox_others.setEnabled(True)
        w.checkBox_user_defined.setEnabled(True)
