from discord.ext import commands

from art import text2art


class Art:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def write(self, ctx, *, cont):
        '''`!write <text>`\nConverts words to art'''
        await ctx.message.delete()
        await ctx.send(f"```\n{text2art(cont, 'random')}```")


def setup(bot):
    bot.add_cog(Art(bot))
