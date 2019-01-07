import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
# import asyncio


class Custom_Images:
    def __init__(self, bot):
        self.bot = bot

    async def create_image(self, name):
        im = Image.open(r"D:\MYPC_HDD\Python_projects\BoTi_rewrite\Rip.png")
        base = im.convert("RGBA")

        txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype(r"D:\MYPC_HDD\Python_projects\BoTi_rewrite\Scheherazade-Regular.ttf", 40)

        d = ImageDraw.Draw(base)
        d.text((80, 175), text=name, font=fnt, fill=(0, 0, 0, 255))

        out = Image.alpha_composite(base, txt)

        out.save(r"D:\MYPC_HDD\Python_projects\BoTi_rewrite\final.png")


    @commands.command(pass_context=True)
    async def rip(self, ctx, member: discord.Member = None):
        '''``!rip (@member)``\nSends a tombstone with the nickname of the member, it's you by default'''
        member = ctx.author if not member else member

        await self.create_image(member.display_name)
        await ctx.send(file=discord.File(r"D:\MYPC_HDD\Python_projects\BoTi_rewrite\final.png"))


def setup(bot):
    bot.add_cog(Custom_Images(bot))
