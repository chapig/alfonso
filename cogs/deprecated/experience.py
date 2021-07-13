import discord
from discord.ext import commands
import pyodbc
from cogs.exp import experience
import datetime
import random

exp = experience()

#AQUÍ PODRÍA PARA QUE NO HUBIESE LAG, GUARDAR EN UN JSON FILE TEMPORAL LA EXPERIENCIA GUARDADA.
#(VER SI SE PUEDE EN PYTHON DIRECTAMENTE), Y CUANDO LLEGUE A CIERTO PUNTO, SUBIRLA AL DATABASE.



class Experiencia(commands.Cog):
  """
  En este módulo se encuentran los comandos utilizados para la utilización de los niveles y experiencia global.
  """
  
  def __init__(self, client):
    self.client = client
    self.player = {}

  def level_up(self, message):
    return(discord.Embed(color=0x404040, description=f"{message.author.mention} ha subido de nivel.",timestamp=datetime.datetime.utcnow()))
  

  @commands.command()
  async def exp(self, ctx, user: discord.Member = None):
    """
    Mostrar la experiencia de un miembro.
    """
    await ctx.trigger_typing()
    try:
      if user is None:
        try:
          all_obj = exp.checkif(ctx.author.id)
        except Exception:
          amount = 0
        try:
          try:
            self.player[f'{str(ctx.author.id)}'] = self.player[f'{str(ctx.author.id)}']
          except Exception:
            self.player[f'{str(ctx.author.id)}'] = 0

          level = (all_obj[0] + self.player[f'{str(ctx.author.id)}']) / 500
          level = round(level)

          embed = discord.Embed(color=0x404040, description=f"Posee actualmente **{all_obj[0] + self.player[f'{str(ctx.author.id)}']}** de experiencia.\nEl nivel de este jugador es **{level}**.",timestamp=datetime.datetime.utcnow())
          embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
        except Exception as error:
          print(error)
      else:
          try:
            all_obj = exp.checkif(user.id)
          except Exception:
            amount = 0
          try:
            self.player[f'{str(user.id)}'] = self.player[f'{str(user.id)}']
          except Exception:
            self.player[f'{str(user.id)}'] = 0
          
          level = (all_obj[0] + self.player[f'{str(user.id)}']) / 500
          level = round(level)

          embed = discord.Embed(color=0x404040, description=f"Posee actualmente **{all_obj[0] + self.player[f'{str(user.id)}']}** de experiencia.\nEl nivel de este jugador es **{level}**.",timestamp=datetime.datetime.utcnow())
          embed.set_author(name=user.name, icon_url=user.avatar_url)
          await ctx.send(embed=embed)
    except Exception as error:
      print(error)
      embed = discord.Embed(color=0x404040, description=f"Este jugador todavía no ha hablado lo suficiente globalmente.",timestamp=datetime.datetime.utcnow())
      embed.set_author(name=user.name, icon_url=user.avatar_url)
      await ctx.send(embed=embed)
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.client.user:
      return
    else:
      try:
        self.player[f'{str(message.author.id)}'] += random.choice(range(5,10))
      except Exception:
        self.player[f'{str(message.author.id)}'] = 0
        if exp.checkif(message.author.id)[1] is False:
          exp.insert(message.author.id)
      if self.player[f'{str(message.author.id)}'] == 500:
        level = (exp.checkif(message.author.id)[1] + self.player[f'{str(message.author.id)}']) / 500
        level = round(level)
        self.player[f'{str(message.author.id)}'] = 0
        embed = discord.Embed(color=0x404040, description=f"Ha subido de nivel. Ahora es nivel **{level}**.")
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.set_footer(text="Alfonso - Alpha 1.0")
        await message.channel.send(embed=embed)
      
      if message.content.upper().startswith('CHAO') and message.author != message.guild.me and message.author.bot is False:
        await message.channel.send(f"chao feo")
  

def setup(client):
  print("inició experiencia")
  client.add_cog(Experiencia(client))




    
