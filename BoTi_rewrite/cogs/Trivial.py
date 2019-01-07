import discord
from discord.ext import commands
import asyncio

import aiohttp
import html

import time
import itertools


async def play():
    question_answer = {}

    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://opentdb.com/api.php?amount=1")

        try:
            data = await response.json()
        except Exception:
            return "error"
    question = html.unescape(data['results'][0]['question'])
    correct_answer = html.unescape(data['results'][0]['correct_answer']).split("\u200b")
    wrong_answers = html.unescape(data['results'][0]['incorrect_answers'])
    answers = set(wrong_answers + correct_answer)
    question_answer.update({question: [correct_answer, answers]})

    return question_answer


class Trivial:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def tplay(self, ctx, rounds: int):
        score = {}

        if rounds > 5:
            msg = await ctx.send("This may take a while")
        else:
            msg = await ctx.send("On it")

        cur_round = 1
        while cur_round <= rounds:

            correct_users = []
            users_said = {}

            QandA = await play()

            if QandA == "error":
                return ctx.send("Something went wrong")

            question = list(QandA.keys())[0].strip("''")
            correct_answer = QandA[question][0][0]
            answers = list(QandA[question][1])

            # Creating the Embed with the question/answers
            embed = discord.Embed(title=question)
            for answer in answers:
                embed.add_field(
                    name="\u200b", value=f"{answers.index(answer) + 1}) {answer}", inline=False)
            embed.set_footer(text="The correct answer will be revealed in 20 seconds")
            # ----------

            if cur_round == 1:
                await msg.edit(content=None, embed=embed)
            else:
                await ctx.send(embed=embed)

            t_end = time.time() + 20
            while time.time() < t_end:

                def check(msg):
                    try:
                        numb = int(msg.content)
                    except Exception:
                        numb = 10

                    return numb in range(1, len(answers)+1) and msg.channel == ctx.channel

                try:
                    choise = await self.bot.wait_for('message', timeout=1.0, check=check)
                except asyncio.TimeoutError:
                    choise = None

                if choise is not None and str(choise.author.id) not in users_said:
                    users_said.update({str(choise.author.id): choise.content})
                    name = choise.author.name

            # await ctx.send(f"answers: {users_said}")

            for user in users_said:
                answer = users_said[user]
                answer = answers[int(answer)-1]

                if user not in score:
                    score[user] = 0
                if answer == correct_answer:
                    correct_users.append(name)
                    score[user] += 50

            if len(correct_users) == 0:
                embed = discord.Embed(
                    title=f"The correct answer was: ``{correct_answer}`` and no one guessed it :(")
                await ctx.send(embed=embed)
                await asyncio.sleep(3)
            else:
                embed = discord.Embed(
                    title=f"The correct answer was: ``{correct_answer}`` and they found it:")
                for user in correct_users:
                    print(user)
                    embed.add_field(name=user, value="_ _")

                await ctx.send(embed=embed)
                await asyncio.sleep(3)

            cur_round += 1

        await asyncio.sleep(1)
        print(f"scores: {score}")
        winners = []
        couples = 0
        for x, y in itertools.combinations(score.values(), 2):
            if x == y:
                couples += 1

        for couple in range(0, couples+1):
            winner = max(score, key=(lambda key: score[key]))
            winners.append(winner)
            del(score[winner])

        print(f"List of winners' ids: {winners}")

        names = []
        for id in winners:
            name = await self.bot.get_user_info(id)
            names.append(name)

        print(f"List of members: {names}")

        if len(names) > 1:
            t = "The winner is: "
        else:
            t = "The winners are: "

        embed = discord.Embed(title=t)
        for winner in names:
            embed.add_field(name=f"**{winner}**", value="_ _", inline=False)

        embed.set_footer(text="Powered by Open Trivia DataBase")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Trivial(bot))
