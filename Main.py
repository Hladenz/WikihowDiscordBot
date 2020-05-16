import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix=("--"))

def GetSites(Seasrch):
    request= requests.get(f"https://www.wikihow.com/wikiHowTo?search={Seasrch}")
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    links =[]
    for link in soup.findAll('a', class_= "result_link", href=True):
        links.append(link['href'] + "\n")

    return links

@bot.command(pass_context=True,name="wikihow")
async def wikihow(ctx,*args):
    Searchterm = " ".join(args)
    embed = discord.Embed(title="Wikihow returns", description=f"{' '.join(GetSites(Searchterm))}", color=0x00ffff)
    await ctx.send(embed=embed)


bot.run("")