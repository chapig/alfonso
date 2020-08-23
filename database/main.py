import pyodbc
import time
import json

class Database:



    def __init__(self):
        
        self.server = 'SERVER'
        self.database = 'DATABASE'
        self.username = 'USER'
        self.password = 'PASSWORD'
        self.driver= '{ODBC Driver 17 for SQL Server}'
        self.global_prefixes = {}


    def all(self, guild, id):

        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT balance, emeralds, timew, discord FROM B{guild} WHERE discord={id}")
        row = cursor.fetchone()
        cursor.execute(f"SELECT status, wt, currency FROM economys WHERE discord={guild}")
        status = cursor.fetchone()

        if status is not None:

            self.estado = status[0]
            self.wt = status[1]
            self.currency = status[2]

        else:

            sql = f"""INSERT INTO economys (discord, status, wt, currency)
                    VALUES ({guild}, '0', '0', '$');"""
            cursor.execute(sql)
            cnxn.commit()

            self.estado = 0
            self.wt = 0
            self.currency = '$'

        if row is not None and status is not None:
            
            self.balance = int(row[0])
            self.emeralds = int(row[1])
            self.timew = float(row[2])



    def balance_update(self, guild, id, total, bolsa):
        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        try:

            cursor.execute(f"SELECT balance, emeralds, timew, discord FROM B{guild} WHERE discord={id}")
            self.row = cursor.fetchone()

        except Exception:

            sql = f"""CREATE TABLE B{guild} (
                        balance int,
                        emeralds int,
                        timew float,
                        discord varchar(255));
                    """

            cursor.execute(sql)
            cnxn.commit()      
            self.balance_update(guild, id, total, bolsa)     

        if self.row is not None:

            sql = f"""UPDATE B{guild} SET balance= balance+{total}, emeralds= emeralds+{bolsa}, timew= {time.time()} WHERE discord = {id}"""
            cursor.execute(sql)
            cnxn.commit()

        else:
            
            sql = f"""INSERT INTO B{guild} (balance, emeralds, timew, discord)
                    VALUES (100, 1, 0, {id});"""
            cursor.execute(sql)
            cnxn.commit()


        cursor.execute(f"SELECT GuildID, Prefix from GuildC WHERE GuildID='{guild}'")
        self.lista = cursor.fetchone()

    def u_prefix(self, guild, prefix):
        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT Prefix FROM Guildc WHERE GuildID={guild}")
        row = cursor.fetchone()
        if row is not None:
            self.prefix = row[0]
            sql = f"""UPDATE GuildC SET Prefix = '{prefix}' WHERE GuildID = '{guild}'"""
            cursor.execute(sql)
            cnxn.commit()
        else:
            sql = f"""INSERT INTO GuildC (GuildID, Prefix)
            VALUES ('{guild}', '{prefix}');"""
            cursor.execute(sql)
            cnxn.commit()
        self.global_prefixes = self.update_all_prefixes()


    def update_all_prefixes(self):
        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT GuildID, Prefix FROM Guildc")
        rows = cursor.fetchall()
        rows = list(rows)
        prefixes = json.dumps(dict(rows))
        self.global_prefixes = json.loads(prefixes)
        return(json.loads(prefixes))
        
        
    

