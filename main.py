import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json

ARQUIVO = "dados.json"

def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {}

def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

contadores = carregar()

async def erro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /erro Nome")
        return

    nome = context.args[0]

    contadores[nome] = contadores.get(nome, 0) + 1
    salvar(contadores)

    await update.message.reply_text(
        f"❌ {nome} fez algo errado!\nTotal: {contadores[nome]}"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not contadores:
        await update.message.reply_text("Ainda não há dados.")
        return

    texto = "📊 Ranking:\n"
    for nome, valor in sorted(contadores.items(), key=lambda x: -x[1]):
        texto += f"{nome}: {valor}\n"

    await update.message.reply_text(texto)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contadores.clear()
    salvar(contadores)
    await update.message.reply_text("🔄 Contadores resetados!")

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

app.add_handler(CommandHandler("erro", erro))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("reset", reset))

print("🤖 Bot iniciado...")
app.run_polling()
