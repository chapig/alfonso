import discord
import traceback
import sys
from discord.ext import commands
from cogs.help_mod import cleanup_prefix
from cogs.base_moddb import connection 
import pyodbc




class Configuracion(commands.Cog):

    def __init__(self, client):
        self.client = client
    
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} ha sido desabilitado.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} no puede ser usado en mensajes privados.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                embed = discord.Embed(title="", description=f"No pude encontrar ese miembro.", color=discord.Color.red())
                await ctx.send(embed=embed)


        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                embed = discord.Embed(title=f"", description=f"{ctx.command.help}\n```html\n{cleanup_prefix(ctx.bot, ctx.prefix)}{ctx.command} {ctx.command.signature}```", color=discord.Color.red())
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            try:
                embed = discord.Embed(title="", description=f"No tienes permisos suficientes para realizar esta acción.", color=discord.Color.red())
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingAnyRole):
            try:
                embed = discord.Embed(title="", description=f"No tienes el role necesario para realizar esta acción.", color=discord.Color.red())
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            try:
                embed = discord.Embed(title="", description=f"Espera unos segundos antes de utilizar este comando.", color=discord.Color.red())
                await ctx.send(embed=embed, delete_after=5)
            except discord.HTTPException:
                pass
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        """
        Este comando es utilizado para la configuración del bot. De aquí sale una rama de comandos que son utilizados para configurar al bot y personalizarlo en tu servidor.
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=f"", description=f"Configuración.", color=discord.Color.red())
            await ctx.send(embed=embed)
    
    @config.command()
    async def muterole(self, ctx, role: discord.Role):
        """
        Añade o actualiza el role que será colocado cuando un miembro sea muteado o en su caso, removido en caso de ser desmuteado.

        **Ejemplo de utilización con role:**
        ``$config muterole @Muted``
        """
        get_role = connection()
        try:
            get_role.update_mute_role(ctx.guild.id, role.id)
            embed = discord.Embed(title="", description=f"El role {role.mention} ahora será el role que será añadido al momento de **mutear/desmutear** a alguien.")
            await ctx.send(embed=embed)
        except Exception as error:
            print(error)
            await ctx.send("Lo siento, ha ocurrido un error al actualizar el role. Intenta más tarde.")
        
    @config.command()
    async def mod(self, ctx, role: discord.Role = None):
        """
        Añada un role con permisos de moderación que permitirán al miembro con dicho role
        utilizar los comandos de moderación, para conocer los comandos de **moderación**
        utilize ``$help Moderacion``

        **Ejemplo de utilización con role: (Se debe mencionar el role)**
        ``$config mod @Moderador``
        """
        get_role = connection()
        try:
            if role:
                get_role.update_moderators(ctx.author.id, role.id)
                embed = discord.Embed(title="", description=f"El role {role.mention} ahora será el role de **moderación** en los comandos de este bot.")
                await ctx.send(embed=embed)
            else:
                try:
                    role = get_role.get_mod_roles(guild=ctx.guild.id)
                except Exception:
                    role = None
                role = ctx.guild.get_role(int(role)) if role else None
                if role:
                    descripcion = f"El role {role.mention} es el role de **moderación** en los comandos de **moderación** de este bot."
                else:
                    descripcion = "No hay ningún role para moderación, por **default** los miembros con permisos de **administración** podrán utilizar los comandos de **moderación**"
                embed = discord.Embed(title="", description=descripcion)
                await ctx.send(embed=embed)
        except Exception as error:
            print(error)
            await ctx.send("Lo siento, ha ocurrido un error al actualizar el role. Intenta más tarde.")



    # @commands.command()
    # @has_permissions(administrator=True)
    # async def economy(self, ctx):
    #     try:
    #         if db.detect_economy_config(ctx.guild.id)[1] == "0":
    #             db.config_economy_server(ctx.guild.id)
    #             embed = discord.Embed(title=f":nut_and_bolt: La economía ha sido activada", color=discord.Color.green())
    #             embed.add_field(name="Información:", value=f"Ahora los usuarios podrán utilizar los comandos relacionados con la economía. Para desactivarla, usar ``$economy``, este comando también se utiliza para desactivarla. \n\n> Los datos no se perderán y seguirán almacenados aún así estando apagado el módulo de economía.")
    #             embed.set_footer(text=f"Configuración | Economía - {ctx.author}")
    #             await ctx.send(embed=embed)
    #         else:
    #             if db.detect_economy_config(ctx.guild.id)[1] == "1":
    #                 db.config_economy_server(ctx.guild.id)
    #                 embed = discord.Embed(title=f":nut_and_bolt: La economía ha sido desactivada", color=0xff4d4d)
    #                 embed.add_field(name="Información:", value=f"**Ahora los usuarios no podrán utilizar los comandos relacionados con la economía, los datos seguirán siendo almacenados y no se perderán.** Para reactivarla, usar ``$economy``, este comando también se utiliza para desactivarla.")
    #                 embed.set_footer(text=f"Configuración | Economía - {ctx.author}")
    #                 await ctx.send(embed=embed)
    #     except Exception:
    #         db.detect_economy_config(ctx.guild.id)
    #         db.create_db_e(ctx.guild.id)
    #         await self.economy(ctx)
            
    # @economy.error
    # async def economy_handler(self, ctx, error):
    #     """A local Error Handler for our command do_repeat.
    #     This will only listen for errors in do_repeat.
    #     The global on_command_error will still be invoked after.
    #     """
    #     # Check if our required argument inp is missing.
    #     if isinstance(error, commands.MissingPermissions):
    #       embed = discord.Embed(title="", description=f"No puedes utilizar este comando. Necesitas permisos de **Administrador**.", color=discord.Color.red())
    #       await ctx.send(embed=embed)

    # @commands.command()
    # @has_permissions(administrator=True)
    # async def currency(self, ctx, arg = None):
    #     if arg is not None:
    #         if len(arg) < 3:
    #             db.currency(ctx.guild.id, arg)
    #         else:
    #             await ctx.send("No se pueden color más de 2 caracteres.")
    #     else:
    #         await ctx.send("Esta es la moneda del servidor ``{}``".format(db.currency(ctx.guild.id)))

                
def setup(client):
    client.add_cog(Configuracion(client))
    print('El módulo de Configuración cargó correctamente.')