import emoji
import discord

def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False

def text_has_digits(s):
    return any(i.isdigit() for i in s)

def Embed(title=None, description=None, footer=None, author=None, author_img= None, thumbnail=None, color=None):

    embed = discord.Embed(

        title = title,
        description = description,
        color = color if color else None
    )

    embed.set_footer(text=footer) if footer else None
    
    embed.set_author(name=author, icon_url=author_img) if author and author_img else None

    embed.set_thumbnail(url=thumbnail) if thumbnail else None

    return embed