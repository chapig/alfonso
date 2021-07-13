import pyodbc

class experience:

    def __init__(self):

        self.server = 'SERVER'
        self.database = 'DATABASE'
        self.username = 'USER'
        self.password = 'PASSWORD'
        self.driver= '{ODBC Driver 17 for SQL Server}'


    def checkif(self, id):
        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT exp, level FROM exp_global WHERE discord={id}")
        try:
            row = cursor.fetchone()
            if row is not None:
                self.status = True
            else:
                self.status = False
            if row[0] is not None:
                return(int(row[0]),row[1], True)
        except Exception:
            return False, False
    
    def update(self, id: int, amount: str):
        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        try:
            self.checkif(id)
        except:
            self.insert(id)
        if self.status is not None:
            cursor.execute(f"UPDATE exp_global SET exp= exp+{amount} WHERE discord = {id}")
            cursor.execute(f"UPDATE exp_global SET level= level+1 WHERE discord = {id}")
            cnxn.commit()
            cursor.execute(f"SELECT level FROM exp_global WHERE discord={id}")
            row = cursor.fetchone()
            return row
        


    def insert(self, id):
        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        try:
            sql = f"""INSERT INTO exp_global (exp, discord)
                    VALUES (0, '{id}');"""
            cursor.execute(sql)
            cnxn.commit()
        except Exception as error:
            raise Exception(error)

