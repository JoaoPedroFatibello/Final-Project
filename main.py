import requests
import discord
import asyncio
from discord.ext import commands


# URL da NASA POWER Projection API
url = "https://power.larc.nasa.gov/api/projection/monthly/point"


# Configuração do bot Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Função que consulta a NASA POWER
def get_climate_data(longitude, latitude):

    params = {
        "longitude": longitude,
        "latitude": latitude,
        "community": "AG",
        "parameters": "T2M,T2M_MAX",
        "scenario": "ssp370",
        "model": "ensemble",
        "start": "203001",
        "end": "203112",
        "format": "JSON",
        "time-standard": "UTC"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# Comando do Discord
@bot.command()
async def climate_changes(ctx, user_longitude, user_latitude):

    # Converte as coordenadas para números
    try:
        longitude = float(user_longitude)
        latitude = float(user_latitude)

    except ValueError:
        await ctx.send(
            "❌ Informe a longitude e latitude corretamente."
        )
        return

    # Verifica se as coordenadas são válidas
    if not -180 <= longitude <= 180:
        await ctx.send("❌ Longitude inválida.")
        return

    if not -59.875 <= latitude <= 89.875:
        await ctx.send(
            "❌ Latitude fora da cobertura da API."
        )
        return

    await ctx.send(
        "🌎 Consultando projeções climáticas da NASA..."
    )

    try:
        # Executa a requisição sem bloquear o Discord
        dados = await asyncio.to_thread(
            get_climate_data,
            longitude,
            latitude
        )

        # Acessa os dados retornados pela API
        parametros = dados["properties"]["parameter"]

        temperatura_media = parametros["T2M"]["ssp370"]
        temperatura_maxima = parametros["T2M_MAX"]["ssp370"]

        # Separa os dados por ano
        anos = {
            "2030": [],
            "2031": []
        }

        for data, valor in temperatura_media.items():

            ano = data[:4]

            if ano in anos and valor != -999:
                anos[ano].append(valor)

        # Calcula a média anual
        media_2030 = sum(anos["2030"]) / len(anos["2030"])
        media_2031 = sum(anos["2031"]) / len(anos["2031"])

        # Calcula a diferença entre os anos
        diferenca = media_2031 - media_2030

        # Monta a mensagem
        mensagem = (
            f"🌡️ **Projeção de mudanças climáticas**\n\n"
            f"📍 Latitude: `{latitude}`\n"
            f"📍 Longitude: `{longitude}`\n"
            f"📊 Cenário: `SSP3-7.0`\n\n"
            f"**Temperatura média projetada:**\n"
            f"• 2030: `{media_2030:.2f} °C`\n"
            f"• 2031: `{media_2031:.2f} °C`\n\n"
            f"**Diferença entre os anos:**\n"
            f"`{diferenca:+.2f} °C`\n\n"
            f"Dados: NASA POWER"
        )

        await ctx.send(mensagem)

    except requests.exceptions.RequestException:
        await ctx.send(
            "❌ Não foi possível acessar a NASA POWER."
        )

    except (KeyError, ZeroDivisionError):
        await ctx.send(
            "❌ Não foi possível interpretar os dados "
            "retornados pela API."
        )


# Inicia o bot
bot.run("SEU_TOKEN_DO_DISCORD")
