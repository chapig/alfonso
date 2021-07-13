import discord
from discord.ext import commands
from ext.toollenize import Embed
from database.db import Roles
from cogs.help import cleanup_prefix

Roles = Roles()

class Moderation(commands.Cog):

    def __init__(self, client):

        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        In order to kick a user, it is necessary to indicate the user by mentioning them, or indicating their Discord ID.
        Placing the reason why it is kicked is optional.
        Example of use:
        `a!kick Chapi 1000 Did not follow the rule of not spam.`
        **For one member to be able to kick another member, they must have `KICK MEMBERS` permissions.**
        """
        if reason:

            await member.kick(reason=reason)
            await ctx.send(embed=Embed(title="",description=f"**{member}** has been kicked for the following reason: \n {reason}**", color=discord.Color.red()))

        else:

            await member.kick()
            await ctx.send(embed=Embed(title="", description=f"**{member}** has been kicked.", color=discord.Color.red()))

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """
        In order to mute a user, it is necessary to indicate the user by mentioning it, 
        or by indicating their Discord ID. Placing the reason for the mute is optional.

        **Example of use:**
        `a!mute Chapi#1000 did not follow the rule of not spamming.`
        **For a member to be able to mute another member, they must have the ``MUTE MEMBERS`` permissions.**

        **Configure custom role:**

        To set up a custom mute role, use
        ``a!set role mute @<role>`` 
        """
        if not reason:

            reason = 'no reason given.'
        
        else:

            reason = f'for the following reason: **{reason}**.'

        mute_role = Roles.get(self.client, 'mute', ctx.guild.id)
        if mute_role:
            
            await member.add_roles(mute_role)
            await ctx.send(
                embed=Embed(
                    color=discord.Color.red(), 
                    title=":mute: Member has been muted.",
                    description=f"**{member}** has been **muted** {reason}",
                    footer=f"Por: {ctx.author}"))
        else:

            mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
            if mute_role:
                await member.add_roles(mute_role)
                await ctx.send(
                    embed=Embed(
                        color=discord.Color.red(), 
                        title=":mute: Member has been muted.", 
                        description=f"**{member}** has been **muted** {reason}.",
                        footer=f"By: {ctx.author}"))

            else:

                await ctx.send(embed=Embed(
                    color=discord.Color.red(), 
                    title="Couldn't perform this operation.", 
                    description=f"""This server must either have a role named ``Muted`` 
                                or a **role configured to mute**. \n\n**In order to configure a role to mute members, use:**
                                ```html\n{cleanup_prefix(ctx.bot, ctx.prefix)}set role mute @Role\n```"""))

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """
        In order to mute a user, it is necessary to indicate the user by mentioning it, 
        or by indicating their Discord ID. Placing the reason for the mute is optional.

        **Example of use:**
        `a!unmute Chapi#1000 did not follow the rule of not spamming.`
        **For a member to be able to unmute another member, they must have the ``MUTE MEMBERS`` permissions.**

        **Configure custom role:**

        To set up a custom mute role, use
        ``a!set role mute @<role>`` 
        """
        if not reason:

            reason = 'no given reason.'
        
        else:

            reason = f'for the following reason: **{reason}**'

        mute_role = Roles.get(self.client, 'mute', ctx.guild.id)
        if mute_role:
            
            await member.remove_roles(mute_role)
            await ctx.send(
                embed=Embed(
                    color=discord.Color.red(), 
                    title=":mute: Member has been muted.",
                    description=f"**{member}** has been **muted** {reason}",
                    footer=f"By: {ctx.author}"))
        else:

            mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
            if mute_role:
                await member.remove_roles(mute_role)
                await ctx.send(
                    embed=Embed(
                        color=discord.Color.red(), 
                        title=":mute: Member has been muted.", 
                        description=f"**{member}** has been muted {reason}",
                        footer=f"By: {ctx.author}"))

            else:

                await ctx.send(embed=Embed(
                    color=discord.Color.red(), 
                    title="Couldn't perform this operation.", 
                    description=f"""This server must either have a role named ``Muted`` 
                                or a **role configured to mute**. \n\n**In order to configure a role to mute members, use:**
                                ```html\n{cleanup_prefix(ctx.bot, ctx.prefix)}set role mute @Role\n```"""))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, messages: int = None, *, reason=None):
        """
        **In order to ban a user you must indicate the user by mentioning them, or by indicating their Discord ID.** Placing the reason for the ban is optional as well as the messages to be deleted.
        
        **Example of use:**
        ``a!ban @Chapi#1000 5 Did not follow the rule of not spamming.``
        This would delete the member's messages from **5** days ago and ban them. When the days are not placed, it is assumed to be 0. **For a member to be able to ban another member they must have the ``BAN MEMBERS`` permissions.
        """
        if reason:

            await ctx.guild.ban(member, reason=reason, delete_message_days=messages if messages else 0)
            await ctx.send(embed=Embed(title="",description=f"Member has been banned for the following reason: **{reason}**.", color=discord.Color.red()))

        else:

            await ctx.guild.ban(member, delete_message_days=messages if messages else 0)
            await ctx.send(embed=Embed(title="",description="Member banned succesfully.", color=discord.Color.red()))


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Object, reason=None):
        """
        **In order to unban an user, it is necessary to indicate the user by mentioning them, or by indicating their Discord ID.** Giving a reason for which they are unbanned is optional.
        
        **Example of use:**
        ``a!unban 282598235003158528 Time of suspension completed.``
        **For a member to be able to ban another member they must have the ``BAN MEMBERS`` permissions.``
        """
        if reason:

            await ctx.guild.unban(member, reason=reason)
            await ctx.send(embed=Embed(title="", description=f"Member has been **unbanned** succesfully: \n**{reason}**.", color=discord.Color.blue()))
        
        else:

            await ctx.guild.unban(member)
            await ctx.send(embed=Embed(title="", description="Member has been **unbanned** succesfully.", color=discord.Color.blue()))


def setup(client):
    client.add_cog(Moderation(client))
