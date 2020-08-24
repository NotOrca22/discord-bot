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
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member.name, member.discriminator = member.split('#')

    for bu in banned_users:
        user = bu.user
        if (user.name, user.discriminator) == (member.name, member.discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}.')


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


@client.command()
@has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member = None, *, reason=None):
    if member == ctx.message.author:
        await ctx.channel.send('You cannot mute yourself. Orca-Bot-Whale does not allow self-harm.')
    elif member is None:
        await ctx.channel.send('You cannot mute nobody you imbecile!')
    else:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        print(ctx.message.content)
        if not member:
            await ctx.channel.send('Please specify a member to mute')
            return
        await member.add_roles(role)
        await ctx.channel.send('%s has been successfully muted by %s' % (member, ctx.message.author))
        channel = await member.create_dm()
        await channel.send(
            f'{member.name}, you were muted in the server by {ctx.message.author}.'
            f' | Reason: %s. You may contact them to appeal the mute.' % reason
        )


@client.command()
@has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    print(ctx.message.content)
    if not member:
        await ctx.channel.send('Please specify a member to unmute.')
        return
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.channel.send('%s has been successfully unmuted by %s' % (member, ctx.message.author))
        channel = await member.create_dm()
        await channel.send(
            f'{member.name}, you were unmuted in the server by {ctx.message.author}.  Great!'
        )
    else:
        await ctx.channel.send('%s was never muted in the first place, %s!' % (member, ctx.message.author))


@client.command()
@has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    if member:
        await ctx.channel.send('%s, you have been warned by %s.  Reason: %s' % (member, ctx.message.author, reason))
    else:
        await ctx.channel.send('%s, please specify a member to warn' % (ctx.message.author))
    channel = await member.create_dm()
    await channel.send(
        f'{member.name}, you were warned in the server by {ctx.message.author}.'
        f' | Reason: %s.' % reason
    )


client.run(TOKEN)
