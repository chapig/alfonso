import discord
from discord.ext import commands
import json
import asyncio
import time
import nltk
from nltk.tokenize import sent_tokenize
import os, requests, uuid, json
import random
import wikipedia
import pandas as pd
import heapq
import traceback

class Language:

    def __init__(self):

        self.key_var_name = 'KEY'
        self.endpoint = 'ENDPOINT'

    def get_language(self, text):

        headers = {
            'Ocp-Apim-Subscription-Key': self.key_var_name,
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


class GameCache:

    def __init__(self):

        self.guild = {}
        self.users = {}
        self.score = {}
        self.temp_list = []
        self.order_list = {}

    def initiate_game(self, g):

        self.guild[str(g)] = True

    def add_user(self, guild, user):
        """
        Añadir miembro a lista temporal.
        """

        self.temp_list.append(str(user))

    def save_users(self, guild, usuarios):
        """
        Guardar usuarios después de todos los miembros entrar a la lista. La lista es creada en temp_list de la función add_player
        """
        try:
            self.users[str(guild)] = {}
        except Exception as error:
            print("Ocurrió error.", error)
        try:
            for i in range(0,len(usuarios)):
                self.users[str(guild)][str(usuarios[i])] = {}
                self.users[str(guild)][str(usuarios[i])] = 0
                print(self.users[str(guild)][str(usuarios[i])], "Este usuario posee estos puntos.")
        except Exception as error:
            print(error, "Ocurrío un error al crear usuarios customizados por guild score. ")

        try:
            self.order_list[str(guild)] = []

            for i in range(0, len(usuarios)):
                self.order_list[str(guild)].append(usuarios[i]) 
                print(self.order_list[str(guild)], "Esta es la lista de orden.")
                print("Se añadió a este jugador al orden listado.")   
            
        except Exception as error:
            print(error, "Ocurrió error al intentar crear el orden.")

        self.temp_list.clear()

    
    def random_selection(self):

        list_selection = ['ies', 'os', 'ión', 'ler', 'por', 'ño', 'ña', 've', 'zu', 
        'sero', 'mort', 'tup', 'mot', 'com', 'loco', 'lla', 'mili', 
        'gue', 'ku', 'tra', 'tro', 'pro', 'ye', 'za']

        length = len(list_selection) - 1

        numero = random.choice(range(0,length))
        
        return list_selection[numero]

    def initiate_score_section(self, guild, user):

        self.users[str(guild)] = {}
        self.users[str(guild)][str(user)] = {}

    def add_score(self, user, guild):

        try:
            self.users[str(guild)][str(user)] += 1
            print(self.users[str(guild)][str(user)])
        except Exception:
            self.users[str(guild)][str(user)] = 1
            print(self.users[str(guild)][str(user)])
        return(self.users[str(guild)][str(user)])

    def remove_score(self, user, guild):

        try:
            self.users[str(guild)][str(user)] -= 1
            print(self.users[str(guild)][str(user)])
        except Exception:
            self.users[str(guild)][str(user)] = 0
            print(self.users[str(guild)][str(user)])
        return(self.users[str(guild)][str(user)])
    
    def total_keys(self, test_dict): 
      return (0 if not isinstance(test_dict, dict)  
      else len(test_dict) + sum(self.total_keys(val) for val in test_dict.values()))  
      
    def check_duplicate(self, listOfElems):
    
        if len(listOfElems) == len(set(listOfElems)):
            return False
        else:
            return True

    def results(self, guild):

        second = None
        third = None

        try:
            print(self.users[str(guild)]) 
            first = max(self.users[str(guild)], key=self.users[str(guild)].get)
            
            if self.total_keys(self.users[str(guild)]) > 1:

                try:
                    self.users[str(guild)].pop(str(first), None)
                    second = max(self.users[str(guild)], key=self.users[str(guild)].get)
                except Exception:
                    second = False

            if self.total_keys(self.users[str(guild)]) > 2:
                try:
                    self.users[str(guild)].pop(str(second), None)
                    third = max(self.users[str(guild)], key=self.users[str(guild)].get)
                except Exception:
                    third = False
            
            duplicate = False
            return duplicate, first, second, third
        except Exception as error:
            print("Hubo un error en result", error)


class Juegos(commands.Cog):

    
    def __init__(self, client):

        self.client = client
        self.game_cache = GameCache()
        self.get_language = Language()
        self.already_said = {}
        self.score_all = {}
        self.round = {}
        self.lista = {}
        self.already_said = {}
        self.total_players = {}
        self.started = {}

    def check(self, reaction, user):
        return str(reaction.emoji) == '🎮' and self.alfonso != user
    
    def new_check(self, m):
        return self.detection_part.upper() in m.content.upper() and m.channel == self.channel and m.author.id == self.random_user_id
    
    async def loop_started(self, ctx, channel, initiz, initial_round, max_round, order):
    
        self.channel = channel
        while self.started[str(ctx.guild.id)] is True:

            if self.started[str(ctx.guild.id)] is False:
                break

            if initial_round <= max_round:
                print("Ronda {} de {}".format(initial_round, max_round))
                print("Comenzando loop.")
                print("Orden actual: {}".format(order))
                print("Jugadores totales: {}".format(self.total_players[str(ctx.guild.id)]))

                if initiz == 1:
                    if order <= self.total_players[str(ctx.guild.id)]: 
                        order = order + 1



                self.detection_part = self.game_cache.random_selection()

                try:
                    self.random_user_id = self.lista[str(ctx.guild.id)][order]
                    self.random_user_id = int(self.random_user_id)
                except Exception as error:
                    print("No se pudo obtener usuario random.", error)

                self.user_now = ctx.guild.get_member(int(self.random_user_id))
                guild_servidor = self.client.get_guild(625860423144570902)
                embed = discord.Embed(title="", description=f"{self.user_now.mention} escribe una palabra que contenga: **{self.detection_part.upper()}**.", color=discord.Color.blue())
                embed.set_author(name="Tienes 10 segundos para responder.", icon_url='https://upload.wikimedia.org/wikipedia/commons/a/ad/YouTube_loading_symbol_3_(transparent).gif')
                mensaje = await ctx.send(content=f"{self.user_now.mention}", embed=embed)
             
                try:

                    message = await self.client.wait_for('message', timeout=10.0, check=self.new_check)
                    await mensaje.delete()
                    try:
                        tokenization = message.content.split(" ")
                        if self.get_language.get_language(tokenization[0]) == 'es' and tokenization[0].upper() not in self.already_said[str(ctx.guild.id)]:
                            await message.add_reaction("☑️")
                            score = self.game_cache.add_score(self.random_user_id, ctx.guild.id)
                            embed = discord.Embed(title="", description=f"{self.user_now.mention} ha anotado un punto más. Ahora tiene **{score}** puntos.", color=discord.Color.gold())
                            await ctx.send(embed=embed, delete_after=15)
                            self.already_said[str(ctx.guild.id)].append(tokenization[0].upper())
                            if order == self.total_players[str(ctx.guild.id)]:
                                initiz = 0
                                order = 0
                                initial_round += 1 
                            else:
                                initiz = 1

                            await self.loop_started(ctx, channel, initiz, initial_round, max_round, order)


                        else:
                            if self.get_language.get_language(tokenization[0]) == 'es' and tokenization[0].upper() in self.already_said[str(ctx.guild.id)]:
                                first = tokenization[0]
                                first = first[0].upper()
                                score = self.game_cache.remove_score(self.random_user_id, ctx.guild.id)
                                embed = discord.Embed(title="", description=f"**{first + tokenization[0][1:]}** ya ha sido usado antes. No lo puedes usar nuevamente. Pierdes este turno y un punto.\nAhora tienes **{score}**.", color=discord.Color.red())
                                await ctx.send(content=f"{self.user_now.mention}", embed=embed, delete_after=15)
                                await message.add_reaction("🔅")
                                if order == self.total_players[str(ctx.guild.id)]:
                                    initiz = 0
                                    order = 0
                                    initial_round += 1
                                else:
                                    initiz = 1
                            else:
                                try:
                                    
                                    if tokenization[0].upper() not in self.already_said[str(ctx.guild.id)]:
                                        x = wikipedia.summary(tokenization[0], sentences=1)
                                        score = self.game_cache.add_score(self.random_user_id, ctx.guild.id)
                                        await message.add_reaction("☑️")
                                        embed = discord.Embed(title="", description=f"{self.user_now.mention} ha anotado un punto más. Ahora tiene **{score}** puntos.", color=discord.Color.gold())
                                        await ctx.send(embed=embed, delete_after=15)
                                        self.already_said[str(ctx.guild.id)].append(tokenization[0].upper())
                                        if order == self.total_players[str(ctx.guild.id)]:
                                            initiz = 0
                                            order = 0
                                            initial_round += 1 
                                        else:
                                            initiz = 1
                                    else:
                                        if tokenization[0].upper() in self.already_said[str(ctx.guild.id)]:
                                            first = tokenization[0]
                                            first = first[0].upper()
                                            score = self.game_cache.remove_score(self.random_user_id, ctx.guild.id)
                                            embed = discord.Embed(title="", description=f"**{first + tokenization[0][1:]}** ya ha sido usado antes. No lo puedes usar nuevamente. Pierdes este turno y un punto.\nAhora tienes **{score}**.", color=discord.Color.red())
                                            await ctx.send(content=f"{self.user_now.mention}", embed=embed, delete_after=15)
                                            await message.add_reaction("🔅")
                                            if order == self.total_players[str(ctx.guild.id)]:
                                                initiz = 0
                                                order = 0
                                                initial_round += 1 
                                            else:
                                                initiz = 1
                                except Exception as error:
                                    await message.add_reaction("🤔")
                                    first = tokenization[0]
                                    first = first[0].upper()
                                    score = self.game_cache.remove_score(self.random_user_id, ctx.guild.id)
                                    embed = discord.Embed(title="", description=f"**{first + tokenization[0][1:]}** no existe. **Pierdes un punto.** \nAhora tienes **{score}** puntos.", color=discord.Color.red())
                                    await ctx.send(content=f"{self.user_now.mention}", embed=embed, delete_after=15)
                                    if order == self.total_players[str(ctx.guild.id)]:
                                        initiz = 0
                                        order = 0
                                        initial_round += 1
                                    else:
                                        initiz = 1
                            await self.loop_started(ctx, channel, initiz, initial_round, max_round, order)
                    except Exception as error:
                        await ctx.send("Lastimosamente ha ocurrido un error al continuar el juego. Este juego está en fase **beta**, por lo tanto puede que hayan errores por un corto periodo de tiempo.")

                except asyncio.TimeoutError:
                    score = self.game_cache.remove_score(self.random_user_id, ctx.guild.id)
                    embed = discord.Embed(title="", description=f"Has tardado mucho tiempo en responder, pierdes un punto. Piensa más rápido la próxima ronda!\nAhora posees **{score}**.", color=discord.Color.red())
                    await ctx.send(content=f"{self.user_now.mention}", embed=embed, delete_after=15)
                    if order == self.total_players[str(ctx.guild.id)]:
                        initiz = 0
                        order = 0
                        initial_round += 1
                    else:
                        initiz = 1
                    await self.loop_started(ctx, channel, initiz, initial_round, max_round, order)
            else:
                self.repeat = 0
                if self.game_cache.results(ctx.guild.id)[0]:
                    if self.repeat == 0:
                        self.repeat = 1
                        initial_round -= 1
                        await ctx.send(":robot: Hubo un empate, aquí va otra ronda.")
                        await self.loop_started(ctx, channel, initiz, initial_round, max_round, order)
                else:
                    first = ctx.guild.get_member(int(self.game_cache.results(ctx.guild.id)[1]))
                    try:
                        second = ctx.guild.get_member(int(self.game_cache.results(ctx.guild.id)[2]))
                    except Exception:
                        second = None
                    try:
                        third = ctx.guild.get_member(int(self.game_cache.results(ctx.guild.id)[3]))
                    except Exception:
                        third = None
                    embed = discord.Embed(title=f":crossed_swords: Resultados de TeaWord", description=f"**Posiciones finales:**\n\n:first_place: {first.mention}\n:second_place: {second.mention if second else '**Ningún jugador.**'}\n:third_place: {third.mention if third else '**Ningún jugador.**'}", color=discord.Color.gold())
                    #embed = discord.Embed(title=f":crossed_swords: La batalla ha terminado.", description=f"De todos los **{self.total_players + 1}** que jugaron, el ganador de esta partida es {ganador.mention}. Felicidades para esta increíble persona.", color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    try:
                        self.round = 1000
                        time.sleep(1)
                        self.started[str(ctx.guild.id)] = False
                        self.game_cache.guild[str(ctx.guild.id)] = False
                    except Exception as error:
                        print(error, "ocurrió un error al comenzar loop.")
            

    @commands.group()
    async def teaword(self, ctx):
        """
        **TeaWord** es un juego de palabras, el bot le dará una terminación aleatoria a un miembro y este tendrá que escribir una palabra con ella.
        
        **Utilización:**

        ``$teaword start 10`` 
        El ``10`` en este caso significa cuántas rondas serán.

        ``$teaword quit``
        Este comando sirve para parar el juego.
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=f"", description=f"{ctx.command.help}", color=discord.Color.red())
            await ctx.send(embed=embed)

    @teaword.command()
    async def start(self, ctx, rnd: int):
        """
        **TeaWord** es un juego de palabras, el bot le dará una terminación aleatoria a un miembro y este tendrá que escribir una palabra con ella.
        
        **Utilización:**

        ``$teaword start 3`` 
        El ``3`` en este caso significa cuántas rondas serán.

        ``$teaword quit``
        Este comando sirve para parar el juego.
        """
        try:
            if self.game_cache.guild[str(ctx.guild.id)]:
                self.game_cache.guild[str(ctx.guild.id)] = self.game_cache.guild[str(ctx.guild.id)]
        except Exception:
            self.game_cache.guild[str(ctx.guild.id)] = False

        if rnd <= 10:

            try:
                
                try:

                    if self.game_cache.guild[str(ctx.guild.id)]:

                        await ctx.send("El juego ya ha comenzado.")
                    
                    else:


                        if rnd == 0:
                            rnd = 1
                            await ctx.message.add_reaction("🔏")
                            await ctx.send(f":lock:{ctx.author.mention} No puedes colocar **0** rondas, se ha colocado como rondas **1** automáticamente.", delete_after=5)

                        elif rnd < 0:
                            await ctx.message.add_reaction("🔏")
                            await ctx.send(f":lock:{ctx.author.mention} No puedes colocar **{rnd}** rondas, se ha colocado como rondas **1** automáticamente.", delete_after=5)
                            rnd = 1


                        order = 0
                        initiz = 0
                        initial_round = 0
                        max_round = rnd

                        self.game_cache.initiate_game(ctx.guild.id)
                        embed = discord.Embed(title=f"", description="**Reacciona a este mensaje para abrir la partida** y así, otros miembros puedan unirse.", color=discord.Color.blue())
                        embed.set_author(name="No se ha unido ningún miembro todavía.")
                        self.game_start_message = await ctx.send(embed=embed)
                        await self.game_start_message.add_reaction('🎮')

                        channel = ctx.channel
                        user_count = 0
                        self.alfonso = ctx.guild.me

                    

                        try:
                            temporal = []
                            while True:
                                print(temporal)
                                reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=self.check)
                                if user.id not in temporal:
                                    temporal.append(user.id)
                                    self.game_cache.add_user(ctx.guild.id, str(user.id))
                                    user_count += 1

                                    if user_count == 1:
                                        autor = "Esperando que los miembros se unan."
                                        alerta = ':exclamation:**Una persona más necesita unirse para poder comenzar el juego.**'
                                    else:
                                        autor = "El juego comenzará dentro de unos segundos."
                                        alerta = False
                    
                                    embed = discord.Embed(title=f"Se {'han' if user_count > 1 else 'ha'} unido {user_count} {'personas' if user_count > 1 else 'persona'} al juego.", description=f"{alerta if alerta else ''}\nReacciona a este mensaje para unirte al juego de palabras. Veamos quién es la persona más sabia. Se han unido **{user_count}** personas hasta ahora.", color=discord.Color.blue())
                                    embed.set_author(name=autor, icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ad/YouTube_loading_symbol_3_(transparent).gif")   
                                    embed.set_footer(text=f"Rondas: {rnd} | Iniciado por {ctx.author}")
                                    await self.game_start_message.edit(embed=embed)
                                    
                                    
                                    self.already_said[str(ctx.guild.id)] = [] #INITIATE LIST OF WORDS

                        except asyncio.TimeoutError:
                            
                            self.game_cache.save_users(ctx.guild.id, self.game_cache.temp_list)
                            
                            self.lista[str(ctx.guild.id)] = self.game_cache.order_list[str(ctx.guild.id)]
                            self.total_players[str(ctx.guild.id)] = len(self.lista[str(ctx.guild.id)]) - 1

                            try:
                                if initial_round <= int(rnd):
                                    print("Comenzando configuracion de juego.")

                                    if len(self.game_cache.order_list[str(ctx.guild.id)]) > 1:
                                        
                                        self.started[str(ctx.guild.id)] = True
                                        print("Arrancó juego.")

                                        print(self.total_players[str(ctx.guild.id)], self.game_cache.temp_list, "Este es total_players lol")
                                        try:

                                            embed = discord.Embed(title=f":crossed_swords: La batalla comenzó.", description=f"Ahora **{user_count}** miembros se enfrentarán a la batalla. Que gane el mejor.", color=discord.Color.blue())
                                            await ctx.send(embed=embed, delete_after=10)
                                            await self.game_start_message.delete()
                                            await self.loop_started(ctx, channel, initiz, initial_round, max_round, order)
                                
                                        except Exception as error:
                                            print(error, "ocurrió un error al comenzar loop.")
                                    else:
                                        embed = discord.Embed(title=f":hourglass_flowing_sand: La batalla no comenzó.", description=f"No se unieron suficientes personas.", color=discord.Color.blue())
                                        await ctx.send(embed=embed, delete_after=15)
                                        self.game_cache.guild[str(ctx.guild.id)] = False
                                        await self.game_start_message.delete()

                            except Exception as error:
                                self.round = 1000
                                time.sleep(1)
                                self.started[str(ctx.guild.id)] = False
                                self.game_cache.guild[str(ctx.guild.id)] = False


                except Exception as error:
                    print(error, "aki es el error.")
                    self.round = 1000
                    time.sleep(1)
                    self.started[str(ctx.guild.id)] = False
                    self.game_cache.guild[str(ctx.guild.id)] = False
            except Exception as error:
                print(error)
        else:
            await ctx.send(":octagonal_sign: No puedes hacer una partida de más de 10 rondas.", delete_after=5)
        

    @teaword.command()
    async def quit(self, ctx):
        """
        Use **teaword quit** para parar el juego actual después de la siguiente ronda.
        """
        self.round = 1000
        time.sleep(1)
        self.started[str(ctx.guild.id)] = False
        self.game_cache.guild[str(ctx.guild.id)] = False
        await ctx.message.add_reaction("⏹️")

       

def setup(client):
    client.add_cog(Juegos(client))
    print('Juegos cargó.')
