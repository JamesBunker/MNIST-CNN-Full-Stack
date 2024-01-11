import os
import sqlite3
import mxarr

class Database():
    #sqlite connection class attribute
    conn = None
    def __init__(self, reset=False):
        #if reset is triggered remove database
        if (reset):
            if os.path.exists('mxarr.db'):
                os.remove('mxarr.db')
        #connect to database
        self.conn = sqlite3.connect('mxarr.db')
        self.conn.execute("pragma journal_mode=OFF")
        return
    
    def create_tables(self):
        #creating Arrays table if it does not exist
        sql = """create table if not exists Arrays 
                 ( NAME VARCHAR(64) NOT NULL,
                   DIMNO INTEGER NOT NULL,
                   DATATYPE INTEGER NOT NULL,
                   DIMS0 INTEGER NOT NULL,
                   DIMS1 INTEGER NOT NULL,
                   ELNO INTEGER NOT NULL,
                   PRIMARY KEY (NAME) );"""
        self.conn.execute(sql)

        #creating DoubleData table if it does not exist
        sql = """create table if not exists DoubleData 
                 ( ARRAYNAME    VARCHAR(64) NOT NULL,
                   I            INTEGER NOT NULL,
                   J            INTEGER NOT NULL,
                   VALUE        FLOAT NOT NULL,
                   PRIMARY KEY (ARRAYNAME,I,J),
                   FOREIGN KEY (ARRAYNAME) REFERENCES Arrays(NAME) );"""
        self.conn.execute(sql)

        #creating IntegerData table if it does not exist
        sql = """create table if not exists IntegerData 
                 ( ARRAYNAME    VARCHAR(64) NOT NULL,
                   I            INTEGER NOT NULL,
                   J            INTEGER NOT NULL,
                   VALUE        INTEGER NOT NULL,
                   PRIMARY KEY (ARRAYNAME,I,J),
                   FOREIGN KEY (ARRAYNAME) REFERENCES Arrays(NAME) );"""
        self.conn.execute(sql)
        self.conn.commit()

        return
    
    def __setitem__(self, table, values):
        #adding arr attributes to Arrays table
        if (table == "Arrays"):
            #adding arr attributes to Arrays table
            sql =  """INSERT INTO   Arrays (NAME, DIMNO, DATATYPE, DIMS0, DIMS1, ELNO)
                              VALUES        ( ?, ?, ?, ?, ?, ? );"""
            self.conn.execute(sql, values)

        if (table == "DoubleData"):
            sql =  """INSERT INTO   DoubleData 
                        VALUES        ( ?, ?, ?, ?);"""
            self.conn.execute(sql,values)
        if (table == "IntegerData"):
            sql =  """INSERT INTO   IntegerData 
                        VALUES        ( ?, ?, ?, ?);"""
            self.conn.execute(sql,values)
        self.conn.commit()
        
        return

    def store_arr(self, arrname, arr):
        #if (arr.dimno != 2):
        #    arr.ERROR_CODE = arr.ERR_VALUE
        #    return
  
        #adding arr attributes to Arrays table
        try:
            self.__setitem__("Arrays", [arrname,arr.dimno,arr.type, arr.getdim(0), arr.getdim(1),arr.elno])
        except:
            print("caught")
        
        #adding values of arr to IntegerData or DoubleData depending on type
        if (arr.type ==  mxarr.DOUBLE_TYPE or arr.type ==  mxarr.FLOAT_TYPE):
            for i in range(arr.getdim(0)):
                for j in range(arr.getdim(1)):
                    self["DoubleData"] = [arrname,i,j,float(arr[i,j])]
        else:
            for i in range(arr.getdim(0)):
                for j in range(arr.getdim(1)):
                    self["IntegerData"] = [arrname,i,j,int(arr[i,j])]
        #self.conn.commit()

        return
    
    def retrieve_arr(self, arrname):
        print(arrname)
        array_params_list = []
        array_data = []
        sql = """SELECT * FROM Arrays WHERE NAME = '{}';"""
        array_params = self.conn.execute(sql.format(arrname)).fetchall()
        for i in array_params:
            for item in i:
                array_params_list.append(item)
        array_params = array_params_list
        arr = mxarr.Array( array_params[5], array_params[2])
        arr.inflate( array_params[4] )

        if (arr.type == mxarr.INT_TYPE or arr.type ==  mxarr.UCHAR_TYPE):
            sql = """SELECT * FROM IntegerData WHERE ARRAYNAME='{}';"""
            array_data = self.conn.execute(sql.format(arrname)).fetchall()
        elif (arr.type == mxarr.DOUBLE_TYPE):
            sql = """SELECT * FROM DoubleData WHERE ARRAYNAME='{}';"""
            array_data = self.conn.execute(sql.format(arrname)).fetchall()
        array_data = [list(row) for row in array_data]

        for i in range(len(array_data)):
            arr[array_data[i][1],array_data[i][2]] = array_data[i][3]
        return arr

    def clear_tables(self):
        #deleting Arrays rows
        sql = 'DELETE FROM Arrays;'
        self.conn.execute(sql)
        
        #deleting DoubleData rows
        sql = 'DELETE FROM DoubleData;'
        self.conn.execute(sql)

        #deleting IntegerData rows
        sql = 'DELETE FROM IntegerData;'
        self.conn.execute(sql)
        
        self.conn.commit()

        return

    def listarr (self):
        array_list = []
        sql = "SELECT NAME FROM Arrays;"
        array_params = self.conn.execute(sql).fetchall()
        for i in array_params:
            for item in i:
                array_list.append(item)

        return array_list
    
    def deletearr (self, name):
        sql = "DELETE FROM Arrays WHERE NAME = '%s';" % name
        self.conn.execute(sql)
        self.conn.commit()

    def close (self):
        self.conn.close()
        return
