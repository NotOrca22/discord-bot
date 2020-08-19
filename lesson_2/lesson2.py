import discord
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = "NzQ0OTY3NTg3ODI5MzgzMTk5.Xzq7IQ.sDfHpFzf4E2yQ0lq1yYsV3a2ha4"
GUILD = os.getenv('Python Bot Making Class')
client = discord.Client()

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
    if message.author == client.user:
        return
    else:
        await message.channel.send('%s' % message.content)

client.run(TOKEN)