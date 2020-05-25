import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import os
import json

bot = commands.Bot(command_prefix=("--"))

def GetDefo(word):
    req = requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
    if req.status_code == 200:
        info = json.loads(req.text)
        if req.text == '{"list":[]}':
            return None,None


        Defo = info.get("list")[0]["definition"]
        Example = info["list"][0]["example"]
        return Defo,Example

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

@bot.event
async def on_message(message):

    if message.author.id != bot.user.id:
        if "im" in message.content.lower():
            words = message.content.lower().split(" ")
            word = words[words.index("im") +1]
            await message.channel.send(f"Hello {word}, Im Dad!")
        elif "i'm" in message.content.lower():
            words = message.content.lower().split(" ")
            word = words[words.index("i'm") +1]
            await message.channel.send(f"Hello {word}, Im Dad!")

@bot.command(pass_context=True,name="MrUrban")
async def MrUrban(ctx):
    messages = ctx.message.content.split(" ")
    if len(messages) < 2:
        await ctx.send(f"Please Provide a word to search")
    Defo, Example = GetDefo(messages[1])
    if Defo == None:
        await ctx.send(f"Can't Find a Definition For that")
    else:
        await ctx.send(f"**Definition:**{Defo} \n **Example:**{Example}")

@bot.command(pass_context=True, name="credit")
async def Credit(ctx):
    embed = discord.Embed(title="Bot Created By Hladenz", url="https://www.fiverr.com/hladenz",
                          description="This Bot Was Created By Hladenz On Fiverr *not really*", color=0x00ff00)
    embed.set_thumbnail(
        url="https://fiverr-res.cloudinary.com/t_profile_original,q_auto,f_auto/attachments/profile/photo/1fdcc4ab070147dd6f8b31246f672514-1588777785551/73c13f35-b2c1-42e5-a5f1-652cd437eeeb.jpg")
    await ctx.channel.send(embed=embed)


bot.run(os.getenv('BOT_TOKEN'))