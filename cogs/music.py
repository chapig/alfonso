import math
import os
import re
import aiohttp
import discord
import lavalink
from discord.ext import commands

url_rx = re.compile(r'https?://(?:www\.)?.+')

class musica(commands.Cog):

    def __init__(self, bot):
        
        self.bot = bot
        self.votes = []

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('127.0.0.1', 2333, 'Runningboy12?', 'us', 'default-node')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        #lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    """
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
    """  # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))

        should_connect = ctx.command.name in ('play', )  # Add commands that require joining voice to work.
        should_not_connect = ctx.command.name in ('lyrics', )

        if should_not_connect:
            return

        if not ctx.author.voice or not ctx.author.voice.channel:
            embed = discord.Embed(
                color=0xffa8e0,
                title="There was an error when attempting this action.",
                description="Make sure to be in a voice channel."
            )
            raise commands.CommandInvokeError(await ctx.send(embed=embed))

        if not player.is_connected:
            if not should_connect:
                embed = discord.Embed(
                    color=0xffa8e0,
                    title="There was an error when attempting this action.",
                    description="Bot is not connected to the voice chat."
                )
                raise commands.CommandInvokeError(await ctx.send(embed=embed))

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                embed = discord.Embed(
                    color=0xffa8e0,
                    title="Insufficient permissions.",
                    description="Bot requires permissions to join voice channels as well as, permissions to be able to speak."
                )
                await ctx.send(embed=embed)

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                embed = discord.Embed(
                    color=0xffa8e0,
                    title="First, do the following.",
                    description="Make sure you're on the same voice channel as your bot."
                )
                raise commands.CommandInvokeError(await ctx.send(embed=embed))

    # async def track_hook(self, event):
    #     if isinstance(event, lavalink.events.QueueEndEvent):
    #         guild_id = int(event.player.guild_id)
    #         await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """ Search and play a song. """

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            embed = discord.Embed(
                color=0xffa8e0,
                title="There was an error when attempting to play the song.",
                description="There was no result with your search."
            )
            return await ctx.send(embed=embed)

        # position = lavalink.utils.format_time(player.position)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed = discord.Embed(color=0xffa8e0,
                                description=f'• **{results["playlistInfo"]["name"]}** - {len(tracks)} tracks',
                                title="Playlist added.")
            embed.set_thumbnail(url=f'https://img.youtube.com/vi/{track["info"]["identifier"]}/default.jpg')
            await ctx.send(embed=embed)
        else:
            track = results['tracks'][0]

            embed = discord.Embed(color=0xffa8e0,
                                description=f'• [**{track["info"]["title"]}**]({track["info"]["uri"]})',
                                title="Song added to the queue.")
            embed.set_thumbnail(url=f'https://img.youtube.com/vi/{track["info"]["identifier"]}/default.jpg')

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

            await ctx.send(embed=embed)

            if not player.is_playing:
                await player.play()
            
            TTSG.activate_music(ctx.guild.id)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=0xffa8e0,
                title="Play music.",
                description="In order to play music, use `a!play <Song's name | Song's URL>`."
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def lyrics(self, ctx, *, song):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.ksoft.si/lyrics/search",
                              params={"q": song},
                              headers={"Authorization": f"Bearer {os.environ.get('ksoft_key')}"}) as r:
                res = await r.json()

                title = res["data"][0]["name"]
                song_picture = res["data"][0]["album_art"]

                try:
                    lyrics = res["data"][0]["lyrics"]
                except IndexError:
                    lyrics = "No se encontró esta letra."

                if len(lyrics) > 2048:
                    embed = discord.Embed(
                        color=0xffa8e0,
                        title=f"→ {title}",
                        description=lyrics[:2047]
                    )
                    embed.set_thumbnail(url=song_picture)
                    embed.set_footer(text="KSoft.Si", icon_url="https://cdn.ksoft.si/images/Logo1024.png")

                    await ctx.send(embed=embed)

                    embed1 = discord.Embed(
                        color=0xffa8e0,
                        description=lyrics[2048:]
                    )
                    embed1.set_footer(text="KSoft.Si", icon_url="https://cdn.ksoft.si/images/Logo1024.png")

                    await ctx.send(embed=embed1)
                    return

                embed = discord.Embed(
                    color=0xffa8e0,
                    title=f"→ {title}",
                    description=lyrics
                )
                embed.set_thumbnail(url=song_picture)
                embed.set_footer(text="KSoft.Si", icon_url="https://cdn.ksoft.si/images/Logo1024.png")

                await ctx.send(embed=embed)

    @lyrics.error
    async def lyrics_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=0xffa8e0,
                title="How to search for lyrics.",
                description="Command usage: `a!lyrics <Song's name>`"
            )

            await ctx.send(embed=embed)

    @commands.command()
    async def seek(self, ctx, *, seconds: int):
        """ Play the song at an exact timestamp. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)

        embed = discord.Embed(
            color=0xffa8e0,
            title="Song timestamp was changed.",
            description=f"Song's now playing at: `{lavalink.utils.format_time(track_time)}`"
        )
        await ctx.send(embed=embed)

    @seek.error
    async def seek_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=0xffa8e0,
                title="How to choose a timestamp.",
                description="`a!seek <timestamp in seconds>`"
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        """ Skip current song. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        await player.skip()
        embed = discord.Embed(
            color=0xffa8e0,
            title="Song has been skipped.",
            description="The song that was playing was skipped."
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def stop(self, ctx):
        """ Stop playing music and delete its current queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No songs are being played.",
                description="First, add songs to the queue."
            )
            return await ctx.send(embed=embed)

        player.queue.clear()
        await player.stop()

        embed = discord.Embed(
            color=0xffa8e0,
            title="Music has been stopped.",
            description="Music has been stopped, bot has left the channel."
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['np', 'n', 'playing'])
    async def now(self, ctx):
        """ Show status of current song. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.current:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No songs are being played.",
                description="First, add songs to the queue."
            )
            return await ctx.send(embed=embed)

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 Live Video'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**• [{player.current.title}]({player.current.uri})**'

        embed = discord.Embed(
            color=0xffa8e0,
            title='Playing now:',
            description=f"{song}"
                        f"\n**•** Timestamp: **({position}/{duration})**."
        )
        embed.set_thumbnail(url=f'https://img.youtube.com/vi/{player.current.identifier}/default.jpg')
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int = 1):
        """ Show current queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No songs in the queue.",
                description="In order to add songs to the queue, use the `a!play` command."
            )
            return await ctx.send(embed=embed)

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(
            color=0xffa8e0,
            title="List of songs:",
            description=f"\n{queue_list}"
        )
        # embed.set_author(name=f'→ List of songs: {len(player.queue)} \n\n{queue_list}')
        embed.set_footer(text=f'Page {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        """ Pause or resume the song. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No music is being played.",
                description="No music is being played at this moment."
            )
            return await ctx.send(embed=embed)

        if player.paused:
            await player.set_pause(False)
            embed = discord.Embed(
                color=0xffa8e0,
                title="Song has been resumed.",
                description="The song is now being played again."
            )
            await ctx.send(embed=embed)
        else:
            await player.set_pause(True)
            embed = discord.Embed(
                color=0xffa8e0,
                title="Song has been paused.",
                description="Song has been paused for now, in order to resume it, use ``a!resume``."
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['v'])
    async def volume(self, ctx, volume: int = None):
        """ Change bot's volume (1-100) """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not volume:
            embed = discord.Embed(
                color=0xffa8e0,
                title="Current volumen:",
                description=f"**{player.volume}%**."
            )
            return await ctx.send(embed=embed)

        await player.set_volume(volume)  # Lavalink will automatically cap values between, or equal to 0-1000.

        embed = discord.Embed(
            color=0xffa8e0,
            title="Bot's volume has been changed.",
            description=f"Current volume is **{player.volume}%**."
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['shuff'])
    async def shuffle(self, ctx):
        """ Activate or deactivate **shufle** mode. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No music is being played right now.",
                description="To use the shuffle function, a song must be playing."
            )
            return await ctx.send(embed=embed)

        player.shuffle = not player.shuffle
        embed = discord.Embed(
            color=0xffa8e0,
            title="Shuffle.",
            description="Shuffle has been"
                        + (' **activated**' if player.shuffle else ' **deactivated**.')
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['loop'])
    async def repeat(self, ctx):
        """ Repeat the current song on a loop until the command is invoked again. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No song is playing right now.",
                description="Nothing to repeat."
            )
            return await ctx.send(embed=embed)

        player.repeat = not player.repeat
        embed = discord.Embed(
            color=0xffa8e0,
            title="Loop (Music)",
            description="Looping has been" + (' **activated**' if player.repeat else ' **deactivated**.')
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['rm'])
    async def remove(self, ctx, index: int):
        """ Removes an item from the queue by typing the index of the item in the queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No song in the queue.",
                description="There are no songs to remove."
            )
            return await ctx.send(embed=embed)

        if index > len(player.queue) or index < 1:
            embed = discord.Embed(
                color=0xffa8e0,
                title="There was an error when attempting to remove song.",
                description=f"Indicated number was {len(player.queue)}."
            )
            return await ctx.send(embed=embed)
        removed = player.queue.pop(index - 1)  # Account for 0-index.

        embed = discord.Embed(
            color=0xffa8e0,
            title="Song has been removed.",
            description=f"Song has been removed `{removed.title}` from the queue."
        )
        await ctx.send(embed=embed)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=0xffa8e0,
                title="Invalid argument.",
                description="Use a valid argument `a!remove 1`."
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["find"])
    async def search(self, ctx, *, query):
        """ Search for a song. """
        o_query = query
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            embed = discord.Embed(
                color=0xffa8e0,
                title="No results.",
                description="No result in given query."
            )
            return await ctx.send(embed=embed)

        tracks = results['tracks'][:10]  # First 10 results

        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'

        embed = discord.Embed(
            color=0xffa8e0,
            title=f"Results for {o_query.capitalize()}.",
            description=f"{o}"
        )
        await ctx.send(embed=embed)

    @search.error
    async def find_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=0xffa8e0,
                title="Command usage.",
                description="Example of command usage: `a!search <song>`."
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['leave'])
    async def disconnect(self, ctx):
        """ Disconnect bot from voice channel. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            embed = discord.Embed(
                color=0xffa8e0,
                title="You are not in a voice channel.",
                description="You must be in a voice channel to use this command."
            )
            return await ctx.send(embed=embed)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed = discord.Embed(
                color=0xffa8e0,
                title="Must be in same voice channel.",
                description="You must be in the same voice channel where the bot is."
            )
            return await ctx.send(embed=embed)

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)

        embed = discord.Embed(
            color=0xffa8e0,
            title="Disconnected.",
            description="Bot has been **disconnected** from the voice channel."
        )
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(musica(bot))
