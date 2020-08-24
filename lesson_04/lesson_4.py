import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions
from random import randint, random

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
    a = ctx.guild.roles
    reason = 'None specified'
    a.reverse()
    for r in a:
        if r not in member.roles:
            if r in ctx.message.author.roles:
                channel = await member.create_dm()
                await channel.send(
                    f'{member.name}, you were banned from the server by {ctx.message.author}.'
                    f' | Reason: {reason}. You may contact them to appeal or get reinvited.'
                )
                await member.ban(reason=reason)
                print(ctx.message.content)
                await ctx.channel.send('%s has been banned by %s. Reason: %s' % (member, ctx.message.author, reason))


@client.command()
async def coin(ctx, call):
    if call == 'heads' or call == 'Heads' or call == 'HEADS':
        if random() <= 0.5:
            await ctx.channel.send('%s, you win!  The coin came up heads!' % ctx.message.author)
        else:
            await ctx.channel.send('%s, you lost!  The coin came up tails! Sorry! (not really)' % ctx.message.author)
    if call == 'tails' or call == 'Tails' or call == 'TAILS':
        a = random()
        if a >= 0.5:
            await ctx.channel.send('%s, you win!  The coin came up tails!' % ctx.message.author)
        else:
            await ctx.channel.send('%s, you lost!  The coin came up heads! Sorry! (not really)' % ctx.message.author)


client.run(TOKEN)
