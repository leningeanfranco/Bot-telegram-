import os
import json
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from ai_engine import AIEngine
from utils import generar_bin, verificar_bin, generar_cc, verificar_cc

# Cargar variables de entorno
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

# Inicializar la IA
ai = AIEngine()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido! Usa /generar_bins para empezar o /generar_tarjetas para ir a la acción.")

async def generar_bins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Buscando bins válidos, esto puede tardar...")

    bins_validos = []
    intentos = 0

    while len(bins_validos) < 1 and intentos < 15:
        bin_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        datos_bin = verificar_bin(bin_code, API_KEY)

        if datos_bin["valido"]:
            bins_validos.append(datos_bin)
            ai.registrar_bin_exitoso(bin_code)
        else:
            ai.registrar_bin_fallido(bin_code)

        intentos += 1

    if bins_validos:
        bin = bins_validos[0]
        mensaje = f"✅ Bin válido encontrado: {bin['bin']}\nTipo: {bin['tipo']}\nMarca: {bin['marca']}\nBanco: {bin['banco']}\nPaís: {bin['pais']}"
        await update.message.reply_text(mensaje)
        ai.guardar_bin(bin)
    else:
        await update.message.reply_text("❌ No se encontraron bins válidos después de varios intentos. Usa /generar_bins nuevamente.")

async def generar_tarjetas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bins_validos = ai.cargar_bins_validos()

    if not bins_validos:
        await update.message.reply_text("Primero genera algunos bins con /generar_bins")
        return

    bin = random.choice(bins_validos)['bin']
    cc = generar_cc(bin, API_KEY)
    chequeo = verificar_cc(cc, API_KEY)

    if chequeo["valido"]:
        ai.registrar_cc_exitosa(cc)
        mensaje = f"✅ Tarjeta válida generada y chequeada:\nNúmero: {cc}\nTipo: {chequeo['tipo']}\nMarca: {chequeo['marca']}\nBanco: {chequeo['banco']}\nPaís: {chequeo['pais']}"
        await update.message.reply_text(mensaje)
        ai.guardar_cc(chequeo)
    else:
        ai.registrar_cc_fallida(cc)
        await update.message.reply_text(f"❌ Tarjeta generada falló en el chequeo: {cc}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generar_bins", generar_bins))
    app.add_handler(CommandHandler("generar_tarjetas", generar_tarjetas))

    print("✅ Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
