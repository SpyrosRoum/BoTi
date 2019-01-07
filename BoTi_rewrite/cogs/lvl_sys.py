import discord
from discord.ext import commands

import json
import asyncio

# formula to determin if level up: round((4 * (cur_lvl ** 3)) / 5)
class lvl_sys:
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.savelevels())

        with open(r"D:\MYPC_HDD\Python_projects\BoTi_rewrite\cogs\levels.json", "r") as f:
            self.levels = json.load(f)

    def lvl_up(self, member):
        cur_xp = self.levels[str(member.id)]["xp"]
        cur_lvl = self.levels[str(member.id)]["level"]

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            self.levels[str(member.id)]["level"] += 1
            return True
        return False



    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user_name = message.author
        msg = message.content
        auth_id = str(message.author.id)

        # Level system
        if str(auth_id) not in self.levels:
            self.levels[auth_id] = {}
            self.levels[auth_id]["level"] = 1
            self.levels[auth_id]["xp"] = 0

        self.levels[auth_id]["xp"] += 2

        if self.lvl_up(message.author):
            user_id = str(message.author.id)
            await message.channel.send(f"{message.author.mention} is now level {self.levels[user_id]['level']}")




    async def savelevels(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open("D:\\MYPC_HDD\\Python_projects\\BoTi_rewrite\\cogs\\levels.json", "w") as f:
                json.dump(self.levels, f, indent=4)
            await asyncio.sleep(5)



    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member

        embed = discord.Embed(color=ctx.me.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Level - {member}", icon_url=self.bot.user.avatar_url)

        embed.add_field(name="Level", value=self.levels[str(ctx.author.id)]["level"])
        embed.add_field(name="XP", value=self.levels[str(ctx.author.id)]["xp"])

        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(lvl_sys(bot))
