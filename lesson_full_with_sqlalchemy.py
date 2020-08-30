import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from random import randint, random
import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# please install sqlalchemy package by pip/pip3 install sqlalchemy
Base = declarative_base()
load_dotenv()

TOKEN = os.getenv("TOKEN")
HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


class DiscordAccount(Base):
    __tablename__ = 'dicord_currency'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    wallet = Column(Integer)
    bank = Column(Integer)


engine = create_engine(f'mysql://{USERNAME}:{PASSWORD}@{HOST}:3306/{DATABASE}')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

client = commands.Bot(command_prefix='!', case_insensitive=True)

s = session()


@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        user_ids = map(lambda account: account.user_id, s.query(DiscordAccount).all())
        for member in guild.members:
            if int(member.id) not in user_ids:
                s.add(DiscordAccount(user_id=int(member.id), user_name=member.name, wallet=100, bank=0))
        s.commit()


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


@client.command(aliases=['balance'])
async def bal(ctx, *, member: discord.Member = None):
    account = None
    if member:
        account = s.query(DiscordAccount).filter(DiscordAccount.user_id == int(member.id))
    else:
        account = s.query(DiscordAccount).filter(DiscordAccount.user_id == int(ctx.message.author.id))
    if account:
        l = ["Cash: %d" % account.wallet, "Bank: %d" % account.bank, "Total: %d" % account.wallet + account.bank]

        embed = discord.Embed(title="{}'s balance".format(member.name),
                              description="{}".format('\n'.join(l)))
        await ctx.channel.send(embed=embed)


@client.command()
async def beg(ctx):
    a = randint(1, 1000)
    if a < 500:
        await ctx.channel.send("Nobody gave you any coins.")
    else:
        money = randint(50, 300)
        await ctx.channel.send("Someone gave %s %d coins! Yay!" % (ctx.message.author, money))
        account = s.query(DiscordAccount).filter(DiscordAccount.user_id == int(ctx.message.author.id))
        account.wallet += money
        s.update(account)
        s.commit()

client.run(TOKEN)
