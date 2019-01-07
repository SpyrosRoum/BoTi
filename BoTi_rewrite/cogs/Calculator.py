import discord
from discord.ext import commands

from numexpr import evaluate


def clear_data(data):
    if "`" in data:
        data = data.strip("`")

    if "^" in data:
        data = data.replace("^", "**")

    if "x" in data.lower():
        data = data.lower().replace("x", "*")

    return data


class Calculator:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, ctx, *, data):
        data = clear_data(data)

        try:
            answer = evaluate(data)

            embed = discord.Embed(title="The answer is:")
            embed.add_field(name=f"```{answer}```", value="_ _")

            await ctx.send(embed=embed)
        except SyntaxError:
            await self.bot.send("Invalid syntax.")
        except Exception as e:
            await ctx.send(f"Oops, something went wrong [{e}]")


def setup(bot):
    bot.add_cog(Calculator(bot))
