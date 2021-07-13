import os
import sqlite3
import sys
from datetime import datetime

import discord
from discord.ext import commands
from colorama import Style, Fore
from database.db import prefix

line_divide = "\n———————————————————————————————"

alfonso_token = ""

intents = discord.Intents.default()
intents.members = True
intents.presences = True

cogs = [
    "cogs.music", "cogs.configuration", "cogs.general", "cogs.help", "cogs.moderation",
    "cogs.comunidad", "error_handler.main", "cogs.matematicas"
]

def get_prefix(bot, message):

    prefix_guild = prefix(int(message.guild.id))

    try:
        if not message.guild:
            return "a!"
        else:
            return commands.when_mentioned_or(prefix_guild.name)(bot, message)
    except Exception:
        return commands.when_mentioned_or("a!")(bot, message)

class Alfonso(commands.AutoShardedBot):

    def __init__(self):

        super().__init__(command_prefix=get_prefix, intents=intents, owner_id=282598235003158528, reconnect=True, case_insensitive=False)

        self.embed_color = 0xF15A24
        self.console_info_format = f"{Fore.BLUE}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET} {Style.BRIGHT}[{Fore.BLUE}INFO{Fore.RESET}]{Style.RESET_ALL}"

        self.load_extension('jishaku')
        self.remove_command('help')
        self.loop.create_task(self.ready())

    async def on_connect(self):
        os.system("clear")
        print(f"{self.console_info_format} Alfonso is starting up...")

    async def ready(self):
        await self.wait_until_ready()
        os.system("clear")

        if not hasattr(self, 'uptime'):
            self.uptime = datetime.utcnow()

        try:
            for cog in cogs:
                self.load_extension(f"{cog}")
        except Exception as e:
            print(f"Could not load extension {e}")

        print(f"{self.console_info_format} Alfonso está iniciando."
              f"\n{self.console_info_format} Bot is online and connected to {self.user}"
              f"\n{self.console_info_format} Connected to {(len(self.guilds))} Guilds."
              f"\n{self.console_info_format} Detected Operating System: {sys.platform.title()}"
              f"\n{self.console_info_format} --------------------------------------------")

Alfonso().run(alfonso_token)
