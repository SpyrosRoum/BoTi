import discord
from discord.ext import commands

import json

class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid arguments")
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You don't have the required permissions to run this command.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Don't be in a hurry, try again in {error.retry_after}")

        raise error



def setup(bot):
    bot.add_cog(Events(bot))



# chat filter
# if any(word in message.content.upper() for word in chat_filter) and message.author.id not in bypass_list:
#     # delete and send
