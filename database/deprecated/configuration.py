import pyodbc
import json

class connection():

    def __init__(self):

        self.server = 'SERVER'
        self.database = 'DATABASE'
        self.username = 'USER'
        self.password = 'PASSWORD'
        self.driver= '{ODBC Driver 17 for SQL Server}'

        self.get_muted_roles()

    def everything(self, guild):

        try:
            cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
            cursor = cnxn.cursor()
            sql = f"""INSERT INTO GuildC (GuildID, Prefix, Moderators, MutedRole)
            VALUES ('{guild}', '$', '0', '0');"""
            cursor.execute(sql)
            cursor.commit()
        except Exception as error:
            print(error)

    def get_muted_roles(self):

        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT GuildID, MutedRole FROM GuildC")
        row = cursor.fetchall()
        row = list(row)
        if row is not None:
            mute_roles = json.dumps(dict(row))
            self.muted_roles =  json.loads(mute_roles)
        else:
            return None

    def update_mute_role(self, guild, _role):

        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT * FROM GuildC WHERE GuildID={guild}")
        row = cursor.fetchall()
        try:
            if row is not None:
                sql = f"""UPDATE GuildC SET MutedRole = '{_role}' WHERE GuildID = '{guild}'"""
                cursor.execute(sql)
                cursor.commit()
            else:
                self.everything(guild)
                self.update_mute_role(guild, _role)
        except Exception as error:
            print(error)


    def update_moderators(self, guild, _role):

        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT Moderators FROM GuildC WHERE GuildID={guild}")
        row = cursor.fetchone()
        if row is not None:
            sql = f"""UPDATE GuildC SET Moderators = '{_role}' WHERE GuildID = '{guild}'"""
            cursor.execute(sql)
            cursor.commit()
        else:
            self.everything(guild)
            self.update_moderators(guild, _role)

    def get_mod_roles(self, guild=None):

        cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT GuildID, Moderators FROM GuildC")
        row = cursor.fetchall()
        if row is not None:
            row = list(row)
            mute_roles = json.dumps(dict(row))
            self.mod_roles = json.loads(mute_roles)
            if guild:
                print("Hola aki")
                print(guild)
                print(self.mod_roles[guild])
                print(self.mod_roles[str(guild)])
                return self.mod_roles[str(guild)]
        else:
            return None
