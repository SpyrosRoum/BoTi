import discord
from discord.ext import commands

import time


def page0():  # You will have to create the embeds for the commands, I made 2 pages as an example
    page = discord.Embed()
    page.add_field(name="page0", value="value")
    return page


def page1():
    page = discord.Embed()
    page.add_field(name="page1", value="value")
    return page


pages = [page0(), page1()]  # List of functions that return the embeds, add as many as you need


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        page = 0  # Sets the page to the first one

        msg = await ctx.send(embed=pages[0])  # Sends the first page
        await msg.add_reaction('⬅')  # Reacts with the two emojis
        await msg.add_reaction('➡')

        def check(reaction, user):  # Checks if the emoji is one of the two and the user is not the bot
            e = str(reaction.emoji)
            return e.startswith(('⬅', '➡')) and user != self.bot.user

        t_end = time.time() + 120  # Sets the timer, currently it's two minutes
        while time.time() < t_end:
            # waits for the reaction
            res, user = await self.bot.wait_for('reaction_add', check=check)

            if str(res.emoji) == "➡":
                page += 1

                if page == len(pages):
                    page = len(pages) - 1

                await msg.edit(embed=pages[page])
                await msg.remove_reaction('➡', user)

            elif str(res.emoji) == "⬅":
                page -= 1
                if page < 0:
                    page = 0
                await msg.edit(embed=pages[page])
                await msg.remove_reaction('⬅', user)

        await msg.remove_reaction('⬅', self.bot.user)
        await msg.remove_reaction('➡', self.bot.user)
        await msg.edit(content="Type ``!help`` or ``!h``", embed=None)


def setup(bot):
    bot.add_cog(Help(bot))

# One thing to note is that the while loop won't break when the timer ends since it get's stuck at
# the wait_for, thus you need to react one last time. That can be avoided with a timeout I think
# but I didn't do it like that to avoid the case that the user might react but the bot isn't
# waiting for it
