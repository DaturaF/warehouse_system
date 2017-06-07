#!/usr/bin/env python
#coding=utf-8

"""
仓库管理系统主界面
by: xf
2017.6.6
"""
# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\p1.ui'
#
# Created: Fri Apr 21 10:21:55 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from dingdan import *
from xiugai import *
from db import *
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class P1(object):
    def __init__(self):
        super(P1, self).__init__()

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(833, 386)
        self.form = Dialog
        self.num_flag = 0  # 表格的行数记录
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 150, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(700, 80, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(700, 130, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 30, 150, 28))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(320, 30, 150, 28))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.tableWidget = QtGui.QTableWidget(Dialog)

        self.tableWidget.setGeometry(QtCore.QRect(30, 70, 651, 291))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels([u'编号', u'交接方', u'货物信息', u'货物属性', u'操作状态'])
        for x in range(self.tableWidget.columnCount()):
            headItem = self.tableWidget.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
            headItem.setBackgroundColor(QColor(0, 60, 10))  # 设置单元格背景颜色
            headItem.setTextColor(QColor(200, 111, 30))  # 设置文字颜色
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)  # 无法编辑
        # 初始化表格
        self.set_table()

        # 开启监控线程
        threads = []
        t1 = threading.Thread(target=self.db_detective, args=())
        threads.append(t1)
        for t in threads:
            t.setDaemon(True)
            t.start()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.finish_order)
        self.pushButton_2.clicked.connect(self.cancel_order)
        self.pushButton_3.clicked.connect(self.all_order)
        self.pushButton_4.clicked.connect(self.change_message)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "仓库管理系统", None))
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.blue)
        self.label.setPalette(pe)
        self.label.setText(_translate("Dialog", "待处理货物", None))
        self.pushButton.setText(_translate("Dialog", "完成入库", None))
        self.pushButton_2.setText(_translate("Dialog", "完成出库", None))
        self.pushButton_3.setText(_translate("Dialog", "查看全部库存记录", None))
        self.pushButton_4.setText(_translate("Dialog", "修改库内货物信息", None))

    def set_table(self):  # 表单设置
        print 'set table'
        db = DataBase()
        db.get_connect()
        db.execute('use warehouse_manage_system')
        sql = 'select serial_number,contract_party,cargo_message,cargo_property,status from inside_warehouse ' \
              'where status=\'准备出库，未确认\' or status=\'准备入库，未确认\' or status=\'准备入库，已确认\' or status=\'准备出库，已确认\' ;'
        result = db.execute(sql)
        if result:
            self.num_flag = len(result)-1
            print 'num', self.num_flag
            while self.tableWidget.rowCount() < self.num_flag+1:
                self.tableWidget.insertRow(1)
            for i in range(len(result)):
                for j in range(len(result[i])):
                    mes = result[i][j]
                    newItem = QtGui.QTableWidgetItem(u"%s" % mes)
                    self.tableWidget.setItem(i, j, newItem)

        db.db_close()

    def finish_order(self):  # 完成入库
        num = self.tableWidget.currentRow()
        serial_num = self.tableWidget.item(num, 0).text()
        status = self.tableWidget.item(num, 4).text()
        if status == u'准备入库，已确认':
            self.num_flag -= 1
            self.tableWidget.removeRow(num)
            db = DataBase()
            db.get_connect()
            db.execute('use warehouse_manage_system')
            sql = 'update inside_warehouse set status = \'已入库\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            sql = 'update manifest set status = \'已入库\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            db.db_close()
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkGreen)
            self.label.setPalette(pe)
            self.label.setText(_translate("Dialog", "确认入库完成", None))
            self.label.show()

        else:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkRed)
            self.label.setPalette(pe)
            self.label.setText(_translate("Dialog", "选择的货物状态不正确，请重新确认", None))
            self.label.show()

    def cancel_order(self):  # 完成出库
        num = self.tableWidget.currentRow()
        serial_num = self.tableWidget.item(num, 0).text()
        status = self.tableWidget.item(num, 4).text()
        if status == u'准备出库，已确认':
            self.num_flag -= 1
            self.tableWidget.removeRow(num)
            db = DataBase()
            db.get_connect()
            db.execute('use warehouse_manage_system')
            sql = 'update inside_warehouse set status = \'已出库\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            sql = 'update manifest set status = \'已出库\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            sql = 'update manifest set out_time = \'%s\' where serial_number = \'%s\';' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),serial_num)
            db.execute(sql)
            db.db_commit()
            db.db_close()
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkGreen)
            self.label.setPalette(pe)
            self.label.setText(_translate("Dialog", "确认出库完成", None))
            self.label.show()

        else:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkRed)
            self.label.setPalette(pe)
            self.label.setText(_translate("Dialog", "选择的货物状态不正确，请重新确认", None))
            self.label.show()

    def db_detective(self):  # 数据库数据实时监测线程
        print 'thread start'
        db = DataBase()
        db.get_connect()
        db.execute('use e_commerce')
        sql = 'select confirm_time, phone, address, client_order, total_price from user_order ;'
        result = db.execute(sql)
        db.db_close()
        num = len(result)
        temp = num
        print 'ori num', num
        while True:
            db = DataBase()
            db.get_connect()
            db.execute('use e_commerce')
            sql = 'select confirm_time, phone, address, client_order, total_price from user_order ;'
            result = db.execute(sql)
            num = len(result)
            if num != temp:
                print 'new num', num, temp
                for i in range(num-temp):
                    self.num_flag += 1
                    self.tableWidget.insertRow(self.num_flag)
                    for j in range(len(result[0])):
                        mes = result[-i-1][j]
                        newItem = QtGui.QTableWidgetItem(u"%s" % mes)
                        self.tableWidget.setItem(self.num_flag, j, newItem)
                temp = num
            db.db_close()
            time.sleep(1)

    def all_order(self):  # 查看订单
        self.form.hide()
        Form1 = QtGui.QDialog()
        ui = Ui_dingdan()
        ui.setupUi(Form1)
        Form1.show()
        Form1.exec_()
        self.form.show()

    def change_message(self):
        self.form.hide()
        Form1 = QtGui.QDialog()
        ui = Ui_xiugai()
        ui.setupUi(Form1)
        Form1.show()
        Form1.exec_()
        self.form.show()
        self.set_table()


