import discord
from discord.ext import commands
import datetime
import random
import os
import pyodbc   
import asyncio
from cogs.azure_main import Azure
import traceback

img = Azure()
botName = 'Alfonso'



class Imagenes(commands.Cog):
  
  def __init__(self, client):
    self.client = client


  @commands.command(aliases=["img"])
  @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
  async def image(self, ctx, *, search: str):
    """
    Hacer una búsqueda en Bing Imágenes. La búsqueda segura está activada.
    """
    n = 0
    author = ctx.author.id
    await ctx.channel.trigger_typing()
    try:
      embed = discord.Embed(color=0x404040, description=f'Utiliza ``n`` para ver la imagen siguiente.',timestamp=datetime.datetime.utcnow())
      embed.set_image(url=img.img_url(search, n))
      embed.set_footer(text=f"\nResultado: {n}/5")
      embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
      msg_embed = await ctx.send(embed=embed)
    except Exception as error:
      print(error)
      if isinstance(error, Azure.QuotaExceeded):
        embed = discord.Embed(color=0x404040, description="**Desfortunadamente se alcanzó la cuota establecida para la búsqueda de imágenes. **Para continuar utilizando esta función es necesario cambiarse a una forma de pago, para mayor información en cómo poder ayudar a Alfonso y que sea accesible para tod@s, utiliza ``$donation``.")
        await ctx.send(embed=embed, delete_after=15)
      else:
        embed = discord.Embed(color=0x404040, description="No hubo ningún resultado en la búsqueda de imágenes.")
        await ctx.send(embed=embed, delete_after=15)


    try:

      channel = ctx.channel

      def check(m):
        
        return m.content == 'n' or m.content == 'N' and m.channel == channel and m.author == author

      while n < 5:
        msg = await self.client.wait_for('message', timeout=15.0, check=check)
        await ctx.channel.purge(limit=1, check=check)
        n += 1
        embed = discord.Embed(color=0x404040, description=f'Utiliza ``n`` para ver la imagen siguiente.',timestamp=datetime.datetime.utcnow())
        embed.set_image(url=img.img_url(search, n))
        embed.set_footer(text=f"\nResultado: {n}/5")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await msg_embed.edit(embed=embed)

    except asyncio.TimeoutError:
      pass

    
def setup(client):
    client.add_cog(Imagenes(client))