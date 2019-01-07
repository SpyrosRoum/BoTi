import discord
from discord.ext import commands

import aiohttp

KEY = "find your own :)"


class Movies:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, *, movie):
        '''``!search <movie>``\nSearches for movies based on the name you provided'''

        async with aiohttp.ClientSession() as session:
            response = await session.get(f"http://www.omdbapi.com/?apikey={KEY}&s={movie}&type=movie")
            data = await response.json()
        # print(data)
        if data['Response'] == 'False':
            await ctx.send(f"Something went wrong.. [{data['Error']}]")
        else:
            Titles = []
            Years = []
            IMDbIDs = []

            for item in data["Search"]:
                Titles.append(item["Title"])
                Years.append(item["Year"])
                IMDbIDs.append(item["imdbID"])

            # print(Titles, '\n', Years, '\n', IMDbIDs)

            embed = discord.Embed(title="movies")
            for i in range(0, len(Titles)):
                embed.add_field(name=f"{Titles[i]}",  value=f"IMDb ID = {IMDbIDs[i]}", inline=True)
                embed.add_field(name=f"{Years[i]}", value="\u200b", inline=True)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.set_footer(text="Powered by the Open Movie DataBase")
            await ctx.send(embed=embed)

    @commands.command()
    async def Mfind(self, ctx, type, *, movie):
        '''``!search <type (i or t)> <movie>``\nSearches for the movie with the imbd id or title you provided'''

        id_find = {"i": movie}
        title_search = {"t": movie}

        if type == 'i':
            parameters = id_find
        elif type == 't':
            parameters = title_search

        async with aiohttp.ClientSession() as session:
            response = await session.get(f"http://www.omdbapi.com/?apikey={KEY}", params=parameters)
            data = await response.json()

        # print(data)
        if data['Response'] == 'True':
            embed = discord.Embed(title=data['Title'],
                                  description=f"Aired: {data['Released']} || Screentime: {data['Runtime']}")

            embed.set_image(url=data["Poster"])

            embed.add_field(name=f"{data['Plot']}", value="\u200b", inline=False)
            embed.add_field(name="Genre: ", value=f"{data['Genre']}", inline=False)

            embed.add_field(
                name="\u200b", value=f"Metascore:  **{data['Metascore']}**/100", inline=True)
            embed.add_field(
                name="\u200b", value=f"IMDb Rating:  **{data['imdbRating']}**/10", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.add_field(name="Director:", value=f"{data['Director']}", inline=True)
            embed.add_field(name="Actors:", value=f"{data['Actors']}")
            embed.set_footer(text=f"IMDB ID = {data['imdbID']}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{data['Error']}")



def setup(bot):
    bot.add_cog(Movies(bot))
