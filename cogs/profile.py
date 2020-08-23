"""
DEPECRATED MODULE
"""


import discord
from discord.ext import commands
import datetime
import json
from PIL import Image, ImageDraw, ImageFont
from cogs.exp import experience
from cogs.profile import Prof_h
import os

img = Prof_h()
exp = experience()
botName = 'Alfonso'

class Perfiles(commands.Cog):
    """
    En este módulo existen los comandos necesarios para modificar y mostrar tu perfil publicamente.
    """

    @commands.command()
    async def profile(self, ctx, user = None):
        if user is None:
            exp = main()

            imagen = img.create_user_profile(font_name=None, 
                                    font_size=40, 
                                    user_name=f"{ctx.author}", 
                                    exp=exp.fetch(ctx.author.id, 'exp'), 
                                    rank=exp.fetch(ctx.author.id, 'rank'), 
                                    badge=exp.fetch(ctx.author.id, 'badge'), 
                                    img_url=ctx.author.avatar_url_as(format='png', size=128))
            
            await ctx.send(file=discord.File(imagen[0]))
            file_temp_n = imagen[1]
            os.remove(f"/home/luis-hatchens/alfonso/img/temp_avatars/{file_temp_n}.png")
            os.remove(f"/home/luis-hatchens/alfonso/img/temp_img/{file_temp_n}.png")



def setup(client):
    client.add_cog(Perfiles(client))
