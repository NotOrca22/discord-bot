import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions

TOKEN = os.getenv("TOKEN")
client = commands.Bot(command_prefix='!', case_insensitive=True)


@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        for member in guild.members:
            print(member)


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f"{member} has been kicked by {ctx.message.author}. Reason: {reason}.")


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f"{member} has been banned by {ctx.message.author}. Reason: {reason}.")


client.run(TOKEN)
