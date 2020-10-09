import sqlite3, asyncio, random, discord, wikipedia, os, requests, uuid, json, random, json, time, traceback

def Embed(title=None, description=None, footer=None, author=None, author_img= None, thumbnail=None, color=None):

    embed = discord.Embed(

        title = title,
        description = description,
        color = color if color else None
    )

    embed.set_footer(text=footer) if footer else None
    
    embed.set_author(name=author, icon_url=author_img) if author and author_img else None

    embed.set_thumbnail(url=thumbnail) if thumbnail else None

    return embed

def random_selection():

    list_selection = ['ies', 'os', 'ión', 'ler', 'por', 'ño', 'ña', 've', 'zu', 
    'sero', 'mort', 'tup', 'mot', 'com', 'loco', 'lla', 'mili', 
    'gue', 'ku', 'tra', 'tro', 'pro', 'ye', 'za']

    return random.choice(list_selection)

def wiki(srch: str):

    try:

        wikipedia.summary(srch, sentences=1)
        return True

    except Exception:

        return False

class Language:

    def __init__(self):

        self.key_var_name = 'cb20e4a7b5414aee86332eaa964d9736'
        self.endpoint = 'https://api.cognitive.microsofttranslator.com'

    def get(self, text):

        headers = {
            'Ocp-Apim-Subscription-Key': self.key_var_name,
            'Ocp-Apim-Subscription-Region': 'southcentralus',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        try:
            path = '/translate?api-version=3.0'
            params = f'&to=en'
            constructed_url = self.endpoint + path + params

            body = [{
                    'text': f'{text}'
                    }]

            request = requests.post(constructed_url, headers=headers, json=body)
            response = request.json()

            return(response[0]['detectedLanguage']['language'])
        except Exception:
            return None

class MESSAGES:

    def winning(self, word, points):

        return Embed(title=None,
                    description=f"**{word.capitalize()}** es una palabra, has ganado un punto. Ahora posees **{points}** puntos.",
                    color=discord.Color.green())
    
    def already_exists(self, word, points):

        return Embed(title=None,
                    description=f"**{word.capitalize()}** ya existe, has perdido un punto. Ahora posees **{points}** puntos.",
                    color=discord.Color.gold())
    
    def inexistent(self, word, points):

        return Embed(title=None,
                    description=f"**{word.capitalize()}** no existe, has perdido un punto. Ahora posees **{points}** puntos.",
                    color=discord.Color.red())

    def timeout(self, points):

        return Embed(title=None,
            description=f"**Tardaste mucho tiempo**, has perdido un punto. Ahora posees **{points}** puntos.",
            color=discord.Color.red())


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
                            SELECT score FROM \"_{self.game_id}\" WHERE id = ?
                            """, (discord_id, ))
        
        return self.cursor.fetchone()[0]


    def add_score(self, discord_id: int):

        self.cursor.execute(f"UPDATE \"_{self.game_id}\" SET score = score+1 WHERE id = ?", (discord_id, ))
        self.conn.commit()


    def remove_score(self, discord_id: int):

        self.cursor.execute(f"UPDATE \"_{self.game_id}\" SET score = score-1 WHERE id = ?", (discord_id, ))
        self.conn.commit()

    def add_player(self, discord_id: int):

        self.cursor.execute(f"""
                            INSERT INTO _{self.game_id} (id, score)
                            VALUES (?, ?);
                            """, (discord_id, 0))
        self.count += 1

    def all_players(self):

        self.cursor.execute(f"SELECT id FROM _{self.game_id}")
        return self.cursor.fetchall()
    
    def winner(self):

        self.cursor.execute(f"SELECT MAX(score) FROM \"_{self.game_id}\" GROUP BY id;")
        winner = self.cursor.fetchone()[0]
        self.cursor.execute(f"SELECT id FROM \"_{self.game_id}\" WHERE score = ?", (winner, ))
        winner = self.cursor.fetchone()[0]
        return winner

class GAME:

    def __init__(self, client, ctx, players):

        self.db = Database()
        self.lang = Language()
        self.MESSAGES = MESSAGES()
        self.client = client
        self.ctx = ctx
        self.words_said = []
        self.round = 0
        self.users = players

    def save_players(self, all_players):

        self.players = all_players
        self.current_order_of_players = [0, len(self.players) - 1]

    def set_rounds(self, rondas):

        self.all_rounds = rondas

    def update_scoreboards(self):

        if self.current_order_of_players[0] == self.current_order_of_players[1]:
            self.round += 1
            self.current_order_of_players[0] = 0
        else:
            self.round += 1
            self.current_order_of_players[0] += 1

    async def start(self):

        try:
            if self.all_rounds == 0:

                raise Exception("Rounds haven't been defined yet, in order to start, define it.")

            else:

                self.round == 1

            if self.round == self.all_rounds:
                
                await self.ctx.send(embed=Embed(title=None, 
                                                description="El juego terminó, gracias por jugar. El **ganador** es {} con **{}** puntos. \n{}".format(self.ctx.guild.get_member(self.users.winner()).mention, 
                                                                                                                                                       self.users.score(self.users.winner()),                                                                                                          
                                                color=discord.Color.gold()
                                                ))
                
                self.round = 1000

                guild = Guild(self.ctx.guild.id)
                guild.remove_table(self.ctx.channel.id)

                return

            while self.round <= self.all_rounds:

                #Defining next player.

                self.player = self.players[self.current_order_of_players[0]][0]
                self.player = self.ctx.guild.get_member(int(self.player))
                #####################################

                #Random termination.
                self.termination = random_selection()
                ###############################################

                def check(m):
                    return self.termination.upper() in m.content.upper() and m.channel == self.ctx.channel and m.author.id == self.player.id

                ################################################

                m = await self.ctx.send(embed=Embed(
                                                title=f"Es ahora el turno de {self.player.name}.",
                                                description=f"Escribe una palabra con la siguiente terminación {self.termination.upper()}.",
                                                color=discord.Color.blurple(),
                                                footer="Ronda {} de {} | TeaWord".format(self.round, self.all_rounds)
                                                ))


                message = await self.client.wait_for('message', timeout=10.0, check=check)
                self.message = message.content.split(" ")

                #################################################

                await m.delete() #Delete previous message.

                ##################################################
 
                if self.lang.get(self.message[0]) == 'es' and self.message[0].upper() not in self.words_said:

                    await message.add_reaction("☑️")
                    self.users.add_score(self.player.id)
                    await self.ctx.send(embed=self.MESSAGES.winning(self.message[0], self.users.score(self.player.id)))
                    self.update_scoreboards()

                elif wiki(self.message[0]) and self.message[0].upper() not in self.words_said:

                    await message.add_reaction("☑️")
                    self.users.add_score(self.player.id)
                    await self.ctx.send(embed=self.MESSAGES.winning(self.message[0], self.users.score(self.player.id)))
                    self.update_scoreboards()

                elif self.message[0].upper() in self.words_said:

                    await message.add_reaction("🔅")
                    self.users.remove_score(self.player.id)
                    await self.ctx.send(embed=self.MESSAGES.already_exists(self.message[0], self.users.score(self.player.id)))
                    self.update_scoreboards()
                                
                else:

                    await message.add_reaction("🤔")
                    self.users.remove_score(self.player.id)
                    await self.ctx.send(embed=self.MESSAGES.inexistent(self.message[0], self.users.score(self.player.id)))
                    self.update_scoreboards()
                    
                ##################################################

                if self.round <= self.all_rounds:
                    await self.start()
                else:
                    await self.ctx.send("El juego terminó, gracias por jugar. El ganador es {} 2".format(self.ctx.guild.get_member(self.users.winner()).mention))
                    return

        except asyncio.exceptions.TimeoutError:

            if self.round <= self.all_rounds:
                await self.start()
                await self.ctx.send(embed=self.MESSAGES.timeout(self.users.score(self.player.id)))
                self.update_scoreboards()
            else:
                await self.ctx.send("El juego terminó, gracias por jugar. El ganador es {} 1".format(self.ctx.guild.get_member(self.users.winner()).mention))
                return
