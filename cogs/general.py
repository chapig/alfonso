from discord.ext import commands
import discord
import os, random, requests, io
import datetime
import urllib, json
from cogs.azure_main import Azure
from discord.ext.commands import MinimalHelpCommand
import julia

jl = julia.Julia(compiled_modules=False)

jl.include("/julia/mathenize.jl")

jl.eval("using .matematicas;")

azure_get = Azure()


botName = 'Alfonso'
gifError = 'Ocurrió un error al enviar este gif.'

class nekos_class:

    def get_url(self, choice):
        base_url = f"https://www.nekos.life/api/v2/img/{choice}"
        resp = requests.get(base_url)
        url = resp.json()["url"]
        return(url)
    
    def get(self, choice):
      base_url = f"https://www.nekos.life/api/v2/{choice}"
      resp = requests.get(base_url)
      url = resp.json()
      return(url)

class General(commands.Cog):
  """
  En este módulo se alojan los comandos generales, que no necesitan de un módulo especial para definirlos.
  """

  def __init__(self, client):
  
    self.client = client


  @commands.command()
  async def calc(self, ctx, *, maths):
    """
    Realiza operaciones matemáticas.
    **Operaciones posibles:**
    ``+`` ``-`` ``*`` ``/`` ``^`` ``**``

    **Nota:** ``^`` y ``**`` cumplen la misma función. Operaciones con parentesis todavía no es posible.

    **Extras:**

    ``//`` (Valor dividido redondeado)
    ``cos(numero)`` Coseno de número.
    ``sen(numero)`` Seno de número.
    ``tan(numero)`` Tangente de número.
    ``sqrt(numero)`` Raiz cuadrada de número. Raíz negativa también permitida.

    **Caracteres reconocidos:**

    ``pi`` o ``π`` Valor de pi.

    Programa escrito por **Chapi**, usando JuliaLang y Python.

    """
    try:
      await ctx.trigger_typing()
      result = jl.eval(f'compute("{maths}")')
      await ctx.send(f"```python\n{result}\n```")
    except Exception:
      await ctx.send("```No se pudo realizar esta operación matemática. Verifica si las operaciones están separadas por signos. Las funciones dentro de funciones no son permitidas.```")

    
  @commands.command()
  @commands.cooldown(rate=1, per=10, type=commands.BucketType.default)
  async def tts(self, ctx, *, text):
    """
    Transforma un texto a una voz neuronal, la voz se envía en un audio.
    """
    
    if text is not None:
      if len(text) < 650:
        await ctx.trigger_typing()
        audio = azure_get.save_audio(text)
        file = discord.File(audio, filename=audio)
        await ctx.send(file=file)
        os.remove(audio)
      else:
        embed = discord.Embed(title="", description=f"No se pudo general el audio porque el texto sobrepasa el límite de los 650 caracteres. **{len(text)}/650**.", color=discord.Color.red())
        await ctx.send(embed=embed)
    
  @commands.command()
  async def avatar(self, ctx, user: discord.Member = None):
    """
    Mira tu avatar o el avatar de un usuario.
    """
    if user is None:
      embed = discord.Embed(title=f"Avatar de {ctx.author}", description=f"[Click aquí para obtener link](<{ctx.author.avatar_url}>)", color=discord.Color.blurple())
      embed.set_image(url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title=f"Avatar de {user}", description=f"[Click aquí para obtener link](<{user.avatar_url}>)", color=discord.Color.blurple())
      embed.set_image(url=user.avatar_url)
      await ctx.send(embed=embed)
      
  @commands.command(aliases=["fact"])
  async def hechos(self, ctx):
    """
    Conoce hechos aleatorios.
    """
    neko = nekos_class()
    fact = neko.get('fact')['fact']
    embed = discord.Embed(title="Dato interesante:", description=f"{azure_get.translate(fact, 'es')}", color=discord.Color.blurple())
    await ctx.send(embed=embed)
  
  @commands.command(aliases=["pipi"])
  async def pp(self, ctx, user: discord.Member = None):
    """
    Comando para saber la medida de la herramienta. (Esto es solo para diversión)
    """
    rpp = random.choice(range(0,30))
    rg  = round(rpp / 2)
    rm = ['desafortunadamente, después de una exhaustiva investigación he llegado a la conclusión de que mide', 'según los rumores, mide', 'chicos, chicas y chicxs, les traigo buenas noticias, mide', 'pues sí, es cierto que mide']
    if user is not None:
      embed = discord.Embed(title="", description=f"Sobre {user.mention}, {random.choice(rm)} **{rpp}** cm.", color=discord.Color.blurple())
      embed.add_field(name="Representación gráfica:", value=f"8{'=' * rg}D")
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="", description=f"Veamos {ctx.author.mention}, {random.choice(rm)} **{rpp}** cm.", color=discord.Color.blurple())
      embed.add_field(name="Representación gráfica:", value=f"8{'=' * rg}D")
      await ctx.send(embed=embed)
        
  @commands.command(aliases=['abrazar','abrazo'])
  async def hug(self, ctx, user: discord.Member = None):
    """
    Menciona a un miembro para abrazarle.
    """
    if user is not None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} está abrazando a {user.mention} (づ｡◕‿‿◕｡)づ", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('hug'))
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
      await ctx.send(embed=embed)
      
  @commands.command(aliases=['besar','beso'])
  async def kiss(self, ctx, user: discord.Member = None):
    """
    Menciona a un miembro para besarle.
    """
    if user is not None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} está besando a {user.mention} （＊＾Ｕ＾）人（≧Ｖ≦＊）/", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('kiss'))
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
      await ctx.send(embed=embed)
        
  @commands.command(aliases=['palmada','palmadita'])
  async def pat(self, ctx, user: discord.Member = None):
    """
    Menciona a un miembro para darle una palmadita.
    """
    if user is not None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} le dio una palmadita a {user.mention}, qué ternura !⑈ˆ~ˆ!⑈", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('pat'))
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
      await ctx.send(embed=embed)
      
  @commands.command(aliases=['acariciar','caricia'])
  async def cuddle(self, ctx, user: discord.Member = None):
    """
    Menciona a un miembro para acariciarle.
    """
    if user is not None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} está acariciando a {user.mention}, qué bonito (*^ -^*)", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('cuddle'))
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
      await ctx.send(embed=embed)
      
  @commands.command()
  async def poke(self, ctx, user: discord.Member = None):
    """
    Menciona a un miembro para molestarle un poco.
    """
    if user is not None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{user.mention}..... Ho-hola, te estoy molestando, perdón ヾ(＠⌒▽⌒＠)ﾉ", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('poke'))
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
      await ctx.send(embed=embed)
      
  @commands.command()
  async def tickle(self, ctx, user: discord.Member = None):
    """
    Menciona a un miembro para hacerle cosquillas.
    """
    if user is not None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} está haciéndole cosquillas a {user.mention} Ｏ(≧▽≦)Ｏ", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('tickle'))
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="", description=f"{ctx.author.mention}, debes mencionar a alguien ≧◡≦", color=discord.Color.blurple())
      await ctx.send(embed=embed)

  @commands.command()
  async def smug(self, ctx, user: discord.Member = None):
    """
    Es mejor descubrir por ti mismo lo que hace este comando.
    """
    img = nekos_class()
    embed = discord.Embed(title="", description=f"♪┏ ( ･o･) ┛♪┗ (･o･ ) ┓♪┏(･o･)┛♪", color=discord.Color.blurple())
    embed.set_image(url=img.get_url('tickle'))
    await ctx.send(embed=embed)

  @commands.command()
  async def meow(self, ctx, user: discord.Member = None):
    """
    Maullar es algo de gatos, este comando envía una imagen aleatoria de un gato.
    """
    if user is None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} está.... maullando (⊙︿⊙✿)", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('meow'))
      await ctx.send(embed=embed)
    else:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} le está.... maullando a {user.mention} (▰˘◡˘▰)", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('meow'))
      await ctx.send(embed=embed)

  @commands.command()
  async def woof(self, ctx, user: discord.Member = None):
    """
    Ladrar es algo de perros, este comando envía una imagen aleatoria de un gato.
    """
    if user is None:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} está.... ladrando (▰˘◡˘▰)", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('woof'))
      await ctx.send(embed=embed)
    else:
      img = nekos_class()
      embed = discord.Embed(title="", description=f"{ctx.author.mention} le está.... ladrando a {user.mention} ╰(◡‿◡✿╰)", color=discord.Color.blurple())
      embed.set_image(url=img.get_url('woof'))
      await ctx.send(embed=embed)

def setup(client):
    client.add_cog(General(client))
    print('El módulo de Generales cargó correctamente.')
