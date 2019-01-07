import discord
from discord.ext import commands

import time


class Help:
    def __init__(self, bot):
        self.bot = bot


    def Nembed(self, page: int, pages, cogs, cogsD, time):
        embed = discord.Embed(timestamp=time)
        embed.set_author(name=f"Help - {cogs[page]} - {len(cogsD[cogs[page]])} commands", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Page {page+1}/{pages}")

        for command in cogsD[cogs[page]]:
            embed.add_field(name=command.name, value=command.help, inline=False)

        return embed


    @commands.command(aliases=["h"])
    @commands.cooldown(1, 120.0, type=commands.BucketType.channel)
    async def help(self, ctx):
        '''`!help`\nDisplay this message'''
        commands = [command for command in self.bot.commands if command.cog_name is not None]
        # Scogs = set([command.cog_name for command in commands])
        cogs = [cog for cog in set([command.cog_name for command in commands])]

        cogsD = {}
        for cog in cogs:
            cogsD[cog] = []
            for command in commands:
                if command.cog_name == cog:
                    cogsD[cog].append(command)

        pages = len(cogsD)
        page = 0

        embed = self.Nembed(page, pages, cogs, cogsD, ctx.message.created_at)
        msg = await ctx.send(embed=embed)

        await msg.add_reaction('⬅')
        await msg.add_reaction('➡')
        await msg.add_reaction("❌")

        def check(reaction, user):
            e = str(reaction.emoji)
            return e.startswith(('⬅', '➡', "❌")) and user != self.bot.user


        t_end = time.time() + 120
        while time.time() < t_end:

            res, user = await self.bot.wait_for('reaction_add', check=check)

            if str(res.emoji) == "➡":
                page += 1

                if page == pages:
                    page = pages - 1

                await msg.edit(embed=self.Nembed(page, pages, cogs, cogsD, ctx.message.created_at))
                await msg.remove_reaction('➡', user)

            elif str(res.emoji) == "⬅":
                page -= 1
                if page < 0:
                    page = 0
                await msg.edit(embed=self.Nembed(page, pages, cogs, cogsD, ctx.message.created_at))
                await msg.remove_reaction('⬅', user)

            elif str(res.emoji) == "❌":
                ctx.command.reset_cooldown(ctx)
                await msg.remove_reaction("❌", user)
                break

        await msg.remove_reaction('⬅', self.bot.user)
        await msg.remove_reaction('➡', self.bot.user)
        await msg.remove_reaction("❌", self.bot.user)
        await msg.edit(content="Type `!help` or `!h`", embed=None)


def setup(bot):
    bot.add_cog(Help(bot))
