# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/hdus/.qgis/python/plugins/wps/qgswpsdescribeprocessgui.ui'
#
# Created: Thu Nov 11 16:18:04 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QgsWpsDescribeProcessGUI(object):
    def setupUi(self, QgsWpsDescribeProcessGUI):
        QgsWpsDescribeProcessGUI.setObjectName("QgsWpsDescribeProcessGUI")
        QgsWpsDescribeProcessGUI.setWindowModality(QtCore.Qt.NonModal)
        QgsWpsDescribeProcessGUI.resize(476, 607)

        self.retranslateUi(QgsWpsDescribeProcessGUI)
        QtCore.QMetaObject.connectSlotsByName(QgsWpsDescribeProcessGUI)

    def retranslateUi(self, QgsWpsDescribeProcessGUI):
        QgsWpsDescribeProcessGUI.setWindowTitle(QtGui.QApplication.translate("QgsWpsDescribeProcessGUI", "Dialog", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    QgsWpsDescribeProcessGUI = QtGui.QDialog()
    ui = Ui_QgsWpsDescribeProcessGUI()
    ui.setupUi(QgsWpsDescribeProcessGUI)
    QgsWpsDescribeProcessGUI.show()
    sys.exit(app.exec_())
