import discord
from discord.ext import commands

import asyncio

import time
import random


class Misc:
    def __init__(self, bot):
        self.bot = bot

    # Poll
    @commands.command()
    async def poll(sel, ctx, *, cont):
        '''`!poll <content>`\nCreate a poll'''
        await ctx.message.delete()
        msg = await ctx.send(f"poll: {cont}")
        await msg.add_reaction('👎')
        await msg.add_reaction('👍')
        await msg.add_reaction('🤷')
    # -------------

    # Send server names
    @commands.command()
    async def servers(self, ctx):
        '''`!servers`\nAll the servers that the bot is in'''
        # names = []
        # for guild in self.bot.guilds:
        #     names.append(guild.name)
        await ctx.send(" ,".join([s.name for s in self.bot.guilds]))
    # -------------

    # send dm
    @commands.command(pass_context=True)
    async def dmsay(self, ctx, user: discord.Member, *, cont):
        '''`!dmsay <@user> <message>`\nAnnoy people in dms'''
        await user.send(f"{ctx.message.author} said: {cont}")
        await ctx.message.delete()
    # -------------

    # Reminder command

    def get_time(self, sec, type):
        return {'sec': sec,
                'min': sec*60,
                'hours': sec*3600}.get(type, "The suported types are: 'sec', 'min' and 'hours'")

    @commands.command(pass_context=True)
    async def remind(self, ctx, sec: int, type, *, reminder=None):
        '''`!remind <num> <time (sec/min/hours)> <reason>`\nSet a reminder'''
        time = self.get_time(sec, type)
        if isinstance(time, int):
            await ctx.send(f"Reminder set for {sec} {type}. [{reminder}]")
            await asyncio.sleep(time)
            await ctx.send(f"Time's up {ctx.message.author.mention} [{reminder}]")
        else:
            await ctx.send(time)
    # -------------

    # Change nickname
    @commands.command(pass_context=True)
    async def nickname(self, ctx, *, new_nickname=None):
        '''`!nickname <new nickname>`\nChange your nickname (leave blank to remove your nickname)'''
        await ctx.message.author.edit(nick=new_nickname)
    # -------------

    @commands.command()
    async def choose(self, ctx, *, options):
        '''`!choose <option 1>, <option 2>, .., <option N>`\nChoose randomly from some options'''
        options = options.split(',')

        choice = random.choice(options)
        await ctx.send(choice)

    @commands.command()
    async def echo(self, ctx, *, message: commands.clean_content):
        await ctx.send(message)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {int(self.bot.latency * 1000)} ms")


def setup(bot):
    bot.add_cog(Misc(bot))
