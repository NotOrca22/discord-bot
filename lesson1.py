import discord
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = 'NzQzMTQ3NTcwMjM4NTg2OTUw.XzQcGw.H6irisFG1VzettI4iOsiYG72Eh0'
GUILD = os.getenv('Python Bot Making Class')
client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await message.channel.send('%s' % message.content)

client.run(TOKEN)