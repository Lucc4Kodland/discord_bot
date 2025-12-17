import discord
from discord.ext import commands, tasks
import random
from datetime import datetime, time as dtime

# ======================
# COLOQUE SEU TOKEN AQUI
# ======================
TOKEN = "Seu_token_aqui"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

# ======================
# MENSAGENS AMBIENTAIS
# ======================
incentivos = [
    "Não jogue lixo na rua, use a lixeira!",
    "Não desperdice água, feche a torneira!",
    "Não deixe luz acesa à toa, apague sempre!",
    "Não use plástico descartável, leve algo reutilizável!",
    "Não queime lixo, recicle o que puder!",
    "Não jogue óleo no ralo, descarte no ponto certo!",
    "Não desperdice comida, aproveite bem!",
    "Não jogue pilhas no lixo comum, leve pra coleta!",
    "Não deixe sujeira na praia, leve seu lixo!",
    "Não use sacola plástica, leve ecobag!",
    "Não jogue papel no chão, recicle!",
    "Não compre coisas sem necessidade, reutilize!",
    "Não use aparelhos ligados sem motivo, desligue!",
    "Não polua rios, segure o lixo até achar lixeira!",
    "Não compre descartáveis, prefira duráveis!",
    "Não desperdice folhas, use frente e verso!",
    "Não derrube árvores, plante uma!",
    "Não deixe água correndo, economize!",
    "Não polua parques, cuide do espaço!",
    "Não ignore pequenos gestos, faça sua parte!"
]

# ======================
# CONFIGURAÇÕES PADRÃO
# ======================
periodo_inicio = dtime(8, 0)
periodo_fim = dtime(20, 0)
delay_horas = 1
canal_id = None

# ======================
# FUNÇÃO DE HORÁRIO
# ======================
def dentro_do_periodo():
    agora = datetime.now().time()
    return periodo_inicio <= agora <= periodo_fim

# ======================
# LOOP AUTOMÁTICO
# ======================
@tasks.loop(hours=1)
async def enviar_mensagem():
    if not canal_id:
        return

    if dentro_do_periodo():
        canal = bot.get_channel(canal_id)
        if canal:
            await canal.send(f"@everyone {random.choice(incentivos)}")

# ======================
# EVENTO
# ======================
@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

# ======================
# COMANDOS
# ======================

@bot.command()
@commands.has_permissions(administrator=True)
async def periodo(ctx, inicio: str, fim: str):
    """Define o horário de funcionamento do bot"""
    global periodo_inicio, periodo_fim
    periodo_inicio = datetime.strptime(inicio, "%H:%M").time()
    periodo_fim = datetime.strptime(fim, "%H:%M").time()
    await ctx.send(f"⏰ Período definido: **{inicio} até {fim}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def delay(ctx, horas: int):
    """Define o intervalo entre mensagens"""
    global delay_horas
    delay_horas = horas
    enviar_mensagem.change_interval(hours=delay_horas)
    await ctx.send(f"⏳ Delay definido para **{horas} hora(s)**")

@bot.command()
@commands.has_permissions(administrator=True)
async def start(ctx):
    """Inicia o envio automático"""
    global canal_id
    canal_id = ctx.channel.id
    if not enviar_mensagem.is_running():
        enviar_mensagem.start()
    await ctx.send("✅ Bot iniciado")

@bot.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    """Para o envio automático"""
    if enviar_mensagem.is_running():
        enviar_mensagem.cancel()
    await ctx.send("⛔ Bot parado")

@bot.command()
async def poluction(ctx):
    """Envia uma mensagem ambiental aleatória"""
    await ctx.send(random.choice(incentivos))

# ======================
# COMANDO DE AJUDA
# ======================
@bot.command()
async def ajuda(ctx):
    """Mostra todos os comandos do bot"""
    mensagem = (
        "**🌱 Comandos do Bot de Poluição**\n\n"
        "`$poluction` → Envia uma mensagem ambiental aleatória\n\n"
        "**⚙️ Comandos de Administração:**\n"
        "`$periodo HH:MM HH:MM` → Define o horário de funcionamento\n"
        "`$delay HORAS` → Define o intervalo entre mensagens\n"
        "`$start` → Inicia o envio automático no canal atual\n"
        "`$stop` → Para o envio automático\n\n"
        "🔒 Apenas administradores podem usar os comandos de administração."
    )
    await ctx.send(mensagem)

# ======================
bot.run(TOKEN)
