# -*- coding: utf-8 -*-
"""
@author: Jayalath A M Madawa Abeywardhana
"""

import sqlite3

class DataBaseSqlite3(object):

    """
    
    create sqlite3 database  
   
    """

    def __init__(self, database='database.db'):
        
        """  Initialize a new database.  """

        # database filename
        self.database = database

        # indicates if selected data is to be returned or printed
        self.display = False

        self.connect()
        self.close()

    def connect(self):
        
        """ Connect to the SQLite3 database."""

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connected = True

    def close(self):
        
        """ Close the SQLite3 database."""

        self.connection.commit()
        self.connection.close()
        self.connected = False
        

    def execute(self, statement):
        
        """ Execute complete SQL statements"""

        queries = []
        
        close = False
        
        if not self.connected:
            
            self.connect()
            # mark the connection to be closed once complete
            close = True

        try:
            self.cursor.execute(statement)
            self.connection.commit()

            # retrieve selected data
            data = self.cursor.fetchall()
            if statement.upper().startswith('SELECT') or statement.upper().startswith('PRAGMA'):
                queries = data

        # handle duplicating primary keys error
        except sqlite3.IntegrityError as e:
            print('sqlite IntegrityError error: ', e.args[0])
            
        except sqlite3.Error as error:
            print 'An error occurred:', error.args[0]
            print 'For the statement:', statement

        # only close the connection if opened in this function
        if close:
            self.close()
        # print results for all queries
        if self.display:
            for result in queries:
                if result:
                    for row in result:
                        print row
                else:
                    print result
        #return results for all queries
        else:
            return queries
