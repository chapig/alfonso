
import sqlite3

class TTSData:

    def __init__(self):

        self.conn = sqlite3.connect('/root/alfonso/database/ttsglobal.db')
        self.cursor = self.conn.cursor()

    def fetch_user_election(self, user_id, guild_id):

        self.cursor.execute(f"SELECT language, gender FROM Member WHERE id = '{user_id}' AND guild = '{guild_id}'")
        return self.cursor.fetchone()

    def modify_user_election(self, user_id, guild_id, language, gender):

        self.cursor.execute(f"SELECT language, gender FROM Member WHERE id = '{user_id}' AND guild = '{guild_id}'")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"""
            INSERT INTO Member (id, guild, language, gender)
            VALUES ({user_id}, {guild_id}, '{language}', '{gender}');""")
            self.conn.commit() 
        else:
            self.cursor.execute(f"UPDATE Member SET language = '{language}', gender = '{gender}' WHERE id = {user_id}")
            self.conn.commit() 
    
class TTSGuild:

    def __init__(self):

        self.conn = sqlite3.connect('/root/alfonso/database/ttsglobal.db')
        self.cursor = self.conn.cursor()
    
    def modify_state(self, guild_id):

        self.cursor.execute(f"SELECT state FROM guild_state WHERE id = '{guild_id}'")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"""
            INSERT INTO guild_state (id, state)
            VALUES ({guild_id}, 0);""")
            self.conn.commit() 
        elif self.cursor.fetchone()[0] == 0:
            self.cursor.execute(f"UPDATE guild_state SET state = 1 WHERE id = '{guild_id}'")
            self.conn.commit() 
        elif self.cursor.fetchone()[0] == 1:
            self.cursor.execute(f"UPDATE guild_state SET state = 0 WHERE id = '{guild_id}'")
            self.conn.commit() 

    
    def fetch_state(self, guild_id):

        self.cursor.execute(f"SELECT state FROM guild_state WHERE id = {guild_id}")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"""
            INSERT INTO guild_state (id, state)
            VALUES ({guild_id}, 0);""")
            self.conn.commit() 
        else:
            print(self.cursor.fetchone())
        return self.cursor.fetchone()
    
    def activate_music(self, guild_id):

        self.cursor.execute(f"SELECT state FROM guild_state WHERE id = '{guild_id}'")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"""
            INSERT INTO guild_state (id, state)
            VALUES ({guild_id}, 2);""")
            self.conn.commit() 
        else:
            self.cursor.execute(f"UPDATE guild_state SET state = 2 WHERE id = '{guild_id}'")
            self.conn.commit() 

    def deactivate_music(self, guild_id):

        self.cursor.execute(f"SELECT state FROM guild_state WHERE id = '{guild_id}'")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"""
            INSERT INTO guild_state (id, state)
            VALUES ({guild_id}, 0);""")
            self.conn.commit() 
        else:
            self.cursor.execute(f"UPDATE guild_state SET state = 0 WHERE id = '{guild_id}'")
            self.conn.commit() 