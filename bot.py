import os 
import requests 
import aiohttp
from discord.ext import commands, tasks
import discord 
import time
from discord import Interaction
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord import app_commands
from Functions import get_rank, get_summoner_id, get_flex_rank, get_level, get_patch_number, get_pfp_id

load_dotenv()
TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
GUILD_ID = int(os.getenv('GUILD_TOKEN'))
CHANNEL_ID = int(os.getenv('CHANNEL_TOKEN'))
API_KEY = os.getenv('API_KEY')

intents=discord.Intents.default()
intents.members = True
intents.message_content = True
# client = discord.Client(intents=intents)
client = discord.Client(intents=intents)
# bot = commands.Bot(command_prefix='$', intents=intents)
tree = discord.app_commands.CommandTree(client)




@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    
    guild = discord.utils.get(client.guilds, name=SERVER)
    # summoner_id = get_summoner_id("Noor")
    # get_profile(summoner_id)
    await tree.sync(guild=discord.Object(id=guild.id))
    print("Ready!")
    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Server Members:\n - {members}')



@tree.command(name = "rank", description = "Grab your League of Legends rank in solo queue", guild=discord.Object(id=GUILD_ID))
async def rank(interaction: discord.Interaction, arg: str):
    value = get_summoner_id(arg)
    store = get_rank(value)
    embed = discord.Embed(
    colour = discord.Colour.dark_green(),
    title= "Solo Queue Rank",
    description= "Account holder's current rank in league of legends solo queue."
    )
    
    embed.add_field(name="Account: " + arg, value="Rank: " + store, inline=False)

    
    await interaction.response.send_message(embed=embed)


@tree.command(name = "flexrank", description = "Grab your League of Legends rank in flex queue", guild=discord.Object(id=GUILD_ID))
async def flexrank(interaction: discord.Interaction, arg: str):
    value = get_summoner_id(arg)
    store = get_flex_rank(value)
    await interaction.response.send_message("Account:" + " " + arg +  "\n" + "Rank:" + " "  + store)

@tree.command(name = "level", description = "Check your Level", guild=discord.Object(id=GUILD_ID))
async def level(interaction: discord.Interaction, arg: str):
    value = get_level(arg)
    
    await interaction.response.send_message("Account:" + " " + arg +  "\n" + "Level:" + " "  + str(value))



@tree.command(name = "profile", description = "Check Users Profile", guild=discord.Object(id=GUILD_ID))
async def profile(interaction: discord.Interaction, arg: str):
    name = arg
    summonerid = get_summoner_id(arg)
    solorank = get_rank(summonerid)
    flexrank = get_flex_rank(summonerid)
    level = get_level(arg)
    value = get_patch_number()
    pfp_id = get_pfp_id(arg)
    url = "https://ddragon.leagueoflegends.com/cdn/" +str(value)  + "/img/profileicon/" + str(pfp_id) + ".png"
    print(url)
    embed = discord.Embed(title= "User Profile", colour=discord.Colour.random())
    embed.set_author(name=f"{name}")
    embed.add_field(name="Level: ", value= level, inline=True)
    embed.add_field(name="Solo Queue Rank: ", value= solorank, inline=False)
    embed.add_field(name="Flex Queue Rank: ", value= flexrank, inline=False)
    embed.set_thumbnail(url=url)
    await interaction.response.send_message(embed=embed)
    
    

 
client.run(TOKEN)

