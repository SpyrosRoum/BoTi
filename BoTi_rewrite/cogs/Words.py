import discord
from discord.ext import commands

import aiohttp


def clear_text(text):
    if "<b>" in text:
        text = text.replace("<b>", "**")
        return text.replace("</b>", "**")
    else:
        return text


def get_value(version, data):
    if version < len(data)-1:
        return f"**Definition**: {clear_text(data[version]['definition'])} \n\n **Example:** {clear_text(data[version]['example'])} \n\n\n _ _"
    else:
        return f"**Definition**: {clear_text(data[version]['definition'])} \n \n **Example:** {clear_text(data[version]['example'])}"


class Words:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def define(self, ctx, *, word):
        '''`!define <word>`\nThe definition of a word'''
        if len(word.split()) > 1:
            return await ctx.send("One words at a time please")

        async with aiohttp.ClientSession() as session:
            response = await session.get(f"https://owlbot.info/api/v2/dictionary/{word.lower()}")
            data = await response.json()

        embed = discord.Embed(title=f"Word: ``{word}``")

        for version in range(0, len(data)):
            embed.add_field(name=data[version]['type'],
                            value=get_value(version, data), inline=False)

        embed.set_footer(text="Powered by owlbot dictionary")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Words(bot))
