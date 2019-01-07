import discord
from discord.ext import commands

import asyncio
import json


class counter:
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.saveuses())

        with open(r"D:\MYPC_HDD\Python_projects\BoTi_rewrite\cogs\uses.json", 'r') as f:
            self.uses = json.load(f)

    async def saveuses(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"D:\MYPC_HDD\Python_projects\BoTi_rewrite\cogs\uses.json", 'w') as f:
                json.dump(self.uses, f, indent=4)
            await asyncio.sleep(5)

    async def on_message(self, message):
        if "hehe" in message.content.lower():
            user_id = str(message.author.id)

            if user_id not in self.uses:
                self.uses[user_id] = 0

            self.uses[user_id] += 1
            await message.channel.send(self.uses[user_id])

    @commands.command()
    async def test(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in self.uses:
            self.uses[user_id] = 0

        self.uses[user_id] += 1

        await ctx.send(self.uses[user_id])


def setup(bot):
        bot.add_cog(counter(bot))
