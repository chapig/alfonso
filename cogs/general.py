import discord, psutil, distro, platform, time, asyncio
from discord.ext import commands

class General(commands.Cog):

    """
    > General commands.
    > **You will only find bot's latency (ping) command**
    > **and bot's invitation link.**  
    """

    def __init__(self, client):

        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """
        Check bot's latency.
        """
        before = time.monotonic()
        a = await ctx.send(embed=discord.Embed(title="", description="Checking latency..."))
        ping = (time.monotonic() - before) * 1000
        await a.delete(delay=1)
        await asyncio.sleep(1)
        embed = discord.Embed(title="", description=f"**Bot's latency**: \n**Ping:** `{round(self.client.latency * 1000)}` ms.\n**Pong**: `{int(ping)}` ms.")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def invite(self, ctx):
        """
        Send bot's invite link.
        """
        embed = discord.Embed(title=f"Invite {ctx.guild.me.name} to your server.", color=0xff9214)
        embed.add_field(name="**Invitación**", value=f"[Click here to get the link](<{discord.utils.oauth_url(self.client.user.id)}>)")
        embed.set_footer(text=f"{ctx.guild.me.name} was created by Chapi.")
        await ctx.send(embed=embed)

    @commands.command(aliases=['server'])
    async def serverinfo(self, ctx):
        """
        Detailed information about the server.
        """
        guild = ctx.guild
        embed = discord.Embed(
            color=discord.Color.blurple(),
            title=f"**{guild.name}**'s server info.",
            description="Detailed information about the server."
        )

        regions = {
            "us_west": ":flag_us: — US West",
            "us_east": ":flag_us: — US East",
            "us_central": ":flag_us: — US Central",
            "us_south": ":flag_us: — US South",
            "sydney": ":flag_au: — Australia - Sydney",
            "eu_west": ":flag_eu: — West Europe",
            "eu_east": ":flag_eu: — East Europe",
            "eu_central": ":flag_eu: — Central Europe",
            "singapore": ":flag_sg: — Singapore",
            "russia": ":flag_ru: — Russia",
            "southafrica": ":flag_za:  — South Africa",
            "japan": ":flag_jp: — Japan",
            "brazil": ":flag_br: — Brazil",
            "india": ":flag_in: — India",
            "hongkong": ":flag_hk: — Hong Kong",
        }
        verifications = {
            "ninguna": "<:white__circle:625695417782239234> — No Verification",
            "baja": "<:green_circle:625541294525251643> — Low Verification",
            "media": "<:yellow_circle:625540435820937225> — Medium Verification",
            "alta": "<:orange_circle:625542217100165135> — High Verification",
            "extrema": "<:red__circle:625833379258040330> — Extreme Verification"
        }
        embed.set_thumbnail(url=guild.icon_url_as(size=1024, format=None, static_format="png"))
        embed.add_field(name="Server's name:", value=str(guild.name))
        embed.add_field(name="Server's ID:", value=str(guild.id))
        embed.add_field(name="Server's owner: ", value=guild.owner)
        embed.add_field(name="Ownner's ID:", value=guild.owner_id)
        embed.add_field(name="Server created on:", value=guild.created_at.strftime("%A %d, %B %Y"))
        embed.add_field(name="Channels:", value=len(guild.channels))
        embed.add_field(name="Server's region:", value=regions[guild.region.name])
        embed.add_field(name="Members:", value=f"{guild.member_count}")
        embed.add_field(name="Nitro boosters:", value=guild.premium_subscription_count or "No current Nitro boosters.")

        await ctx.send(embed=embed)

        logger.info(f"Information | Sent Serverinfo : {ctx.author}")

def setup(client):
    client.add_cog(General(client))
