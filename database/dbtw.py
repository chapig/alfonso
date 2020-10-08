import sqlite3, asyncio, random

class Database:

    def __init__(self):

        self.conn = sqlite3.connect('/home/azureuser/python/python/games/database/points_tw.db', timeout=1)
        self.cursor = self.conn.cursor()

    def close(self):

        self.cursor.close()

class Guild:

    def __init__(self, guild_id: int):
        
        self.guild_id = guild_id
        self.db = Database()

    def create_table(self, channel_id: str):
        
        self.game_id = str(self.guild_id)[0:4] + str(channel_id)[0:2] #ID OF GAME
        self.db.cursor.execute(f"""
                            CREATE TABLE _{self.game_id} (
                                id int,
                                score int,
                                UNIQUE(id)
                            );
                            """)
        self.db.cursor.close()
        return self.game_id


    def remove_table(self, channel_id: str):

        self.game_id = str(self.guild_id)[0:4] + str(channel_id)[0:2]
        self.db.cursor.execute(f"""
                            DROP TABLE _{self.game_id}
                            """)
        self.db.cursor.close()
        return self.game_id

    def temporal_stop(self):

        self.db.conn.close()
        print("DB closed.")


class Users:

    def __init__(self, game_id: str):

        database = Database()
        self.game_id = game_id
        self.conn = database.conn
        self.cursor = database.cursor
        self.count = 0

    def score(self, discord_id):

        self.cursor.execute(f"""
                            SELECT score FROM _{self.game_id} WHERE id = ?
                            """, (discord_id))
        
        return self.cursor.fetchone()[0]

    def add_score(self, discord_id: int):

        self.cursor.execute(f"UPDATE _{self.game_id} SET score = score+1 WHERE id = ?", (discord_id))
            
    def add_player(self, discord_id: int):

        self.cursor.execute(f"""
                            INSERT INTO _{self.game_id} (id, score)
                            VALUES (?, ?);
                            """, (discord_id, 0))
        self.count += 1

    def all_players(self):

        self.cursor.execute(f"SELECT id FROM _{self.game_id}")
        return self.cursor.fetchall()

class GAME:

    def __init__(self, client, ctx):

        self.client = client
        self.ctx = ctx
        self.rounds = 0
        self.db = Database()


    async def start(self):

        if self.rounds == 0:
            raise Exception("Rounds haven't been defined yet, in order to start, define it.")
        
        while rounds <= self.rounds:
