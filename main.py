import requests
import discord
from discord.ext import commands


# URL oficial da API da NASA POWER
url = "https://nasa.gov"

# Parâmetros para buscar a projeção de temperatura
params = {
    "longitude": user_longitude,
    "latitude": user_latitude,
    "community": "ag",
    "parameters": "T2M_MAX",
    "scenario": "ssp585",
    "model": "ensemble",
    "temporal": "monthly",
    "start": "2030",
    "end": "2031",
    "format": "json"
}

response = requests.get(url, params=params)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!" , intents=intents) 
