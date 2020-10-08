import discord, os, requests, uuid, json, random, wikipedia, traceback, json, time, asyncio, sqlite3
from discord.ext import commands
from games.external.tools_g import language
from games.database.teaword import Guild, Users, GAME
from games.external.tw_tools import embed_start, random_selection
from ext.toollenize import Embed

class tw(commands.Cog):

    def __init__(self, client):

        self.client = client

    def check(self, reaction, user):
        return str(reaction.emoji) == '🎮' and self.alfonso != user

    @commands.group()
    async def tw(self, ctx):
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
    
    @tw.command()
    async def start(self, ctx, rondas: int):
        """
        **TeaWord** es un juego de palabras, el bot le dará una terminación aleatoria a un miembro y este tendrá que escribir una palabra con ella.
        
        **Utilización:**
        ``$teaword start 3`` 
        El ``3`` en este caso significa cuántas rondas serán.
        ``$teaword quit``
        Este comando sirve para parar el juego.
        """

        guild = Guild(ctx.guild.id)
        self.alfonso = ctx.guild.me

        try:

            if rondas <= 10 and rondas >= 1:

                game = guild.create_table(ctx.channel.id) #Creating UNIQUE table on SQL database.
                users = Users(game) #Initiating Users instance.

                start_msg = await ctx.send(embed=embed_start())
                await start_msg.add_reaction("🎮")


                try:
                    
                    while True:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=5.0, check=self.check)
                        users.add_player(user.id) # Adding player to SQL Database.
                
                        if users.count == 1:
                            autor = "Esperando que los miembros se unan."
                            alerta = ':exclamation:**Una persona más se necesita para comenzar el juego.**'
                        else:
                            autor = "El juego comenzará dentro de unos segundos."
                            alerta = False
                        
                        embed = discord.Embed(title=f"Se {'han' if users.count > 1 else 'ha'} unido {users.count} {'personas' if users.count > 1 else 'persona'} al juego.", description=f"{alerta if alerta else ''}\nReacciona a este mensaje para unirte al juego de palabras. Veamos quién es la persona más sabia. Se han unido **{users.count}** personas hasta ahora.", color=discord.Color.blue())
                        embed.set_author(name=autor, icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ad/YouTube_loading_symbol_3_(transparent).gif")   
                        embed.set_footer(text=f"Rondas: {rondas} | Iniciado por {ctx.author}")
                        await start_msg.edit(embed=embed)

                except asyncio.exceptions.TimeoutError:
                    
                    if users.count > 1:
                        
                        await start_msg.delete()
                        embed = discord.Embed(title=f":crossed_swords: La batalla comenzó.", 
                                                description=f"Ahora **{users.count}** miembros se enfrentarán a la batalla. Que gane el mejor.",
                                                color=discord.Color.blue())

                        await ctx.send(embed=embed, delete_after=10)

                        game = GAME(self.client, ctx)
                        game.rounds = rondas
                        game.players = users.all_players()
                        await game.start()

                    else:

                        await start_msg.delete()
                        embed = discord.Embed(title=f"", 
                                                description=f":hourglass_flowing_sand: No se unieron suficientes personas para comenzar el juego.", 
                                                color=discord.Color.blue())
                        await ctx.send(embed=embed, delete_after=15)

            else:

                await ctx.send(embed=Embed(title=None, description=f"{ctx.author.mention} No puedes colocar menos de 1 o más de 10 ronda(s), intenta un número de rondas válido **(1 al 10)**.", color=discord.Color.red()), delete_after=10)

        except sqlite3.OperationalError:

            await ctx.send(embed=Embed(title="Antes de comenzar, haz lo siguiente.",
                                        description="Puede que un juego ya haya comenzado en este canal, o acabe de terminar uno.\n **Utiliza ``tw exit`` para terminar o eliminar el juego de este canal.**", 
                                        color=discord.Color.blurple()))

        except Exception as error:
            print(error)

    @tw.command(aliases=["quit", "remove"])
    async def exit(self, ctx):

        try:
            guild = Guild(ctx.guild.id)
            game = guild.remove_table(ctx.channel.id)
            description = "Se ha parado el juego de este canal. \n**ID:** ``%s``" % game
        except Exception:
            description = "**No hay ningún juego en este canal.** \nPara comenzar un juego utiliza ``tw start``."

        await ctx.send(embed=Embed(title=None, description=description, color=discord.Color.blurple()))
   

def setup(client):
    client.add_cog(tw(client))
