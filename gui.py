"""
@author: Jayalath A M Madawa Abeywardhana

Useful references>>
Qt tutorials : http://zetcode.com/gui/pyqt5/layout/
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtGui import QFont

import configs as cfgs
from dataBaseSqlite3 import DataBaseSqlite3 as dbs
from guiSlots import GUISlots as guiSlots


class GUI(QMainWindow):
 
    def __init__(self):
        super(GUI, self).__init__()
        
        # run parameters and database paramters
        self.runParams = cfgs.config().runParams
        self.DB = {}
        self.gs = guiSlots()
        
        # set up main window
        self.title = 'DB Local'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create tabs
        self.tab_widget = TabWidget(self)
        # set tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

        tab1 = self.tab_widget.tab1
        tab2 = self.tab_widget.tab2
        tab3 = self.tab_widget.tab3

        # connect 'loadDB' function to clicked signal of load button
        tab1.dbLoad_btn.clicked.connect(lambda: self.gs.loadDB(self))
        # connect 'loadDB' function to enter key press signal of database name textbox
        tab1.dbName_edit.returnPressed.connect(lambda: self.gs.loadDB(self))

        #tab2.tablesCBox.currentIndexChanged.connect(self.loadTable)
        tab2.tablesCBox.currentIndexChanged.connect(lambda: self.gs.loadTable(self))

        # This static method sets a font used to render tooltips
        QToolTip.setFont(QFont('SansSerif', 10))
        # To create a tooltip, we call the setTooltip() method. We can use rich text formatting. 
        # btn.setToolTip('This is a <b>QPushButton</b> widget')

        # connedt slot functions for buttons in tab2
        tab2.recEdit_btn.clicked.connect(lambda: self.gs.editRecord(self))
        tab2.recInsert_btn.clicked.connect(lambda: self.gs.insertRecord(self))

        tab3.exec_btn.clicked.connect(lambda: self.gs.executeSQLQuery(self))

        # show main window
        self.show()

    # close main window on escape key press
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

class TabWidget(QWidget):
    """
    Widget that include the tabs
    """
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = DBTab()
        #self.tab2 = QWidget()
        self.tab2 = TablesTab()
        #self.tabs.resize(300,200) 
        self.tab3 = SQLTab()
        # Add tabs
        self.tabs.addTab(self.tab1,"Database")
        self.tabs.addTab(self.tab2,"Tables")
        self.tabs.addTab(self.tab3,"SQL Query")
  
        # Add tabs to widget        
        layout.addWidget(self.tabs)
        self.setLayout(layout)


class SQLTab(QWidget):
    """
    SQL query tab 
    """
    def __init__(self):
        super(SQLTab, self).__init__()
        
        self.initContent()
        
        
    def initContent(self):


        # create a push button widget
        self.exec_btn = QPushButton('Execute', self)
        self.exec_btn.setToolTip('Execute QSL query')
        
        #self.table_lbl = QLabel('Table')
        # text box for sql query
        self.queryTextBox = QTextEdit(self)

        # plain textbox to display sql output
        self.sqlOutput = QPlainTextEdit(self)
        self.sqlOutput.setReadOnly(True)

        # create a grid layout and set spacing between widgets. 
        grid = QGridLayout()
        grid.setSpacing(10)

        # setup grid
        #grid.addWidget(self.table_lbl, 1, 0)
        grid.addWidget(self.queryTextBox, 0, 0, 3, 4)
        grid.addWidget(self.exec_btn, 2, 4)
        grid.addWidget(self.sqlOutput, 3, 0, 2, 5)
        #grid.addWidget(self.tblWidget, 2, 0, 5, 4)

        self.setLayout(grid)


        
class TablesTab(QWidget):
    """
    Tables tab 
    """
    def __init__(self):
        super(TablesTab, self).__init__()
        
        self.initContent()
        
        
    def initContent(self):


        # We create a push button widget
        self.recInsert_btn = QPushButton('Insert', self)
        self.recInsert_btn.setToolTip('Insert a new record')
        self.recEdit_btn = QPushButton('Edit', self)
        self.recEdit_btn.setToolTip('Edit selected row')
        
        #self.table_lbl = QLabel('Table')
        # Create and fill the combo box to choose the salutation
        self.tablesCBox = QComboBox(self)

        # table
        self.tblWidget = QTableView()
        # set selection behavior to select the entire row and to single row selection mode
        self.tblWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # create a grid layout and set spacing between widgets. 
        grid = QGridLayout()
        grid.setSpacing(10)

        # setup grid
        #grid.addWidget(self.table_lbl, 1, 0)
        grid.addWidget(self.tablesCBox, 1, 0, 1, 2)
        grid.addWidget(self.recInsert_btn, 1, 2)
        grid.addWidget(self.recEdit_btn, 1, 3)
        grid.addWidget(self.tblWidget, 2, 0, 5, 4)

        self.setLayout(grid)
        
class DBTab(QWidget):
    """
    Database tab
    """
    def __init__(self):
        super(DBTab, self).__init__()
        
        self.initContent()
        
        
    def initContent(self):

        # lables
        self.dbName_lbl = QLabel('Database Name')
        self.cols_lbl = QLabel('Columns')
        self.tables_lbl = QLabel('Tables')

        # database name entry
        self.dbName_edit = QLineEdit()
        
        # table list widget
        self.tableListwidget = QListWidget()
        self.colsListwidget = QListWidget()

        # We create a push button widget and set a tooltip for it.
        self.dbLoad_btn = QPushButton('Load', self)
        self.dbLoad_btn.setToolTip('Load <b>sqlite</b> database ')

        # connect on_click function to clicked signal
        #self.dbLoad_btn.clicked.connect(self.loadDB)

        # create a grid layout and set spacing between widgets. 
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.dbName_lbl, 1, 0)
        grid.addWidget(self.dbName_edit, 1, 1)
        grid.addWidget(self.dbLoad_btn, 1, 2, 1, 1)

        grid.addWidget(self.tables_lbl, 2, 0)
        grid.addWidget(self.cols_lbl, 2, 2, 1, 2)

        # make the reviewEdit widget span 5 rows. 
        grid.addWidget(self.tableListwidget, 3, 0, 5, 2)
        grid.addWidget(self.colsListwidget, 3, 2, 5, 2)
        
        self.setLayout(grid) 
        
        #self.setGeometry(300, 300, 350, 300)
        #self.setWindowTitle('Review')    

#################################################################################
## How to query any sql statement:
# query = QSqlQuery()
# #query.prepare("SELECT * FROM {};".format(tblName))
# #query.prepare("SELECT * FROM sqlite_master WHERE type='table';")
# query.prepare("pragma table_info({});".format(tblName))

# print query.exec_()
# while query.next():
#     i=0
#     while i < query.record().count():
#         print "i:: ", i, " fName: ", query.record().fieldName(i), " Val: ", query.value(i)
#         i=i+1

