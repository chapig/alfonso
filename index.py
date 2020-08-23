import discord
from discord.ext import commands, flags
from discord.ext.commands import MinimalHelpCommand
import sys
import os
import pyodbc
import time
from cogs.database import Database

db = Database()

db.update_all_prefixes()

extensions = ['cogs.games','cogs.moderation', 'cogs.help','cogs.general', 'cogs.economy', 'cogs.wikipedia', 'cogs.img', 'cogs.translator', 'cogs.profile', 'cogs.exp', 'cogs.config']

def num_there(s):
    return any(i.isdigit() for i in s)

def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner.id

def get_prefix(bot, message):
  try:
    if not message.guild:
        return "$"
    else:
        return commands.when_mentioned_or(db.global_prefixes[f'{str(message.guild.id)}'])(bot, message)
  except KeyError:
    return commands.when_mentioned_or("$")(bot, message)

client = commands.Bot(command_prefix = get_prefix)


client.remove_command('help')

@client.command()
@commands.check(is_guild_owner)
async def prefix(ctx, *, prefix: str):
    """
    Cambia el prefijo de un servidor, **solo los dueños de los servidores pueden hacer esto**.
    """
    if num_there(prefix) is False:
        if len(prefix) < 4:
            db.u_prefix(ctx.guild.id, prefix)
            embed = discord.Embed(title=f"Se cambió el prefijo del servidor exitosamente.", description=f'Ahora el prefijo es ``{prefix}``.', color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"No se pudo cambiar el prefijo.", description=f'El prefijo es muy largo.', color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"No puedes usar esos caracteres.", description=f'**Tu prefijo actual es **``{db.lista[1]}``.\n\nPara cambiar el prefijo, utiliza ``$prefix <prefijo>``. Por favor no utilices números ni emojis.', color=discord.Color.purple())
        await ctx.send(embed=embed)
    db.update_all_prefixes()


@client.command()
async def userinfo(ctx, user: discord.Member = None):
    """
    Muestra la información general de un usuario.
    """
    if user is not None:
        embed = discord.Embed(title=f"", description='Información de usuario', color=discord.Color.purple())
        embed.add_field(name="Nombre de usuario", value=f"{user}")
        embed.add_field(name="Se unió al servidor", value=f"`{user.joined_at}`")
        embed.add_field(name="ID de Discord", value=f"`{user.id}`")
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    """
    Muestra la latencia del bot con la conexión a Discord y a la base de datos.
    """
    embed = discord.Embed(title=f"Información de redes de Alfonso", color=discord.Color.blue())
    embed.add_field(name="Latencia de la API de Discord ", value=f" **{round(client.latency * 1000)}** ms.")
    try:
        start_time = time.time()
        server = 'SERVER'
        database = 'DATABASE'
        username = 'USER'
        password = 'PASSWORD'
        driver= '{ODBC Driver 17 for SQL Server}'
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        cursor.execute(f"""SELECT * FROM economys
                WHERE discord=625860423144570902;""")
        r = time.time() - start_time 
        r = round(r * 1000)
        embed.add_field(name="Conexión a base de datos ", value=f" **{r}** ms.")
    except:
        embed.add_field(name=":exclamation: No se pudo conectar con la base de datos", value=f"Si el problema persiste contactar a los desarrolladores.")
    await ctx.send(embed=embed)	

@client.command()
async def invite(ctx):
    """
    Muestra el link de invitación del bot.
    """
    embed = discord.Embed(title=f"", color=0xff9214)
    embed.add_field(name="**Invitación**", value=f"[Haz click aquí para obtener el enlace.](<{discord.utils.oauth_url(client.user.id)}>)")
    embed.set_footer(text=f"{botName} fue creado por Hatchens.com y es la nueva versión de Auguste.")
    await ctx.send(f"{ctx.author.mention}", embed=embed)

@client.group()
@commands.has_permissions(manage_messages=True)
async def say(ctx):
    """
    Anuncia algo en algún canal.
    """
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title=f"", description=f"**Haz un anuncio, con texto o en una embed.**\n```html\n{ctx.prefix}{ctx.command} embed|text```", color=discord.Color.red())
        await ctx.send(embed=embed)

@say.command()
async def text(ctx, channel: discord.TextChannel, *, text: str):
    """
    Para anunciar algo en un canal, se debe especificar el canal en dónde el anuncio será enviado y el texto.

    **Ejemplo de utilización**

    ``$say text #Anuncios Mañana habrá un anuncio muy importante a las 14:00.``
    """
    await channel.send(text) if channel else await ctx.send(text)

@say.command()
async def embed(ctx, channel: discord.TextChannel, title: str, text: str):
    """
    Para anunciar algo en un canal, se debe especificar el canal en dónde el anuncio será enviado y el texto.
    **Importante:** Para indicar el título y el texto es necesario ponerlo entre comillas.

    **Ejemplo de utilización**

    ``$say embed #Anuncios "Anuncio importante" "Mañana habrá un anuncio muy importante a las 14:00."``
    """
    embed = discord.Embed(title=title, description=text)
    await channel.send(embed=embed) if channel else await ctx.send(embed=embed)



@client.command()
@commands.is_owner()
async def reload(ctx, cog: str):
    """
    Comando con el propósito de ser utilizado solo por el desarrollador.
    """
    try:
        client.unload_extension(cog)
        client.load_extension(cog)
    except Exception as error:
        await ctx.send("> No se puso reiniciar cog, **error:**\n```{}```".format(error))
    


@client.event
async def on_ready():
    print('El bot está encendido.')
    numero = len(client.guilds)
    personas = sum(len(guild.members) for guild in client.guilds)
    game = discord.Game(f"$help | Estoy en {numero} servidores y hay en total {personas} miembros")
    await client.change_presence(status=discord.Status.online, activity=game)



if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print(error)

            


client.run('TOKEN')
