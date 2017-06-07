# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class HistogramView(QAbstractItemView):
    def __init__(self, parent):
        super(HistogramView, self).__init__()
        self.listRegionM = []
        self.listRegionF = []
        self.listRegionS = []
        self.region = QRegion()

    def paintEvent(self, QPaintEvent):
        print "paintEvent\n"
        painter = QPainter(self.viewport())
        painter.setPen(Qt.black)
        x0 = 40
        y0 = 250
        painter.drawLine(x0, y0, 40, 30)
        painter.drawLine(38, 32, 40, 30)
        painter.drawLine(40, 30, 42, 32)
        painter.drawText(20, 30, self.tr("num"))
        for i in xrange(5):
            painter.drawLine(-1, -i * 50, 1, -i * 50)
            painter.drawText(-20, -i * 50, self.tr("%1").arg(i * 5))

        painter.drawLine(x0, y0, 540, 250)
        painter.drawLine(538, 248, 540, 250)
        painter.drawLine(540, 250, 538, 252)
        painter.drawText(545, 250, self.tr("department"))

        posD = x0 + 20
        for row in xrange(self.model().rowCount(self.rootIndex())):
            index = self.model().index(row, 0, self.rootIndex())
            dep = self.model().data(index).toString()

            painter.drawText(posD, y0 + 20, dep)
            posD += 50

        posM = x0 + 20
        for row in xrange(self.model().rowCount(self.rootIndex())):
            index = self.model().index(row, 1, self.rootIndex())
            male = self.model().data(index).toDouble()[0]

            width = 10
            if self.selections.isSelected(index):
                painter.setBrush(QBrush(Qt.blue, Qt.Dense3Pattern))
            else:
                painter.setBrush(Qt.blue)
            painter.drawRect(QRect(posM, y0 - male * 10, width, male * 10))
            regionM = QRegion(posM, y0 - male * 10, width, male * 10)
            self.listRegionM.append(regionM)
            posM += 50
        posF = x0 + 30
        for row in xrange(self.model().rowCount(self.rootIndex())):
            index = self.model().index(row, 2, self.rootIndex())
            female = self.model().data(index).toDouble()[0]
            width = 10
            if self.selections.isSelected(index):
                painter.setBrush(QBrush(Qt.red, Qt.Dense3Pattern))
            else:
                painter.setBrush(Qt.red)
            painter.drawRect(QRect(posF, y0 - female * 10, width, female * 10))
            regionF = QRegion(posF, y0 - female * 10, width, female * 10)
            self.listRegionF.append(regionF)
            posF += 50
        posS = x0 + 40
        for row in xrange(self.model().rowCount(self.rootIndex())):
            index = self.model().index(row, 3, self.rootIndex())
            sum = self.model().data(index).toDouble()[0]
            width = 10
            if self.selections.isSelected(index):
                painter.setBrush(QBrush(Qt.green, Qt.Dense3Pattern))
            else:
                painter.setBrush(Qt.green)
            painter.drawRect(QRect(posS, y0 - sum * 10, width, sum * 10))
            regionS = QRegion(posS, y0 - sum * 10, width, sum * 10)
            self.listRegionS.append(regionS)
            posS += 50

    def datachanged(self, topLeft, bottomRight):
        QAbstractItemView.dataChanged(topLeft, bottomRight)
        self.viewport().update()

    def setSelectionModel(self, sectionModel):
        self.selections = sectionModel

    def selectionChanged(self, selected, deselected):
        self.viewport().update()

    def setSelection(self, rect, flags):
        rows = self.model().rowCount(self.rootIndex())
        columns = self.model().columnCount(self.rootIndex())
        selectedIndex = QModelIndex()
        for row in xrange(rows):
            for column in xrange(1, columns):
                index = self.model().index(row, column, self.rootIndex())
                self.region = self.itemRegion(index)
                if not region.intersected(contentsRect).isEmpty():
                    selectedIndex = index
        if selectedIndex.isValid():
            self.selections.select(selectedindex, flags)
        else:
            noIndex = QModelIndex()
            self.selections.select(noIndex, flags)

    def mousePressEvent(self, e):
        QAbstractItemView.mousePressEvent(self, e)
        self.setSelection(QRect(e.pos().x(), e.pos().y(), 1, 1), QItemSelectionModel.SelectCurrent)

    def itemRegion(self, index):
        if index.column() == 1:
            self.region = self.listRegionM(index.row())
        if index.column() == 2:
            self.region = self.listRegionF(index.row())
        if index.column() == 3:
            self.region = self.listRegionS(index.row())
        return self.region

    def indexAt(self, point):
        newPoint = QPoint(point.x(), point.y())
        region = QRegion()
        for region in self.listRegionM:
            if region.contains(newPoint):
                row = self.listRegionM.indexOf(region)
                index = self.model().index(row, 1, self.rootIndex())
                return index
        for region in self.listRegionF:
            if region.contains(newPoint):
                row = self.listRegionF.indexOf(region)
                index = self.model().index(row, 1, self.rootIndex())
                return index
        for region in self.listRegionS:
            if region.contains(newPoint):
                row = self.listRegionS.indexOf(region)
                index = self.model().index(row, 1, self.rootIndex())
                return index
        return QModelIndex()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.name = QString()
        self.strList = QStringList()
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)

        self.createActions()
        self.createMenus()
        self.setupModel()
        self.setupView()
        file = QFile("./image/data.tab")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.model.removeRows(0, self.model.rowCount(QModelIndex()), QModelIndex())
            row = 0

            while True:
                line = stream.readLine()
                if line.isEmpty() is False:
                    self.model.insertRows(row, 1, QModelIndex())
                    pieces = line.split(",", QString.SkipEmptyParts)

                    self.model.setData(self.model.index(row, 0, QModelIndex()), pieces.takeAt(0))
                    self.model.setData(self.model.index(row, 1, QModelIndex()), pieces.takeAt(0))
                    self.model.setData(self.model.index(row, 2, QModelIndex()), pieces.takeAt(0))
                    self.model.setData(self.model.index(row, 3, QModelIndex()), pieces.takeAt(0))
                    row += 1

                else:
                    break

        file.close()

    def createActions(self):
        self.setMouseTracking(True)
        self.myaction = QAction(self.tr("打开"), self)
        self.connect(self.myaction, SIGNAL("triggered()"), self.slotOpenFile)

    def createMenus(self):
        PrintMenu = self.menuBar().addMenu(self.tr("文件"))
        PrintMenu.addAction(self.myaction)
        circumgyrateMenu = self.menuBar().addMenu(self.tr("编辑"))

    def setupModel(self):
        self.model = QStandardItemModel(4, 4, self)
        self.model.setHeaderData(0, Qt.Horizontal, self.tr("department"))
        self.model.setHeaderData(1, Qt.Horizontal, self.tr("male"))
        self.model.setHeaderData(2, Qt.Horizontal, self.tr("female"))
        self.model.setHeaderData(3, Qt.Horizontal, self.tr("retrie"))

    def setupView(self):
        table = QTableView()
        histogram = HistogramView(self.splitter)

        table.setModel(self.model)
        self.setCentralWidget(table)
        histogram.setModel(self.model)
        self.dockWidget = QDockWidget()
        self.dockWidget.setWidget(histogram)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget)

        selectionModel = QItemSelectionModel(self.model)
        table.setSelectionModel(selectionModel)
        histogram.setSelectionModel(selectionModel)

        histogram.connect(selectionModel, SIGNAL("selectionChanged(QItemSelection,QItemSelection)"),
                          histogram.selectionChanged)
        table.connect(selectionModel, SIGNAL("selectionChanged(QItemSelection,QItemSelection)"),
                      histogram.selectionChanged)

    def slotOpenFile(self):
        self.name = QFileDialog.getOpenFileName(self, "open file dialog", ".", "strip file(*.txt)")
        if self.name.isEmpty() is False:
            self.openFile(self.name)

    def slotSaveFile(self):
        if self.name.isEmpty():
            return
        file = QFile(self.name)
        if file.open(QFile.WriteOnly):
            return
        ts = QTextStream(self.file)
        for i in xrange(self.model.rowCount()):
            index = self.model.index(i)
            str = self.model.data(index).toString()
            ts << str << ","

    def openFile(self, path):
        if not path.isEmpty():
            file = QFile(path)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                self.model.removeRows(0, self.model.rowCount(QModelIndex()), QModelIndex())
                row = 0

                while True:
                    line = stream.readLine()
                    if line.isEmpty() is False:
                        self.model.insertRows(row, 1, QModelIndex())
                        pieces = line.split(",", QString.SkipEmptyParts)

                        self.model.setData(self.model.index(row, 0, QModelIndex()), pieces.takeAt(0))
                        self.model.setData(self.model.index(row, 1, QModelIndex()), pieces.takeAt(0))
                        self.model.setData(self.model.index(row, 2, QModelIndex()), pieces.takeAt(0))
                        self.model.setData(self.model.index(row, 3, QModelIndex()), pieces.takeAt(0))
                        row += 1

                    else:
                        break
            file.close()

    def slotInsertRows(self):
        ok = True
        index = self.list.currentIndex()
        rows = QInputDialog.getInteger(self, self.tr("Insert Row Number"), self.tr("Please input number:"), 1, 1, 10, 1,
                                       1, ok)
        if ok:
            self.model.insertfRows(index.row(), rows, QModelIndex())

    def slotRemoveRows(self):
        index = self.list.currentIndex()
        self.model.removeRows(index.row(), 1, QModelIndex())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()