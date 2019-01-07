import discord
from discord.ext import commands

import random
import asyncio

import aiohttp
import aiofiles

import os


def is_bot_or_server_owner(ctx):
    return ctx.bot.owner_id == ctx.author.id or ctx.guild.owner_id == ctx.author.id


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason="No reason"):
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user} banned by {ctx.author.mention}. [{reason}]")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason"):
        await user.kick(reason=reason)
        await ctx.send(f"{user.mention} kicked by {ctx.author.mention}. [{reason}]")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100):
        channel = ctx.channel
        await channel.purge(limit=int(amount)+1)

        await ctx.send(f"{amount} messages deleted")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def name(self, ctx, user: discord.Member, *, new_name=None):
        await user.edit(nick=new_name)

    # @commands.command()
    # @commands.check(is_bot_or_server_owner)
    # async def create(self, ctx):
    #     guild = ctx.guild
    #     if f"{guild.name} - Snap" in [guild.name for guild in self.bot.guilds]:
    #         return await ctx.send("Server already exist")
    #
    #     await self.bot.create_guild(name=f"{guild.name} - Snap", region=guild.region)
    #     await ctx.send(f"Guild created, now do `{ctx.prefix}snapshot`")

    async def download_img(self, img_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(img_url) as resp:
                img  = await resp.read()

        return img

    async def make_channel(self, channel, new_guild: discord.Guild, new_category: discord.CategoryChannel = None):
        if isinstance(channel, discord.TextChannel):

            permissions = channel.overwrites
            if not permissions:
                if new_category is None:
                    new_channel = await new_guild.create_text_channel(name=channel.name)
                else:
                    new_channel = await new_guild.create_text_channel(name=channel.name, category=new_category)
            else:
                overwrites = {}
                for tu in permissions: # tu because it's a tuple, first item is the role and second is the PermissionOverwrite obj
                    role_name = tu[0].name
                    role = discord.utils.get(new_guild.roles, name=role_name)
                    perms = tu[1]

                    overwrites[role] = perms

                if new_category is None:
                    new_channel = await new_guild.create_text_channel(name=channel.name, overwrites=overwrites)
                else:
                    new_channel = await new_guild.create_text_channel(name=channel.name, category=new_category, overwrites=overwrites)

            nsfw = False
            if channel.is_nsfw(): nsfw = True
            await new_channel.edit(topic=channel.topic, slowmode_delay=channel.slowmode_delay, nsfw=nsfw)

            # Get's channel history
            f = await aiofiles.open(f"{channel.name}_history.txt", "w+", encoding="utf-8")
            async for message in channel.history(reverse=True, limit=300):
                user = message.author
                content = message.content
                when = message.created_at

                await f.write(f"\n{user} said: '{content}'\nAt: {when}\n")
            await f.close()

            await new_channel.send(file=discord.File(f"{channel.name}_history.txt"))
            os.remove(f"{channel.name}_history.txt")

        else:
            if new_category is None:
                await new_guild.create_voice_channel(name=channel.name)
            else:
                await new_guild.create_voice_channel(name=channel.name, category=new_category)


    @commands.command()
    @commands.check(is_bot_or_server_owner)
    async def snapshot(self, ctx):
        async with ctx.typing():
            msg = await ctx.send("This may take a while, I will let you know when it's done")
            await asyncio.sleep(1)
            guild = ctx.guild

            # Check if there already exist a guild named f"{guild.name} - Snap", if not create one else return
            if not f"{guild.name} - Snap" in [guild.name for guild in self.bot.guilds]:
                await self.bot.create_guild(name=f"{guild.name} - Snap", region=guild.region)
                await asyncio.sleep(1)
                new_guild = discord.utils.get(self.bot.guilds, name=f"{guild.name} - Snap")

                progress = f"New guild has been created\n------------"
                await msg.edit(content=progress)
            else:
                new_guild = discord.utils.get(self.bot.guilds, name=f"{guild.name} - Snap")
                progress = ""
                # return await msg.edit(content="It appears as there already is a backup of this server, please delete the backup and try again. If you think that something is wrong message `Spyros#1947`.")

            # Remove all the channels so new can be created
            for channel in new_guild.channels:
                await channel.delete()
                await asyncio.sleep(1)

            # Removes all the roles. This is probably useless
            if len(new_guild.roles) > 1:
                for role in new_guild.roles:
                    if role.name != "@everyone":
                        await role.delete()
                        await asyncio.sleep(1)

            # Create roles same as before
            for role in guild.roles:
                await new_guild.create_role(name = role.name, permissions = role.permissions, colour = role.color, hoist = role.hoist, mentionable = role.mentionable)
                await asyncio.sleep(1)

                progress = f"{progress}\n`{role.name}` role has been created"
                await msg.edit(content=progress)
            progress = f"{progress}\n------------"

            member = new_guild.me
            roles = [discord.utils.get(new_guild.roles, name=role.name) for role in guild.me.roles if role.name != "@everyone"]
            [await member.add_roles(role) for role in roles]

            # Creates the channels that are not in a category
            channels = [channel for channel in guild.text_channels if channel.category is None]
            for channel in guild.voice_channels:
                if channel.category is None:
                    channels.append(channel)

            for channel in channels:
                await self.make_channel(channel, new_guild)

            # Create all the categories with overwrites as before
            for category in guild.categories:
                permissions = category.overwrites

                if not permissions:
                    new_category = await new_guild.create_category_channel(name=category.name)
                else:
                    overwrites = {}
                    for tu in permissions: # tu because it's a tuple, first item is the role and second is the PermissionOverwrite obj
                        role_name = tu[0].name
                        role = discord.utils.get(new_guild.roles, name=role_name)
                        perms = tu[1]

                        overwrites[role] = perms

                    new_category = await new_guild.create_category_channel(name=category.name, overwrites=overwrites)


                # Create all the channels in the category with overwrites same as before
                for channel in category.channels:
                    await self.make_channel(channel, new_guild, new_category)
                    await asyncio.sleep(1)


                if category.is_nsfw(): await new_category.edit(nsfw=True)

                progress = f"{progress}\n`{category.name}` category is ready"
                await msg.edit(content=progress)


            # Setting the afk channel and timeout if necessary
            old_afk_channel = guild.afk_channel
            if old_afk_channel is not None:
                afk_chn_name = old_afk_channel.name
                new_afk_channel = discord.utils.get(new_guild.voice_channels, name=afk_chn_name)

                await new_guild.edit(afk_channel=new_afk_channel, afk_timeout=guild.afk_timeout)


            # Bans the old people in the new server
            bans = await guild.bans()
            if not bans:
                pass
            else:
                progress = f"{progress}\n------------"
                progress = f"{progress}\nBanning people"
                await msg.edit(content=progress)
                for ban in bans:
                    await new_guild.ban(ban.user, reason=ban.reason)


            chn = random.choice(new_guild.text_channels)
            inv = await chn.create_invite()


            # Transfer emojis
            emojis = guild.emojis
            if not emojis:
                pass
            else:
                progress = f"{progress}\n------------"
                progress = f"{progress}\nTransfering emojis"
                await msg.edit(content=progress)
                for emoji in emojis:
                    if emoji.animated:
                        continue

                    emoji_url = emoji.url
                    img = await self.download_img(emoji_url)

                    if len(emoji.roles) >= 1:
                        await new_guild.create_custom_emoji(name=emoji.name, image=img, roles=emoji.roles)
                    else:
                        await new_guild.create_custom_emoji(name=emoji.name, image=img)

                    await asyncio.sleep(1)

            # Making the old owner owner again and setting the icon for the server
            icon_url = guild.icon_url_as(format='jpeg', size=2048)
            if not icon_url:
                pass
            else:
                img = await self.download_img(icon_url)
                await new_guild.edit(icon=img)

            await ctx.send(f"{ctx.author.mention} the snapshot is completed. Here is a link for the server {inv.url}, please join for the process to be completed")

        member = await self.bot.wait_for("member_join", check=lambda mem: (mem.id == guild.owner_id) and (mem.guild.id == new_guild.id))


        await new_guild.edit(owner=member)

        await chn.send("Welcome. I have given you ownership and I hope everyhting is as it should. If there any any problems please message `Spyros#1947`")


    @commands.command()
    @commands.check(is_bot_or_server_owner)
    async def inv(self, ctx):
        guilds = [guild for guild in self.bot.guilds if guild.name == f"{ctx.guild.name} - Snap"]
        invs = []
        for guild in guilds:
            try:
                chn = random.choice(guild.text_channels)
            except IndexError:
                chn = await guild.create_text_channel(name="Oops")

            inv = await chn.create_invite()
            invs.append(inv.url)
        await ctx.send(invs)

    @commands.command()
    @commands.is_owner()
    async def dele(self, ctx):
        guild = ctx.guild
        await guild.delete()

    @commands.command()
    async def show_bans(self, ctx):
        bans = await ctx.guild.bans()

        users = [ban.user for ban in bans]

        await ctx.send(users)

def setup(bot):
    bot.add_cog(Mod(bot))
