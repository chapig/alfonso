from discord.ext import commands
from ext.toollenize import Embed
from database.alfonso_db import Currencies
import discord, urllib, json

#export PATH="$PATH:/root/julia/julia-1.5.3/bin"

cu = Currencies()
try:

    from julia.api import Julia
    jl = Julia(compiled_modules=False)
    julia_status = True

except Exception as error:

    print(error)
    julia_status = False

class convertion:

    def get_currency_name(self, currency):
        currency = currency.lower()
        return self.all_currencies[f'{currency}'] if currency in self.all_currencies else currency.upper()

    def send_embed_error(self, ctx):
        embed = discord.Embed(title=f"Currencies price convertion", description=f"To convert currencies or coins, you need to know their **ISO** code. Possible uses of the command: \n ````{ctx.prefix}c <currency-to-be-converted> <conversion-currency-target> <number>``` \n**When a number is not placed, the number will be 1 by default.** ```{ctx.prefix}c <currency-to-be-converted> <conversion-currency-target>``` \n**If only one currency is placed, it will be converted to U.S. dollars.** ```$c <currency-to-be-converted>``` \n📒**To display a summary of the most commonly used currencies, use or coins \n```{ctx.prefix}c list```", color=0xff9214)
        embed.set_footer(text=f"Economy | Currencies - {ctx.author}")
        return embed

    def no_currency_error(self, ctx):
        embed = discord.Embed(title=f"Currency was not found.", description=f"In order to use the command correctly, it is necessary to know the **ISO** code of the coins or currency that will be converted. Use ```{ctx.prefix}c list'' to find out a general list of currencies.", color=0xff9214)
        embed.set_footer(text=f"Economía | Conversión - {ctx.author}")
        return embed

    def calc(self, arg1=None, arg2=None, n=1):

        APIKEY = 'b72d1dd701b7f6375318ea8238a5686ca49e22a280c96bae4ffae124c0e8ad6e'

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

class Math(commands.Cog):

    """
    Mathematical operations such as international **calculations** and **currency prices**
    will be here.
    """

    def __init__(self, client):

        self.client = client
        if julia_status:
            jl.eval("using Mathenize")



    @commands.command(aliases=["convertir", "convert"])
    async def c(self, ctx, currency_a= None, currency_b= None, number: float= 1):
      """
      View the price and convert international currencies and coins. To convert coins or currencies, you need to know the ISO code. Use ''a!c list'' to get a general list of currencies.
      """
      lista_all = """
        **USD** is equal to **US Dollars**.
        **VES** is equal to **Venezuelan bolivars**.
        **MXN** is equal to **Mexican pesos**.
        **COP** is equal to **Colombian pesos**.
        **ARS** is equal to **Argentinian pesos**.
        **EUR** is equal to **euros**.
        **BRL** is equal to **Brazilian reals**.
        **DKK** is equal to **Danish kroner**.
        **AED** is equal to **UAE dirhams**.
        **CRC** is equal to **Costa Rican colones**.
        **CLP** is equal to **Chilean pesos**.
        **CAD** is equal to **Canadian dollars**.
        **BOB** is equal to **Bolivians**.
        **PEN** is equal to **new soles**.
      """
      try:
        if currency_a.upper() == "LISTA" or currency_a.upper() == "LIST":
            embed = discord.Embed(title=f"",
            description=f"General list of international currencies.\n{lista_all}\n[Click here for more information regarding currencies](https://es.iban.com/currency-codes)", color=0xff9214)
            embed.set_footer(text=f"Economy | Convertion - {ctx.author}")
            await ctx.send(embed=embed)
        else: 
          try:
            calculator = convertion()
            await ctx.trigger_typing()
            x = calculator.calc(currency_a, currency_b, number)
            embed = discord.Embed(title=f"", description=f"\n\n**{x[3]}** {cu.fetch_name(x[1].upper()).lower()} **({x[1].upper()})** equivalen a **{x[0]}** {cu.fetch_name(x[2].upper()).lower()} **({x[2]})**.", color=0xff9214)
            embed.set_footer(text=f"Economy | Convertion - {ctx.author}")
            await ctx.send(embed=embed)
          except Exception as error:
            await ctx.send(embed=convertion().no_currency_error(ctx))
            print(error)
      except Exception as error:
        await ctx.send(embed=convertion().send_embed_error(ctx))
        print(error)


    @commands.command()
    async def calc(self, ctx, *, math):
        """
        Perform mathematical operations.
        **Possible operations:**
        `+` `-` `*` `/` `^` `**`
        **Extras:**
        ``cos(number)`` Cosine number.
        ``sen(number)`` Number sine.
        ``tan(number)`` Number tangent.
        ``sqrt(number)`` Square root number. Negative square root also allowed with complex() function.
        **Recognized characters:**
        ``pi`` or ``π`` Value of pi.
        Program written by **Chapi**, using Julia and Python.
        """
        if julia_status:
            try:
                await ctx.trigger_typing()
                result = jl.eval(f'calculate("{math}")')
                await ctx.send(f"```python\n{result}\n```")
            except Exception:
                await ctx.send("This mathematical operation could not be performed. Check grammar.")
        else:
            await ctx.send(embed=Embed(title=None, description="This command is disabled for now globally. Contact the developer if this problem persists.", color=discord.Color.red()))


def setup(client):
    client.add_cog(Math(client))
