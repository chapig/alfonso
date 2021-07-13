from discord.ext import commands
from urllib import parse, request
import datetime
import requests
import random
import json
import discord
import os 
import sys
import pyodbc
import re
import time
import julia
import wikipedia

jl = julia.Julia(compiled_modules=False)

jl.include("/julia/wikipedia.jl")

jl.eval("using .wikisearch;")

wikipedia.set_lang("es")

botName = 'Alfonso'

class Wikipedia(commands.Cog):

    m_search = discord.Embed(color=0x404040, description="Debes escribir algo para buscar en **Wikipedia**.",timestamp=datetime.datetime.utcnow())
    e_search = discord.Embed(color=0x404040, description="No hubo ningún resultado en **Wikipedia**.",timestamp=datetime.datetime.utcnow())
    def final(self, text):
        text = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", text)
        text = text.replace('[','')
        text = text.replace(']','')
        text = text.replace('(', '')
        text = text.replace(')', '')
        return(discord.Embed(color=0x404040, description=text,timestamp=datetime.datetime.utcnow()))

    @commands.command()
    async def wiki(self, ctx, *, busqueda: str):
        """
        Hacer una búsqueda en Wikipedia.
        """
        try:
            await ctx.channel.trigger_typing()
            await ctx.send(embed=self.final(wikipedia.summary(busqueda, sentences=2))) if busqueda else await ctx.send(embed=self.m_search)
            
        except Exception:
            await ctx.send(embed=self.e_search)
    
    @commands.command()
    async def jwiki(self, ctx, *, busqueda: str):
        try:
            result = jl.eval(f'search("{busqueda}", 2, false)')
            await ctx.send(result)
        except Exception as error:
            await ctx.send(error)


    # @wiki.error
    # async def wiki_handler(self, ctx, error):
    #     """
    #     Muestra el error de Wikipedia
    #     """
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         embed = discord.Embed(title="", description=f"Falta un argumento. Para saber cómo utlizar un comando usa ``$help <comando>``.", color=discord.Color.red())
    #         await ctx.send(embed=embed)


    # @commands.command(aliases=['wki', 'WIKI', 'Wiki'])
    # async def wiki(self, ctx, *, search = None):
    #     modulo = 'Wikipedia'
    #     try:
    #         await ctx.trigger_typing()
    #         mediawikiapi = MediaWikiAPI()
    #         mediawikiapi.config.language = 'es'
    #         tupla = mediawikiapi.search(search)
    #         page = mediawikiapi.page(tupla[0])
    #         data = mediawikiapi.summary(tupla[0], sentences = 1, chars= 0, auto_suggest= True, redirect= True)
    #         data = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", data)
    #         data = data.replace('[','')
    #         data = data.replace(']','')
    #         data = data.replace('(', '')
    #         data = data.replace(')', '')
    #         embed=discord.Embed(title=f"{page.title}", description=f"{data}\n\n[Para leer más, hacer clic aquí.](<{page.url}>)", color=discord.Color.from_rgb(255,255,255))
    #         embed.set_author(name="Wikipedia", icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
    #         embed.set_footer(text=f'{modulo} - {ctx.author}')
    #         await ctx.send(embed=embed)
    #     except Exception as error:
    #         if search is None:
    #             embed=discord.Embed(title=f"", description=f"**Cómo hacer una búsqueda en Wikipedia**:  ```$wiki <búsqueda>```", color=discord.Color.from_rgb(255,255,255))
    #             embed.set_author(name="Wikipedia", icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
    #             embed.set_footer(text=f'{modulo} - {ctx.author}')
    #             await ctx.send(embed=embed)
    #         else:
    #             embed=discord.Embed(title=f"", description="**No hubo ningún resultado.**", color=discord.Color.from_rgb(255,255,255))
    #             embed.set_author(name="Wikipedia", icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
    #             embed.set_footer(text=f'{modulo} - {ctx.author}')
    #             await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Wikipedia(client))
