# for nothing: "\u200b"
import discord
from discord.ext import commands

# from aioprint import print as aiprint

bot = commands.Bot(commands.when_mentioned_or("!"))
bot.remove_command('help')

TOKEN = open('TOKEN.txt', 'r').read()

extentions = ['cogs.Mod', 'cogs.Calculator',
              'cogs.Custom_Images', 'cogs.Misc',
              'cogs.Words', 'cogs.Art', 'cogs.Movies', 'cogs.Music',
              'cogs.Trivial', 'cogs.Help', 'cogs.Events']


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    # print(bot.user.id)
    print('------')
    # print(len(bot.guilds))
    # x = [command for command in bot.commands]
    # print([command.cog_name for command in x])
    # print([command.name for command in bot.commands])

@bot.command()
@commands.is_owner()
async def tet(ctx):
    guild = ctx.guild
    await ctx.send(guild.by_category())
    print(guild.by_category())


@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, module):
    """Loads a module."""
    try:
        bot.load_extension('cogs.'+module)
        print(f"Loaded {module}")
    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send(f'{type(e).__name__}: {e}')


@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, module):
    """Unloads a module."""
    try:
        bot.unload_extension('cogs.'+module)
        print(f"Unloaded {module}")

    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send(f'{type(e).__name__}: {e}')



@bot.command(name='reload', hidden=True)
@commands.is_owner()
async def _reload(ctx, *, module : str):
    """Reloads a module."""
    try:
        bot.unload_extension('cogs.'+module)
        bot.load_extension('cogs.'+module)
        await ctx.send('\N{OK HAND SIGN}')

    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send(f'{type(e).__name__}: {e}')


if __name__ == '__main__':
    for extension in extentions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'{extension} can not be loaded:')
            raise e

    bot.run(TOKEN)
