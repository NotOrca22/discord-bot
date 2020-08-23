import discord
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = "NzQ1MzU5OTg5NDEyOTg2OTcw.XzwolQ.VmKjN_-s1TpTAN7crrRdAwoSvdw"
GUILD = os.getenv('Python Bot Making Class 3-4')
client = discord.Client()
@client.event
async def on_ready():
    for guild in client.guilds():
        print("{} has connected to {}".format(client, guild.name))
        for member in guild.members:
            print(member.name)
client.run(TOKEN)

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    else:
        await message.channel.send(f"{message.content}")
