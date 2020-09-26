# -*- coding: utf-8 -*-
"""
 /***************************************************************************
   QGIS Web Processing Service Plugin
  -------------------------------------------------------------------
 Date                 : 09 November 2009
 Copyright            : (C) 2009 by Dr. Horst Duester
 email                : horst dot duester at kappasys dot ch

  ***************************************************************************
  *                                                                         *
  *   This program is free software; you can redistribute it and/or modify  *
  *   it under the terms of the GNU General Public License as published by  *
  *   the Free Software Foundation; either version 2 of the License, or     *
  *   (at your option) any later version.                                   *
  *                                                                         *
  ***************************************************************************/
"""
from __future__ import absolute_import
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtNetwork import *
from qgis.core import *
from . import version
from .wpslib.wpsserver import WpsServer
from .Ui_qgswpsgui import Ui_QgsWps
from .qgswpsbookmarks import Bookmarks
from .doAbout import DlgAbout


import os, sys, string
from .apicompat.sipv2.compat import pystring, pyint


class QgsWpsGui(QDialog, QObject, Ui_QgsWps):
  MSG_BOX_TITLE = "WPS"
  getDescription = pyqtSignal(str,  QTreeWidgetItem)  
  newServer = pyqtSignal()  
  editServer = pyqtSignal(str)  
  deleteServer = pyqtSignal(str)          
  connectServer = pyqtSignal(list)   
  pushDefaultWPSServer = pyqtSignal(str)   
  requestDescribeProcess = pyqtSignal(str,  str)  
  
  
  def __init__(self, parent, fl):
    QDialog.__init__(self, parent, fl)
    self.setupUi(self)
    self.fl = fl
    self.setWindowTitle('QGIS WPS-Client '+version())
    self.dlgAbout = DlgAbout(parent)
    self.filterText = ''
    self.lneFilter.setText('')
   
  def initQgsWpsGui(self):    
##    self.btnOk.setEnabled(False)
    self.btnConnect.setEnabled(False)
    settings = QSettings()
    settings.beginGroup("WPS")
    connections = settings.childGroups()
    self.cmbConnections.clear()
    self.cmbConnections.addItems(connections)
    self.treeWidget.clear()
    
    if self.cmbConnections.count() > 0:
      self.btnConnect.setEnabled(True)
      self.btnEdit.setEnabled(True)
      self.btnDelete.setEnabled(True)

    try:
        settings = QSettings()
        myIndex = pyint(settings.value("WPS-lastConnection/Index",  "Index"))
        self.cmbConnections.setCurrentIndex(myIndex)
    except:
        pass

    return 1    

  def getBookmark(self, item):
      self.requestDescribeProcess.emit(item.text(0), item.text(1))
        
  def on_buttonBox_rejected(self):
    self.close()

  # see http://www.riverbankcomputing.com/Docs/PyQt4/pyqt4ref.html#connecting-signals-and-slots
  # without this magic, the on_btnOk_clicked will be called two times: one clicked() and one clicked(bool checked)
  def on_buttonBox_accepted(self):
    if  self.treeWidget.topLevelItemCount() == 0:
      QMessageBox.warning(None, 'WPS Warning','No Service connected!')
    else:
      try:
        self.getDescription.emit(self.cmbConnections.currentText(),  self.treeWidget.currentItem() )
      except:
        QMessageBox.information(None, self.tr('Error'),  self.tr('Please select a process!'))
    
  # see http://www.riverbankcomputing.com/Docs/PyQt4/pyqt4ref.html#connecting-signals-and-slots
  # without this magic, the on_btnOk_clicked will be called two times: one clicked() and one clicked(bool checked)
  def on_btnConnect_clicked(self):
    self.treeWidget.clear()
    self.filterText = ''
    self.lneFilter.setText('')
    selectedWPS = self.cmbConnections.currentText()
    self.server = WpsServer.getServer(selectedWPS)
    self.server.capabilitiesRequestFinished.connect(self.createCapabilitiesGUI)
    self.server.requestCapabilities()

  def on_btnBookmarks_clicked(self):    
      self.dlgBookmarks = Bookmarks(self.fl)
      self.dlgBookmarks.getBookmarkDescription.connect(self.getBookmark)
#      self.dlgBookmarks.bookmarksChanged.connect(bookmarksChanged())
      self.dlgBookmarks.show()

  def on_btnNew_clicked(self):    
    self.newServer.emit()

  def on_btnEdit_clicked(self):    
    self.editServer.emit(self.cmbConnections.currentText())    

  def on_cmbConnections_activated(self,  index):
    settings = QSettings()
    settings.setValue("WPS-lastConnection/Index", pystring(index))

  def on_btnDelete_clicked(self):    
    self.deleteServer.emit(self.cmbConnections.currentText())    

  def initTreeWPSServices(self, taglist):
    self.treeWidget.clear()
    self.treeWidget.setColumnCount(self.treeWidget.columnCount())
    itemList = []
    
    for items in taglist:

        if self.filterText == '':
            item = QTreeWidgetItem()
            ident = pystring(items[0])
            title = pystring(items[1])
            abstract = pystring(items[2])
            item.setText(0,ident.strip())
            item.setText(1,title.strip())  
            item.setText(2,abstract.strip())  
            itemList.append(item)
        else:
            if self.filterText in pystring(items[0]) or self.filterText in pystring(items[1]) or self.filterText in pystring(items[2]):
                item = QTreeWidgetItem()
                ident = pystring(items[0])
                title = pystring(items[1])
                abstract = pystring(items[2])
                item.setText(0,ident.strip())
                item.setText(1,title.strip())  
                item.setText(2,abstract.strip())  
                itemList.append(item)
    
    self.treeWidget.addTopLevelItems(itemList)

  def on_btnAbout_clicked(self):
      self.dlgAbout.show()
      pass

  def on_treeWidget_itemDoubleClicked(self, item, column):
      self.getDescription.emit(self.cmbConnections.currentText(),  self.treeWidget.currentItem() )

  def createCapabilitiesGUI(self):
#      try:
          self.treeWidget.clear()
          self.itemListAll = self.server.parseCapabilitiesXML()
          self.initTreeWPSServices(self.itemListAll)
#      except:
#          pass

  def on_lneFilter_textChanged(self, p0):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.filterText = p0
        self.initTreeWPSServices(self.itemListAll)
