import discord
import os
from discord.ext import commands
TOKEN = "NzQ0OTY3NTg3ODI5MzgzMTk5.Xzq7IQ.Jnkka2fQo85bPC1Gk_INr_uQz8Y"
client = commands.Bot(command_prefix='!', case_insensitive=True)
from discord.ext.commands import has_permissions

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
async def kick(ctx, member:discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send("%s has been kicked by %s. Reason: %s." % (member, ctx.message.author, reason))
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send("%s has been banned by %s. Reason: %s." % (member, ctx.message.author, reason))
client.run(TOKEN)