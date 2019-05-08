"""
@author: Jayalath A M Madawa Abeywardhana

Useful references>>
Qt tutorials : http://zetcode.com/gui/pyqt5/layout/
"""


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel

class GUISlots():
    def __init__(self):
        pass

    def executeSQLQuery(self, gui):
        tab2 = gui.tab_widget.tab2
        tab3 = gui.tab_widget.tab3
        query = gui.DB['query'] # or query = QSqlQuery() # would work too

        sqlQuery = tab3.queryTextBox.toPlainText()

        query.prepare(sqlQuery)
        #print "Query excuting... result: ", query.exec_()

        tab3.sqlOutput.setPlainText(sqlQuery)

    def insertRecord(self, gui):

        tab2 = gui.tab_widget.tab2
        query = gui.DB['query'] # or query = QSqlQuery() # would work too

        # lists of form lables and lineEdit boxes
        lableList = []
        editList = []

        # get selected table from combobox
        tblName = tab2.tablesCBox.currentText()
        pass
        
    def editRecord(self, gui):
        tab2 = gui.tab_widget.tab2
        query = gui.DB['query'] # or query = QSqlQuery() # would work too

        # lists of form lables and lineEdit boxes
        lableList = []
        editList = []

        # get selected table from combobox
        tblName = tab2.tablesCBox.currentText()
        # get selected item indexes of the table from tableView
        indexes = tab2.tblWidget.selectedIndexes()

        # check any row is selected from the table view
        if len(indexes) == 0:
            QMessageBox.critical(None, "Select a row",
                                 "Select a row from the table to edit.\n",
                                 QMessageBox.Ok)
            return

        # list to hold column data (columns are in the order of the table)
        cols = []

        # each columns data are stored in a dictionary
        for index in indexes:
            colDataDict = {}
            colName = tab2.tblWidget.model().headerData(index.column(), Qt.Horizontal)
            cellValue = tab2.tblWidget.model().data(index)
            colDataDict['index'] = index.column()
            colDataDict['name'] = colName
            colDataDict['oldValue'] = cellValue

            cols.append(colDataDict)

        # get table primary keys
        # adapeted from: http://pyqt.sourceforge.net/Docs/PyQt4/qtsql.html
        query.prepare("pragma table_info({});".format(tblName))
        # table_info output: [cid, name, type, notnull, dflt_value, pk  Val]
        #print "Query excuting on talbe: ", tblName, ".., result: ", query.exec_()
        
        while query.next():
            index = query.value(0)            
            cols[index]['type'] = query.value(2)
            cols[index]['notnull'] = query.value(3)
            cols[index]['dflt_value'] = query.value(4)
            cols[index]['pk'] = query.value(5)

        # Create where clause
        rowIdenfier = ["{} = '{}'".format(c['name'], c['oldValue']) for c in cols if c['pk']>0]
        cond = "WHERE " + " AND ".join(rowIdenfier)
            
        # submit changes function
        def submitChanges():
            # sqlquery to update record
            updateQuery = "UPDATE {} SET ".format(tblName)
            
            newdata=[]
            for i in range(len(cols)):
                # check for integer values
                newVal = editList[i].text()
                if cols[i]['type'] == "INTEGER":
                    try:
                        int(newVal)
                    except ValueError:
                        QMessageBox.critical(None, "Integer Required",
                                             "Column \"{}\" only accepts integer values\n".format(cols[i]['name']),
                                             QMessageBox.Ok)
                        return False
                # check for float values
                if cols[i]['type'] == "REAL":
                    try:
                        float(newVal)
                    except ValueError:
                        QMessageBox.critical(None, "Float Required",
                                             "Column \"{}\" only accepts floating point values\n".format(cols[i]['name']),
                                             QMessageBox.Ok)
                        return False
                newdata.append("{}='{}'".format(cols[i]['name'], newVal))

            updateQuery = updateQuery +  ", ".join(newdata) +" "+ cond + ";"

            query.prepare(updateQuery)

        # create dialog box
        diag = QDialog()
        diag.setWindowTitle("Edit Record")
        #diag.setWindowModality(Qt.ApplicationModal)

        # Main layout of the dialog box. (a vertical layout)
        mainLayout = QVBoxLayout(diag)

        # submit button: not enabled until make any changes to record data
        submit_btn = QPushButton("Submit",diag)
        submit_btn.setEnabled(False)
        submit_btn.clicked.connect(submitChanges)
        
        # enable button slot to be connected to all the lineEdit objects
        def enableSubmit():
            if not submit_btn.isEnabled():
                submit_btn.setEnabled(True)
                print " submit enabled"
        
        # groupbox for edit record form
        groupbox = QGroupBox('Edit Record:')

        # form layout to arrange lables and textboxes
        formLayout = QFormLayout()
        # set up form layout
        for i in range(len(cols)):
            if cols[i]['pk'] >0:
                lblText = cols[i]['name'] + "(PK)"
            else:
                lblText = cols[i]['name']
                
            lableList.append(QLabel(lblText))
            editList.append(QLineEdit())
            editList[i].setText(str(cols[i]['oldValue']))
            editList[i].textChanged.connect(enableSubmit)
            formLayout.addRow(lableList[i], editList[i])

        # set layout of groupbox
        groupbox.setLayout(formLayout)

        # Create a scrollable area to add the groupbox
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)

        # add scroll area to main layout
        mainLayout.addWidget(scroll)
        mainLayout.addStretch()
        # add submit button to main layout
        mainLayout.addWidget(submit_btn)

        # set layout of the dialog box
        diag.setLayout(mainLayout)
        diag.exec_()    


    def loadTable(self, gui):
        tblName = gui.tab_widget.tab2.tablesCBox.currentText()
        model = QSqlTableModel()
        model.setTable(tblName)
        model.select()

        gui.tab_widget.tab2.tblWidget.setModel(model)

                    
    def loadDB(self, gui):

        dbTab = gui.tab_widget.tab1
        tblTab = gui.tab_widget.tab2

        # set QtDatabase object
        gui.DB['db'] = QSqlDatabase.addDatabase('QSQLITE')

        # get table name from text box
        gui.DB['dbFileName'] = dbTab.dbName_edit.text()
        gui.DB['db'].setDatabaseName(gui.DB['dbFileName'])

        if not gui.DB['db'].open():
            QMessageBox.critical(None, "Cannot open database",
                                 "Unable to establish a database connection.\n",
                                 QMessageBox.Cancel)
            return False

        gui.DB['query'] = QSqlQuery()
        
        # get table list
        #gui.DB['query'].exec_("SELECT name FROM sqlite_master WHERE type='table';")
        gui.DB['tables'] = gui.DB['db'].tables()

        # populate table list box in left hand side
        dbTab.tableListwidget.clear()
        dbTab.tableListwidget.addItems(gui.DB['tables'])

        # set itemSelectionChanged signal of the table listbox to function 'updateRowList'
        #dbTab.tableListwidget.itemClicked.connect(self.updateRowList)
        dbTab.tableListwidget.itemSelectionChanged.connect(lambda: self.updateColumnList(gui))

        # populate combobox in tblTab
        tblTab.tablesCBox.clear()
        tblTab.tablesCBox.addItems(gui.DB['tables'])


        
    def updateColumnList(self, gui):
        dbTab = gui.tab_widget.tab1
        tblTab = gui.tab_widget.tab2

        # get selected table name 
        table_name = dbTab.tableListwidget.currentItem().text()

        # get table columns of the selected table
        #table_info = self.DB['query'].exec_('PRAGMA TABLE_INFO({});'.format(table_name))
        table_info = gui.DB['db'].record(table_name)

        col_names = []

        dbTab.colsListwidget.clear()
        # fill columns listbox
        for i in range(table_info.count()):
            colName = table_info.fieldName(i)
            col_names.append(colName)
            dbTab.colsListwidget.addItem(colName)
            #print "table_info.fieldName(i): ", table_info.fieldName(i), table_info.field(i).type()
            itemType = table_info.field(i).type()
            dbTab.colsListwidget.item(i).setToolTip("<p>Field: <b>{}</b></p><p>Type: <b>{}</b></p>".format(colName, itemType))


    
