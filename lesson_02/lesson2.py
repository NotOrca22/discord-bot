import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv("TOKEN")
client = discord.Client


@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        for member in guild.members:
            print(member)


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    else:
        await message.channel.send(f"{message.content}")
