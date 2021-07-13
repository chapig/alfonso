import discord, aiohttp, json, asyncio, random
from discord.ext import commands


class nekos_api:

    async def get_url(self, choice):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.nekos.life/api/v2/img/{choice}') as r:
                res = await r.json()
                return res['url']
    
    async def get(self, choice):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.nekos.life/api/v2/{choice}') as r:
                res = await r.json()
                return res[f'{choice}']


class Community(commands.Cog):

    """
    This module contains the necessary commands for the interaction between players. 
    The images used and facts provided are thanks to: 
    https://www.nekos.life
    """

    def __init__(self, client):

        self.client = client

    @commands.command(aliases=["pfp"])
    async def avatar(self, ctx, user: discord.Member = None):
        """
        Check someone's profile picture.
        """
        if user is None:
            embed = discord.Embed(title=f"{ctx.author}'s Avatar", description=f"[Click here to get link](<{ctx.author.avatar_url}>)", color=discord.Color.blurple())
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"{user}'s Avatar", description=f"[Click here to get link](<{user.avatar_url}>)", color=discord.Color.blurple())
            embed.set_image(url=user.avatar_url)
            await ctx.send(embed=embed)
        
    @commands.command(aliases=["fact"])
    async def hecho(self, ctx):
        """
        Conoce hechos aleatorios.
        """
        neko = nekos_api()
        fact = await neko.get('fact')
        embed = discord.Embed(title="Dato interesante:", description=f"{fact}", color=discord.Color.blurple())
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["pipi"])
    async def pp(self, ctx, user: discord.Member = None):
        """
        Get to know the measurement of someone's tool (or yours).
        """
        rpp = random.choice(range(0,30))
        rg  = round(rpp / 2)
        rm = ['unfortunately, after extensive research I have come to the conclusion that it measures', 'according to rumors, measures', 'Girls, boys, and theys, I got some news, it measures', 'Yes!, it is a fact that it measures']
        if user is not None:
            embed = discord.Embed(title="", description=f"Sobre {user.mention}, {random.choice(rm)} **{rpp}** cm.", color=discord.Color.blurple())
            embed.add_field(name="Graphical representation:", value=f"8{'=' * rg}D")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f"Veamos {ctx.author.mention}, {random.choice(rm)} **{rpp}** cm.", color=discord.Color.blurple())
            embed.add_field(name="Graphical representation:", value=f"8{'=' * rg}D")
            await ctx.send(embed=embed)
            
    @commands.command(aliases=['abrazar','abrazo'])
    async def hug(self, ctx, user: discord.Member = None):
        """
        Hug a member from the server.
        """
        if user is not None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} is hugging {user.mention} (づ｡◕‿‿◕｡)づ", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('hug'))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f"{ctx.author.mention}, you must mention someone ≧◡≦", color=discord.Color.blurple())
            await ctx.send(embed=embed)
        
    @commands.command(aliases=['besar','beso'])
    async def kiss(self, ctx, user: discord.Member = None):
        """
        Kiss a member from the server.
        """
        if user is not None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} is kissing {user.mention} （＊＾Ｕ＾）人（≧Ｖ≦＊）/", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('kiss'))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f"{ctx.author.mention}, you must mention someone ≧◡≦", color=discord.Color.blurple())
            await ctx.send(embed=embed)
            
    @commands.command(aliases=['palmada','palmadita'])
    async def pat(self, ctx, user: discord.Member = None):
        """
        Pat a member from the server.
        """
        if user is not None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} le dio una palmadita a {user.mention}, qué ternura !⑈ˆ~ˆ!⑈", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('pat'))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
            await ctx.send(embed=embed)
            
    @commands.command(aliases=['acariciar','caricia'])
    async def cuddle(self, ctx, user: discord.Member = None):
        """
        Cuddle a member from the server.
        """
        if user is not None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} está acariciando a {user.mention}, qué bonito (*^ -^*)", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('cuddle'))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
            await ctx.send(embed=embed)
            
    @commands.command()
    async def poke(self, ctx, user: discord.Member = None):
        """
        Poke a member from the server.
        """
        if user is not None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{user.mention}..... H-hey, I am bothering you..., sorry ヾ(＠⌒▽⌒＠)ﾉ", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('poke'))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f"{ctx.author.mention}, you must mention someone ≧◡≦", color=discord.Color.blurple())
            await ctx.send(embed=embed)
        
    @commands.command()
    async def tickle(self, ctx, user: discord.Member = None):
        """
        Tickle a member from the server.
        """
        if user is not None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} is tickling {user.mention} Ｏ(≧▽≦)Ｏ", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('tickle'))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f"{ctx.author.mention}, you must mention someone ≧◡≦", color=discord.Color.blurple())
            await ctx.send(embed=embed)

    @commands.command()
    async def smug(self, ctx, user: discord.Member = None):
        """
        Smug a member from the server.
        """
        img = nekos_api()
        embed = discord.Embed(title="", description=f"♪┏ ( ･o･) ┛♪┗ (･o･ ) ┓♪┏(･o･)┛♪", color=discord.Color.blurple())
        embed.set_image(url=await img.get_url('tickle'))
        await ctx.send(embed=embed)

    @commands.command()
    async def meow(self, ctx, user: discord.Member = None):
        """
        Send a picture of a cat.
        """
        if user is None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} is meowing (⊙︿⊙✿)", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('meow'))
            await ctx.send(embed=embed)
        else:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} is meowing {user.mention} (▰˘◡˘▰)", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('meow'))
            await ctx.send(embed=embed)

    @commands.command()
    async def woof(self, ctx, user: discord.Member = None):
        """
        Send a picture of a dog.
        """
        if user is None:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} is... barking (▰˘◡˘▰)", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('woof'))
            await ctx.send(embed=embed)
        else:
            img = nekos_api()
            embed = discord.Embed(title="", description=f"{ctx.author.mention} is barking... {user.mention} ╰(◡‿◡✿╰)", color=discord.Color.blurple())
            embed.set_image(url=await img.get_url('woof'))
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Community(client))
