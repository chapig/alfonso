import discord
from discord.ext import commands
from database.db import prefix as pfx
from database.db import Roles, Emoji_in_Prefix, TooLong, Number_in_Prefix
from ext.toollenize import text_has_digits, text_has_emoji
from ext.toollenize import Embed

Roles = Roles()


class Configuration(commands.Cog):

    """
    > Set up the bot and personalize it. \n> Change server's bot prefix and more.
    """

    def __init__(self, client):

        self.client = client 

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefijo: str = None):
        
        """
        Modify or show server's prefix.
        **Only members** with **administrator** permissions can use this bot.

        """

        try:

            guild = pfx(int(ctx.guild.id))

            if prefijo:

                guild.modify(str(prefijo))
                await ctx.send(embed=Embed(title="Server's prefix has been changed.", description="\nServer's prefix now is `%s`." % guild.name, color=discord.Color.gold()))
            
            else:
                await ctx.send(embed=Embed(title="Server's prefix.", description="\nServer's prefix is `%s`." % guild.name, color=discord.Color.gold()))

        except Emoji_in_Prefix:

            await ctx.send(embed=Embed(title=None, description="You can't use **emojis** as a prefix.", color=discord.Color.red()))
        
        except TooLong:

            await ctx.send(embed=Embed(title=None, description="This prefix is too large.", color=discord.Color.red()))
        
        except Number_in_Prefix:

            await ctx.send(embed=Embed(title=None, description="You can't use digits as a prefix.", color=discord.Color.red()))
        
        except Exception:
            try:
                await ctx.send(embed=Embed(title=None, description="This server's default prefix is ``a!`` or also mentioning the **bot**. To set up a prefix, use \n```html\n@Alfonso prefix <prefix>\n```", color=discord.Color.blue()))
            except Exception as error:
                print(error)
    @commands.group()
    async def set(self, ctx):
        """
        Set configuration.
        """
        if ctx.invoked_subcommand is None:

            await ctx.send(embed=Embed(title="", description=f"{ctx.command.help}", color=discord.Color.red()))
    
    @set.command()
    async def role(self, ctx, role_options: str, role: discord.Role):
        """
        To activate and improve functions like ``mute``, it is necessary to have a role named ``Muted``
        or add your custom role.

        **Usage:**
        ``a!set role mute @Cannot Speak`` (You must mention the role)
        """
        try:
            Roles.add(self.client, role_options, role, ctx.guild.id)
            await ctx.send(embed=Embed(color=discord.Color.blurple(), title="", description=f"You've succesfully modified ``{role_options.upper()}``'s role option. \nNew role added: {role.mention}."))
        except Exception as error:
            await ctx.send(error)
     
def setup(client):
    client.add_cog(Configuration(client))        
