import sqlite3
import discord
import emoji

def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False

def text_has_digits(s):
    return any(i.isdigit() for i in s)


class Error(Exception):
    pass

class TooLong(Error):

    """Prefix passed was too large.

    Attributes:
        prefix -- input expression in which the error occurred.
    """

    def __init__(self, prefix, message="Prefix passed was too large."):

        self.prefix = prefix
        self.message = message
        super().__init__(self.message)

class Emoji_in_Prefix(Error):

    """Prefix passed had an emoji.

    Attributes:
        prefix -- input expression in which the error occurred.
    """

    def __init__(self, prefix, message="Prefix had an emoji."):

        self.prefix = prefix
        self.message = message.capitalize
        super().__init__(self.message)

class Number_in_Prefix(Error):

    """Prefix passed had a number.

    Attributes:
        prefix -- input expression in which the error occurred.
    """

    def __init__(self, prefix, message="Number had an emoji."):

        self.prefix = prefix
        self.message = message.capitalize
        super().__init__(self.message)

class Database:

    def __init__(self):

        self.conn = sqlite3.connect('/root/alfonso/database/guild.db')
        self.cursor = self.conn.cursor()


class prefix(Database):

    def __init__(self, id: int):

        database = Database()
        self.conn = database.conn
        self.cursor = database.cursor
        self.prefixes = {}
        self.id = id

    @property
    def name(self):

        self.cursor.execute("SELECT prefix FROM guild_prefix WHERE id = ?", (self.id,))
        return self.cursor.fetchone()[0] 



    def modify(self, prefix: str):

        if not text_has_digits(prefix):
            if not text_has_emoji(prefix):

                if len(prefix) < 5:

                    self.cursor.execute("SELECT prefix FROM guild_prefix WHERE id = '%d'" % self.id)
                    if self.cursor.fetchone() is None:
                        self.cursor.execute(f"""
                        INSERT INTO guild_prefix (id, prefix)
                        VALUES ({self.id}, '{prefix}');""")
                        self.conn.commit() 
                    else:
                        self.cursor.execute(f"UPDATE guild_prefix SET prefix = '{prefix}' WHERE id = {self.id}")
                        self.conn.commit() 

                else:
                    if len(prefix) > 5:
                        raise TooLong(prefix)

            else:

                raise Emoji_in_Prefix(prefix)
        else:

            raise Number_in_Prefix(prefix)

    def create(self):

        self.cursor.execute("""
                            CREATE TABLE guild_prefix (
                                id int,
                                prefix varchar(255)
                            );  
                            """)


class Roles:

    def __init__(self):

        database = Database()
        self.conn = database.conn
        self.cursor = database.cursor

    def get(self, client, role, guild_id):
        
        try:
            
            if role == "mute":
                role = 'muted_role'

            self.cursor.execute(f"SELECT role_id FROM {role} WHERE id = '{int(guild_id)}'")
            guild = client.get_guild(guild_id)
            return guild.get_role(self.cursor.fetchone()[0])

        except Exception:
            
            return None


    def add(self, client, role_type, role: discord.Role, guild_id):

        guild = client.get_guild(int(guild_id))
        role_id = guild.get_role(role.id)

        
        if role_type == "mute":
            role_type = 'muted_role'
        elif role_type == "moderator":
            role_type = 'moderator_role'

        self.cursor.execute(f"SELECT role_id FROM {role_type} WHERE id = '{id}'")
        if not self.cursor.fetchone():

            self.cursor.execute(f"""
                INSERT INTO {role_type} (id, role_id)
                VALUES ({guild_id}, {role_id.id});""")

            self.conn.commit()
        
        else:

            self.cursor.execute(f"""
                UPDATE {role_type} SET role_id = {role_id} WHERE id = '{id}'""")
            self.conn.commit()
        
    def create(self):

        try:
            self.cursor.execute("""
                                CREATE TABLE muted_role (
                                    id int,
                                    role_id int
                                );
                                """)    
        except Exception as error:
            print(error)
        
        try:
            self.cursor.execute("""
                        CREATE TABLE moderator_role (
                            id int,
                            role_id int
                        );
                        """)
        except Exception as error:
            print(error)