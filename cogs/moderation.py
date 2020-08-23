import discord
from discord.ext import commands
import datetime
import os
import pyodbc
import json
from cogs.database.configuration import connection 

mute = connection()
mute.get_muted_roles()

class Moderacion(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, razon: str = None):
        """
        Para kickear a un usuario es necesario indicar el usuario mencionándole, o indicando su ID.
        Colocar la razón por la cuál es kickeado es opcional.
        Ejemplo de utilización:

        ``$kick Chapi#1000 No siguió la norma de no hacer spam.``

        **Para un miembro poder kickear a otro debe poseer el permiso de ``KICK MEMBERS`` activado.**
        """
        if razon:
            await user.kick(reason=razon)
            descripcion = f"El miembro **{user.name}** ha sido kickeado del servidor, por la razón siguiente:\n**{razon}**"
            embed = discord.Embed(title="", description=f"{descripcion}")
            embed.set_footer(text=f"Kickeado por el miembro: {ctx.author} | Moderación")
            await ctx.send(embed=embed)
        else:
            await user.kick()
            descripcion = f"El miembro **{user.name}** ha sido kickeado del servidor."
            embed = discord.Embed(title="", description=f"{descripcion}")
            embed.set_footer(text=f"Kickeado por el miembro: {ctx.author} | Moderación")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, mensajes: int = None, *, razon: str = None):
        """
        **Para banear a un usuario es necesario indicar el usuario mencionándole, o indicando su ID.** Colocar la razón por la cuál es baneado es opcional al igual que los mensajes a borrar.
        
        **Ejemplo de utilización:**

        ``$unban @Chapi#1000 5 No siguió la norma de no hacer spam.``

        Esto borraría los mensajes del miembro desde hace **5** días atrás y le banearía. Cuando los días no son colocados, se asume que es 0. **Para un miembro poder banear a otro debe poseer el permiso de ``BAN MEMBERS`` activado.**
        """
        if razon:
            await ctx.guild.ban(user, reason=razon, delete_message_days=mensajes if mensajes else 0)
            descripcion = f"El miembro **{user.name if user.name else user}** ha sido baneado del servidor, por la razón siguiente: \n**{razon}**"
            embed = discord.Embed(title="", description=f"{descripcion}")
            embed.set_footer(text=f"Baneado por el miembro: {ctx.author} | Moderación")
            await ctx.send(embed=embed)
        else:
            await ctx.guild.ban(user, delete_message_days=mensajes if mensajes else 0)
            descripcion = f"El miembro **{user.name if user.name else user}** ha sido baneado del servidor."
            embed = discord.Embed(title="", description=f"{descripcion}")
            embed.set_footer(text=f"Baneado por el miembro: {ctx.author} | Moderación")
            await ctx.send(embed=embed)

    @commands.command(aliases=['desban','pardon'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.Object, *, razon: str = None):
        """
        **Para desbanear a un usuario es necesario indicar el usuario mencionándole, o indicando su ID.** Colocar la razón por la cuál es desbaneado es opcional.
        
        **Ejemplo de utilización:**

        ``$unban 282598235003158528 Tiempo de suspensión cumplido.``

        **Para un miembro poder banear a otro debe poseer el permiso de ``BAN MEMBERS`` activado.**
        """
        if razon:
            await ctx.guild.unban(user, reason=razon)
            descripcion = f"El miembro ha sido desbaneado del servidor, por la razón siguiente: \n**{razon}**"
            embed = discord.Embed(title="", description=f"{descripcion}")
            embed.set_footer(text=f"Acción hecha por: {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.guild.unban(user)
            descripcion = f"**El miembro ha sido desbaneado del servidor.**"
            embed = discord.Embed(title="", description=f"{descripcion}")
            embed.set_footer(text=f"Desbaneado por: {ctx.author} | Moderación")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, user: discord.Member, *, razon: str = None):
        """
        **Para mutear a un usuario es necesario indicar el usuario mencionándole, o indicando su ID.** Colocar la razón por la cuál es muteado es opcional.
        
        **Ejemplo de utilización:**

        ``$mute @Chapi#1000 Hizo spam en #general``

        **Para un miembro poder mutear a otro debe poseer el permiso de ``ADMINISTRATOR`` activado. (Actualización a role personalizado pronto)**
        """      

        mute.get_muted_roles()

        try:
            if str(ctx.guild.id) in mute.muted_roles and mute.muted_roles[str(ctx.guild.id)] is not None and mute.muted_roles[str(ctx.guild.id)] != 0:
                mute_role = ctx.guild.get_role(int(mute.muted_roles[str(ctx.guild.id)]))
                await user.add_roles(mute_role, reason=razon if razon else None)
                embed = discord.Embed(title="", description=f"**El miembro {user.mention} ha sido muteado.** {f'Por la razón siguiente: **{razon}**' if razon is not None else ''}")
                embed.set_footer(text=f"Muteado por el miembro: {ctx.author} | Moderación")
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Configuración", description=f"Antes de mutear a un miembro, es necesario configurar un **role** que será asignado para el miembro muteado. Utilize ``{ctx.prefix}config muterole <@role>`` para asignar el role.")
                embed.set_footer(text=f"Configuración de muteo | Pasos a seguir")
                await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(title="No tengo los permisos suficientes", description=f"Esto significa que el bot es menor en la lista de roles que la persona o rol que está intentando editar, o que el bot está intentando editar el propietario del servidor, lo que no puede suceder.")
            embed.set_footer(text=f"Configuración de muteo | Pasos a seguir")
            await ctx.send(embed=embed)

            

    @commands.command()
    async def unmute(self, ctx, user: discord.Member, *, razon: str = None):
        """
        **Para desmutear a un usuario es necesario indicar el usuario mencionándole, o indicando su ID.** Colocar la razón por la cuál es desmuteado es opcional.
        
        **Ejemplo de utilización:**

        ``$unmute @Chapi#1000 Hizo spam en #general``

        **Para un miembro poder desmutear a otro debe poseer el permiso de ``ADMINISTRATOR`` activado. (Actualización a role personalizado pronto)**
        """   

        mute.get_muted_roles()

        try:
            if str(ctx.guild.id) in mute.muted_roles and mute.muted_roles[str(ctx.guild.id)] is not None and mute.muted_roles[str(ctx.guild.id)] != '0':
                mute_role = ctx.guild.get_role(int(mute.muted_roles[str(ctx.guild.id)]))
                await user.remove_roles(mute_role, reason=razon if razon else None)
                embed = discord.Embed(title="", description=f"**El miembro {user.mention} ha sido desmuteado.** {f'Por la razón siguiente: **{razon}**' if razon is not None else ''}")
                embed.set_footer(text=f"Desmuteado por el miembro: {ctx.author} | Moderación")
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Configuración", description=f"Antes de desmutear a un miembro, es necesario configurar un **role** que será asignado para el miembro muteado. Utilize ``{ctx.prefix}config muterole <@role>`` para asignar el role.")
                embed.set_footer(text=f"Configuración de muteo | Pasos a seguir")
                await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(title="No tengo los permisos suficientes", description=f"Esto significa que el bot es menor en la lista de roles que la persona o rol que está intentando editar, o que el bot está intentando editar el propietario del servidor, lo que no puede suceder.")
            embed.set_footer(text=f"Configuración de muteo | Pasos a seguir")
            await ctx.send(embed=embed)


    @commands.group()
    async def warn(self, ctx):
        """
        El comando **warn** es utilizado para advertir a un miembro sobre algo.

        **Hay dos utlizaciones del comando:**

        ``$warn privately @Chapi#1000 Estás rompiendo la regla número 4.``

        ``$warn default @Chapi#1000 Estás rompiendo la regla número 4.``

        Para tener acceso a estos comandos, el miembro debe tener permisos de **administrador** o configurar un rango
        con ``$config moderation``.
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=f"", description=f"{ctx.command.help}", color=discord.Color.red())
            await ctx.send(embed=embed)

    @warn.command()
    async def privately(self, ctx, user: discord.Member, *, razon):
        """
        Advierte a un jugador mandándole un mensaje privado. Colocar la razón es **obligatorio**.

        **Utilización del comando:**

        ``$warn privately @Chapi#1000 Estás rompiendo la regla número 7.``

        Para tener acceso a estos comandos, el miembro debe tener permisos de **administrador** o configurar un rango
        con ``$config moderation``.
        """
        try:
            embed = discord.Embed(title=f"Has sido advertido.", description=razon, color=discord.Color.red())
            embed.set_footer(text="Servidor: {} | Advertido por: {}".format(ctx.guild.name, ctx.author))
            await user.send(embed=embed)
        except Exception as error:
            print(error)
            embed = discord.Embed(title=f"Warn falló al ser enviado.", description="Esta persona no permite mensajes privados. Intente advertirle con ``default``.", color=discord.Color.red())
            embed.set_footer(text="Servidor: {} | Intendo de warn por: {}".format(ctx.guild.name, ctx.author))
            await ctx.send(embed=embed)

    @warn.command()
    async def default(self, ctx, user: discord.Member, *, razon):
        """
        Advierte a un jugador. Colocar la razón es **obligatorio**.

        **Utilización del comando:**

        ``$warn default @Chapi#1000 Estás rompiendo la regla número 7.``

        Para tener acceso a estos comandos, el miembro debe tener permisos de **administrador** o configurar un rango
        con ``$config moderation``.
        """
        embed = discord.Embed(title=f":bell: Has sido advertido por romper las reglas", description=razon, color=discord.Color.red())
        embed.set_footer(text="Servidor: {} | Advertido por: {}".format(ctx.guild.name, ctx.author))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Moderacion(client))