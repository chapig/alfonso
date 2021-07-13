from discord.ext import commands
from urllib import parse, request
import requests
import random
import json
import discord
import pyodbc
import os
import datetime
import time
import urllib
from cogs.database import Database

db = Database()

all_currencies = {"btc": "bitcoins", "ltc": "litecoins", "xrp": "ripples", "bch": "bitcoin cash", "doge": "dogecoins", "eth": "ethereum", "usd": "dólares estadounidenses", "ves": "bolívares venezolanos", "mxn": "pesos mexicanos", "cop": "pesos colombianos", "ars": "pesos argentinos", "eur": "euros", "brl": "reales brasileños", "dkk": "coronas danesas", "aed": "dirhams DE EAU", "crc": "colones costarricenses", "clp": "pesos chilenos", "cad": "dólares canadienses", "bob": "bolivianos", "pen": "nuevos soles"}

def get_currency_name(currency):
  currency = currency.lower()
  return all_currencies[f'{currency}'] if currency in all_currencies else currency.upper()

def send_embed_error(ctx):
    embed = discord.Embed(title=f"Conversión de monedas", description=f"Para convertir monedas, necesitas saber su código **ISO**. Las posibles utilizaciones del comando son las siguientes:\n```$c <moneda-a-convertir> <moneda-en-que-será-convertida> <número>```\n**Cuando no se coloca un número, el número será 1 por defecto.**```$c <moneda-a-convertir> <moneda-en-que-será-convertida>```\n**Si solo se coloca una moneda, será convertida a dólares estadounidenses.**```$c <moneda-a-convertir>```\n:ledger: **Para mostrar un resumen de las monedas más utilizadas, use ``$c list``.**", color=0xff9214)
    embed.set_footer(text=f"Economía | Conversión - {ctx.author}")
    return embed

def no_currency_error(ctx):
    embed = discord.Embed(title=f"No hubo ningún resultado.", description=f"Para poder utilizar el comando correctamente, es necesario conocer el código **ISO** de las monedas a convertir. Utiliza ``{ctx.prefix}c list`` para conocer una lista general de las monedas.", color=0xff9214)
    embed.set_footer(text=f"Economía | Conversión - {ctx.author}")
    return embed

class convertion:
  
  def calc(self, arg1=None, arg2=None, n=1):

    APIKEY = 'APIKEY'

    if arg1 is not None and arg2 is not None:
      s1 = None
      s2 = None
      if n != 1:
        with urllib.request.urlopen(f"https://min-api.cryptocompare.com/data/price?fsym={arg1.upper()}&tsyms={arg2.upper()}&api_key={APIKEY}") as url:
          data = json.loads(url.read().decode())
          price = data[f'{arg2.upper()}']
          price = price * n
          s1 = arg1.upper()
          s2 = arg2.upper()
          return price, s1, s2, n
      else:
        with urllib.request.urlopen(f"https://min-api.cryptocompare.com/data/price?fsym={arg1.upper()}&tsyms={arg2.upper()}&api_key={APIKEY}") as url:
          data = json.loads(url.read().decode())
          price = data[f'{arg2.upper()}']
          s1 = arg1.upper()
          s2 = arg2.upper()
          return price, s1, s2, n
    else:
      if arg1 is not None:
        with urllib.request.urlopen(f"https://min-api.cryptocompare.com/data/price?fsym={arg1.upper()}&tsyms=USD&api_key={APIKEY}") as url:
          data = json.loads(url.read().decode())
          price = data[f'USD']
          s1 = arg1
          s2 = 'USD'
          return price, s1, s2, n



class Economia(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        """
        Mirar el balance del usuario.
        """
        try:
          db.all(ctx.guild.id, ctx.author.id)
          guild = self.client.get_guild(625860423144570902)
          emerald_emoji = discord.utils.get(guild.emojis, name='diamante')
          modulo = "Economia"
          section = 'Balance'
          embed = discord.Embed(title=f":moneybag: Balance", color=0xff9214)
          embed.add_field(name="**Dinero:**", value=f"{db.balance} **{db.currency}**")
          embed.add_field(name="**Esmeraldas:**", value=f"{db.emeralds} {emerald_emoji}")
          embed.set_footer(text=f"{modulo} | {section} - {ctx.author}")
          await ctx.send(embed=embed)
        except Exception as error:
          print(error)
          db.balance_update(ctx.guild.id, ctx.author.id, 100, 1)
          await self.balance(ctx)
          


    @commands.command(aliases=['wrk'])
    async def work(self, ctx):
        """
        Comando para trabajar, ganar dinero y esmeraldas.
        """  
        guild = self.client.get_guild(625860423144570902)
        emerald_emoji = discord.utils.get(guild.emojis, name='diamante')
        
        section = 'Trabajo'
        modulo = 'Economia'
        db.all(ctx.guild.id, ctx.author.id)
        if db.estado == '0':

            embed = discord.Embed(title=f":nut_and_bolt: Este servidor tiene la economía desactivada.", color=0xff4d4d)
            embed.add_field(name="Cómo activarla:", value=f"Para activarla, usar ``$config economy``, este comando también se utiliza para desactivarla.")
            embed.set_footer(text=f"{modulo} | {section} - {ctx.author}")
            await ctx.send(embed=embed)
            
        elif db.estado == '1':

          tiempo = db.timew

          tiempo_pasado = time.time() - tiempo

          segundos_que_tienen_que_pasar = 3600

          conversion_a_minutos = segundos_que_tienen_que_pasar / 60

          minutos_restantes = conversion_a_minutos - (tiempo_pasado / 60)  

          minutos_restantes = round(minutos_restantes)

          if tiempo_pasado >= segundos_que_tienen_que_pasar:

              salario = random.choice(range(100,200)) 


              esmeraldas = random.choice(range(0,3)) 

              db.balance_update(ctx.guild.id, ctx.author.id, salario, esmeraldas)
              
              
              if esmeraldas != 0:
                finaldesc = f"Has ganado el monto de **{salario}**$ y también ganaste **{esmeraldas}**{emerald_emoji}"
              else:
                finaldesc = f"Has ganado el monto de **{salario}**$"

              embed = discord.Embed(title=f"Trabajo", description=f"{finaldesc}", color=0xff9214)
              embed.set_footer(text=f"{modulo} | {section} - {ctx.author}")
              await ctx.send(embed=embed)
          else:
              embed = discord.Embed(title=f":alarm_clock: No puedes trabajar todavía.", color=0xff4d4d)
              embed.add_field(name="Información", value=f"Debes esperar **{minutos_restantes}** minutos para poder trabajar de nuevo.")
              embed.set_footer(text=f"{modulo} | {section} - {ctx.author}")
              await ctx.send(embed=embed)

    @commands.command(aliases=["convertir", "convert"])
    async def c(self, ctx, moneda_1= None, moneda_2= None, numero: float= 1):
      """
      Comando para ver el precio y convertir monedas internacionales. Para convertir monedas, necesitas saber el código ISO. Utiliza ``$c list`` para obtener una lista general de monedas. 
      """
      lista_all = """
      **USD** es igual a **dólares estadounidenses**.
      **VES** es igual a **bolívares venezolanos**.
      **MXN** es igual a **pesos mexicanos**.
      **COP** es igual a **pesos colombianos**.
      **ARS** es igual a **pesos argentinos**.
      **EUR** es igual a **euros**.
      **BRL** es igual a **reales brasileños**.
      **DKK** es igual a **coronas danesas**.
      **AED** es igual a **dirhams DE EAU**.
      **CRC** es igual a **colones costarricenses**.
      **CLP** es igual a **pesos chilenos**.
      **CAD** es igual a **dólares canadienses**.
      **BOB** es igual a **bolivianos**.
      **PEN** es igual a **nuevos soles**.
      """
      try:
        if moneda_1.upper() == "LISTA" or moneda_1.upper() == "LIST":
            embed = discord.Embed(title=f"",
            description=f"Lista general de monedas internacionales.\n{lista_all}\n[Clique aquí para ver una lista más completa.](https://es.iban.com/currency-codes)", color=0xff9214)
            embed.set_footer(text=f"Economía | Conversión - {ctx.author}")
            await ctx.send(embed=embed)
        else: 
          try:
            calculator = convertion()
            await ctx.trigger_typing()
            x = calculator.calc(moneda_1, moneda_2, numero)
            embed = discord.Embed(title=f"", description=f"\n\n**{round(x[3])}** {get_currency_name(x[1])} **({x[1].upper()})** equivalen a **{x[0]}** {get_currency_name(x[2])} **({x[2]})**.", color=0xff9214)
            embed.set_footer(text=f"Economía | Conversión - {ctx.author}")
            await ctx.send(embed=embed)
          except Exception as error:
            await ctx.send(embed=no_currency_error(ctx))
            print(error)
      except Exception as error:
        await ctx.send(embed=send_embed_error(ctx))
        print(error)
        
def setup(client):
    client.add_cog(Economia(client))
    print('El módulo de Economia cargó correctamente.')
 

