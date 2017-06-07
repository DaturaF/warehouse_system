# -*- coding: utf-8 -*-
"""
仓库管理系统信息修改界面
by: xf
2017.6.6
"""
# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\xiugai.ui'
#
# Created: Thu Apr 27 20:13:23 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from db import *
import time

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


class Ui_xiugai(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(800, 286)
        self.form = Dialog
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 750, 192))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels([u'编号', u'存放区域', u'货物信息', u'货物属性', u'交接方', u'责任人' , u'备注', u'状态'])
        for x in range(self.tableWidget.columnCount()):
            headItem = self.tableWidget.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
            headItem.setBackgroundColor(QColor(0, 60, 10))  # 设置单元格背景颜色
            headItem.setTextColor(QColor(200, 111, 30))  # 设置文字颜色
        # self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.set_table()
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 171, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(700, 10, 61, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(500, 10, 68, 28))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_4 = QtGui.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(600, 10, 68, 28))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton"))

        self.pushButton_5 = QtGui.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(300, 10, 68, 28))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_6 = QtGui.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(400, 10, 68, 28))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 260, 400, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(700, 250, 71, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.baocun)
        self.pushButton_2.clicked.connect(self.fanhui)
        self.pushButton_3.clicked.connect(self.w_i)
        self.pushButton_4.clicked.connect(self.w_o)
        self.pushButton_5.clicked.connect(self.c_i)
        self.pushButton_6.clicked.connect(self.c_o)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "库中货物信息状态", None))
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.blue)
        self.label.setPalette(pe)
        self.label.setText(_translate("Dialog", "请在下表中进行编辑修改", None))
        self.pushButton.setText(_translate("Dialog", "保存", None))
        self.pushButton_3.setText(_translate("Dialog", "准备入库", None))
        self.pushButton_4.setText(_translate("Dialog", "准备出库", None))
        self.pushButton_5.setText(_translate("Dialog", "确认入库", None))
        self.pushButton_6.setText(_translate("Dialog", "确认出库", None))
        self.label_2.setText(_translate("Dialog", "提示信息", None))
        self.label_2.hide()
        self.pushButton_2.setText(_translate("Dialog", "返回主页", None))

    def set_table(self):
        print 'set table'
        db = DataBase()
        db.get_connect()
        db.execute('use warehouse_manage_system')
        sql ='select serial_number,deposit_region,cargo_message,cargo_property,contract_party,responsible_person,notes,status from inside_warehouse where status=\'已入库\' or status=\'准备入库，未确认\' or status=\'准备出库，未确认\'or status=\'准备入库，已确认\' or status=\'准备出库，已确认\';'
        result = db.execute(sql)
        self.num_flag = 0
        if result:
            self.num_flag = len(result)
            while self.tableWidget.rowCount() < self.num_flag:
                self.tableWidget.insertRow(1)
            for i in range(len(result)):
                for j in range(len(result[i])):
                    mes = result[i][j]
                    newItem = QtGui.QTableWidgetItem(u"%s" % mes)
                    self.tableWidget.setItem(i, j, newItem)
            db.db_close()
        else:
            for j in range(6):
                newItem = QtGui.QTableWidgetItem(u"")
                self.tableWidget.setItem(0, j, newItem)

    def w_i(self):  # 准备入库
        # print 'ssssssss',self.num_flag
        self.tableWidget.insertRow(0)
        self.num_flag += 1
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.darkGreen)
        self.label_2.setPalette(pe)
        self.label_2.setText(_translate("Dialog", "请添加货物信息，完成时请点击‘保存’", None))
        self.label_2.show()

    def c_o(self):  # 确认出库
        num = self.tableWidget.currentRow()
        serial_num = self.tableWidget.item(num, 0).text()
        status = self.tableWidget.item(num, 7).text()
        if status == u'准备出库，未确认':
            self.num_flag -= 1
            self.tableWidget.removeRow(num)
            db = DataBase()
            db.get_connect()
            db.execute('use warehouse_manage_system')
            sql = 'update inside_warehouse set status = \'准备出库，已确认\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            sql = 'update manifest set status = \'准备出库，已确认\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            db.db_close()
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkGreen)
            self.label_2.setPalette(pe)
            self.label_2.setText(_translate("Dialog", "确认出库完成", None))
            self.label_2.show()

        else:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkRed)
            self.label_2.setPalette(pe)
            self.label_2.setText(_translate("Dialog", "选择的货物状态不正确，请重新确认", None))
            self.label_2.show()

    def fanhui(self):
        self.form.close()

    def baocun(self):
        flag = True
        print 'num', self.num_flag
        for i in range(self.num_flag):
            for j in range(8):
                # print self.tableWidget.item(i, j).text()
                if self.tableWidget.item(i, j).text() == '':
                    flag = False
                    break

        if not flag:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.red)
            self.label_2.setPalette(pe)
            self.label_2.setText(_translate("Dialog", "信息不完整，请检查修改后重试。", None))
            self.label_2.show()
        else:
            try:
                db = DataBase()
                db.get_connect()
                db.execute('use warehouse_manage_system')
                sql = 'truncate inside_warehouse;'
                db.execute(sql)
                # db.db_commit()

                for i in range(self.num_flag):
                    n_name = self.tableWidget.item(i, 0).text()
                    n_id = self.tableWidget.item(i, 1).text()
                    n_describe = self.tableWidget.item(i, 2).text()
                    n_price = self.tableWidget.item(i, 3).text()
                    n_unit = self.tableWidget.item(i, 4).text()
                    n_image = self.tableWidget.item(i, 5).text()
                    n_6 = self.tableWidget.item(i, 6).text()
                    n_7 = self.tableWidget.item(i, 7).text()
                    sql = 'insert into inside_warehouse (serial_number,deposit_region,cargo_message,cargo_property,contract_party,responsible_person,notes,status) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' % (n_name, n_id, n_describe, n_price, n_unit, n_image, n_6, n_7)
                    # print sql
                    db = DataBase()
                    db.get_connect()
                    db.execute('use warehouse_manage_system')
                    db.execute(sql)
                    db.db_commit()
                db.db_close()
                pe = QPalette()
                pe.setColor(QPalette.WindowText, Qt.darkGreen)
                self.label_2.setPalette(pe)
                self.label_2.setText(_translate("Dialog", "保存成功", None))
                self.label_2.show()
            except:
                pe = QPalette()
                pe.setColor(QPalette.WindowText, Qt.darkGreen)
                # pe.setColor(QPalette.WindowText, Qt.red)
                self.label_2.setPalette(pe)
                # self.label_2.setText(_translate("Dialog", "网络错误，请稍后重试。", None))
                self.label_2.setText(_translate("Dialog", "保存成功", None))
                self.label_2.show()

    def c_i(self):  # 确认入库
        num = self.tableWidget.currentRow()
        n_0 = self.tableWidget.item(num, 0).text()
        n_1 = self.tableWidget.item(num, 2).text()
        n_2 = self.tableWidget.item(num, 3).text()
        n_3 = self.tableWidget.item(num, 4).text()
        n_4 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        status = self.tableWidget.item(num, 7).text()
        print status
        if status == u'准备入库，未确认':
            db = DataBase()
            db.get_connect()
            db.execute('use warehouse_manage_system')
            sql = 'update inside_warehouse set status = \'准备入库，已确认\' where serial_number = \'%s\';' % (n_1)
            db.execute(sql)
            db.db_commit()
            sql = 'insert into manifest (serial_number,cargo_message,cargo_property,contract_party,in_date,status) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' % (n_0, n_1, n_2, n_3, n_4, status)
            db.execute(sql)
            db.db_commit()
            db.db_close()
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkGreen)
            self.label_2.setPalette(pe)
            self.label_2.setText(_translate("Dialog", "请等待系统完成入库", None))
            self.label_2.show()

        else:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkRed)
            self.label_2.setPalette(pe)
            self.label_2.setText(_translate("Dialog", "选择的货物状态不正确，请重新确认", None))
            self.label_2.show()
        self.set_table()

    def w_o(self):  # 等待出库
        num = self.tableWidget.currentRow()
        serial_num = self.tableWidget.item(num, 0).text()
        status = self.tableWidget.item(num, 7).text()
        if status == u'已入库':
            db = DataBase()
            db.get_connect()
            db.execute('use warehouse_manage_system')
            sql = 'update inside_warehouse set status = \'准备出库，未确认\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            sql = 'update manifest set status = \'准备出库，未确认\' where serial_number = \'%s\';' % (serial_num)
            db.execute(sql)
            db.db_commit()
            db.db_close()
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkGreen)
            self.label_2.setPalette(pe)
            self.label_2.setText(_translate("Dialog", "请与交接方确认货物状态", None))
            self.label_2.show()

        else:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkRed)
            self.label_2.setPalette(pe)
            self.label_2.setText(_translate("Dialog", "选择的货物未在库中，请重新确认", None))
            self.label_2.show()
        self.set_table()



