import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

# Inicializar el bot con el token de Telegram proporcionado
bot = telebot.TeleBot("TELEGRAM_TOKEN")


# Define un gestor de mensajes para los comandos /start y /help.
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        """
    Hola, soy tu primer bot, estos son los comandos disponibles:
    \n /count - contar palabras o caracteres de un texto
    \n /start - mensaje de bienvenida
    """,
    )


# Definir un manejador de mensajes para el comando /count
@bot.message_handler(commands=["count"])
def count(message):
    # Crear un teclado personalizado con opciones para contar palabras o caracteres
    board = ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True
    )
    board.add(KeyboardButton("Contar palabras"), KeyboardButton("Contar caracteres"))
    # Envía un mensaje para elegir qué contar y registra el manejador del siguiente paso
    bot.send_message(message.chat.id, "Elige qué quieres contar:", reply_markup=board)
    bot.register_next_step_handler(message, handle_count_choice)


def handle_count_choice(message):
    # Compruebar la elección del usuario y proceder con la función correspondiente
    if message.text.lower() == "contar palabras":
        bot.send_message(
            message.chat.id, "Envía el texto del que deseas contar palabras"
        )
        bot.register_next_step_handler(message, count_words)
    elif message.text.lower() == "contar caracteres":
        bot.send_message(
            message.chat.id, "Envía el texto del que deseas contar caracteres"
        )
        bot.register_next_step_handler(message, count_characters)


def count_words(message):
    words = message.text.split()
    word_count = len(words)
    bot.reply_to(message, f"El texto tiene {word_count} palabras")


def count_characters(message):
    char_count = len(message.text)
    bot.reply_to(message, f"El texto tiene {char_count} caracteres")


# Definir un gestor de mensajes para textos generales
@bot.message_handler(content_types=["text"])
def hola(message):
    if message.text.lower() in ["hola", "hello", "hi"]:
        bot.send_message(
            message.chat.id,
            f"Hola {message.from_user.first_name}, ¿en qué te puedo ayudar?",
        )
    else:
        bot.send_message(
            message.chat.id,
            "Comando no encontrado. Por favor, usa /start para revisar los comandos disponibles",
        )


# Empezar a recibir mensajes
bot.polling()
