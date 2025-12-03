import discord
import random
from bot_logic import *
# A variável intents armazena as permissões do bot
intents = discord.Intents.default()
# Ativar a permissão para ler o conteúdo das mensagens
intents.message_content = True
# Criar um bot e passar as permissões
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f'Fizemos login como {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$Qual o seu nome ?'):
        await message.channel.send("Meu nome é chatbot!")
    elif message.content.startswith('$bye'):
        await message.channel.send("\U0001f642")
    elif message.content.startswith('$gerar senha'):
        senha = gen_pass(10)
        await message.channel.send(f"Sua senha é: {senha}")
    elif message.content.startswith('$girar moeda'):
        resultado = flip_coin()
        await message.channel.send(f"O resultado é: {resultado}")
    elif message.content.startswith('$rolar dado'):
        resultado = roll_dice(sides=6)
        await message.channel.send(f"O resultado do dado é: {resultado}")
    elif message.content.startswith('$piada'):
        piada = gen_joke()
        await message.channel.send(piada)
    elif message.content.startswith('$gerar palavra'):
        palavra = gen_word()
        await message.channel.send(f"Sua palavra é: {palavra}")
    elif message.content.startswith('$gerar número'):
        numero = gen_number(1, 100)
        await message.channel.send(f"Seu número é: {numero}")
    elif message.content.startswith('$citação'):
        citacao = gen_quote()
    elif message.content.startswith('$fatos'):
        fatos = gen_fact()
        fato = random.choice(fatos)
        await message.channel.send(fato)
    elif message.content.startswith('$ppt'):
        ppt = rps()
        await message.channel.send(ppt)
    else:
        await message.channel.send(message.content)

client.run('MTQ0MDgyNTY4NTI5OTAzNjE2MA.GjzT2y.mBix7Oswykrcj7PC0lIFtRUce2MSFc6h7PKliA')