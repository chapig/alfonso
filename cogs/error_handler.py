import discord, traceback, sys
from discord.ext import commands
from cogs.help import cleanup_prefix


class error_handler(commands.Cog):

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
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in private messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                embed = discord.Embed(title="", description=f"Couldn't find member.", color=discord.Color.red())
                await ctx.send(embed=embed)


        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                embed = discord.Embed(title=f"", description=f"{ctx.command.help}\n```html\n{cleanup_prefix(ctx.bot, ctx.prefix)}{ctx.command} {ctx.command.signature}```", color=discord.Color.red())
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            try:
                embed = discord.Embed(title="", description=f"Not enough permissions.", color=discord.Color.red())
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingAnyRole):
            try:
                embed = discord.Embed(title="", description=f"You don't have a role that this command requires.", color=discord.Color.red())
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            try:
                embed = discord.Embed(title="", description=f"Wait a few seconds before using this command.", color=discord.Color.red())
                await ctx.send(embed=embed, delete_after=5)
            except discord.HTTPException:
                pass
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

                
def setup(client):
    client.add_cog(error_handler(client))