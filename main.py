import os
import discord
from discord.ext import commands
import tracemalloc
import asyncio

class Principal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

prefixo = os.getenv('PREFIXO', ',b')
testing = False

client = commands.Bot(prefixo, intents=discord.Intents.all())
client.remove_command('help')


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'): 
            tracemalloc.start()
            await client.load_extension(f'cogs.{filename[:-3]}')
            

async def main():
    await load_cogs()

if __name__ == "__main__":
    # aumenta o limite de eventos para lidar com mais conexões
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # inicia o loop de eventos
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


try:
    with open("verde/token.txt", "r") as f:
        token = f.read().strip()
except FileNotFoundError:
    print("Arquivo com o token não encontrado.")
    token = ""

@client.command(name='reload', help='Recarrega o módulo específico mesmo comigo funcionando', aliases=['recarregar'])
async def reload(ctx, extension=None):
    if extension:
        await client.reload_extension(f'cogs.{extension}')
        await ctx.send(f'Cog {extension} foi recarregado.')
    else:
        for cog in client.cogs.copy():
            client.unload_extension(f'cogs.{cog}')
        load_cogs()
        await ctx.send('Todas as cogs foram recarregadas.')

@client.event
async def on_ready():
    print("Bot is ready!")
    #tipos de activity: playing, watching, listening ou streaming.
    #tipos de status: online, offline, idle ou dnd (do not disturb)
    
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{prefixo}r 1d6"), status=discord.Status.dnd)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"O comando `{ctx.invoked_with}` não existe. Digite `{prefixo}help` para ver a lista de comandos disponíveis.")

client.run(token)