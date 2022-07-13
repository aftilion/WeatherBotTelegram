
from telebot import types

from Commands.helpmessage import help_message
from Commands.myauth import owm, bot

city = "Moscow"
standart_city = "Moscow"  # Used to rollback in case of an error in choosing a city
mgr = owm.weather_manager()
observation = mgr.weather_at_place(city)
w = observation.weather




@bot.message_handler(commands=["start"])
def starting_the_bot(message):
    """Bot launch function"""
    bot.send_message(
        message.chat.id,
        "Поздравляю, вы запустили бота. \nЧтобы получить помощь, введите /help"
    )

@bot.message_handler(commands=["help"])
def bot_helper_message(message):
    """Function that displays a help message"""
    bot.send_message(
        message.chat.id,
        help_message
    )


@bot.message_handler(commands=["change_city"])
def change_city(message):
    """A function that changes the city"""
    bot.send_message(
        message.chat.id,
        "Введите название города: "
    )


    @bot.message_handler(content_types=["text"])
    def change_city_variable(message):
        """A function that modifies a city variable"""
        global city, observation, w

        try:
            city = message.text
            observation = mgr.weather_at_place(city)
            w = observation.weather
            bot.send_message(message.chat.id, "Успешно!")

        except:
            bot.send_message(message.chat.id, "Ошибка! Город введён неверно")
            city = standart_city


@bot.message_handler(commands=["get_city"])
def get_city(message):
    """Function that displays the current city"""
    bot.send_message(
        message.chat.id,
        f"Текущий город: {city}"
    )


@bot.message_handler(commands=["weather"])
def get_weather(message):
    """Function that displays the weather in the city"""
    bot.send_message(message.chat.id,
                     f"""Полные сведения о погоде:

Регион: {city} 
Температура: {w.temperature('celsius').get("temp")}°C
Мин. температура: {w.temperature('celsius').get("temp_min")}°C
Макс. температура: {w.temperature('celsius').get("temp_max")}°C
Давление: {int(w.pressure.get("press") / 1.333)} мм рт. ст.
Влажность: {w.humidity}%
Облачность: {w.clouds}%
Статус: {w.detailed_status}
"""
                     )


@bot.message_handler(commands=["temp"])
def get_temperature(message):
    """Function that outputs temperature information"""
    bot.send_message(message.chat.id,
                     f"""Температура: {w.temperature('celsius').get('temp')}°C
Ощущается как: {w.temperature('celsius').get('feels_like')}°C"""
                     )


@bot.message_handler(commands=["humidity"])
def get_humidity(message):
    """Function that displays humidity information"""
    bot.send_message(
        message.chat.id,
        f"Атмосферная влажность: {w.humidity}%"
    )


@bot.message_handler(commands=["pressure"])
def get_pressure(message):
    """Function that displays humidity information"""
    bot.send_message(message.chat.id,
                     "Атмосферное давление: {} мм рт. ст.".format(int(w.pressure.get("press") / 1.333))
                     )


@bot.message_handler(commands=["keyboard"])
def show_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row("Показать возможности")
    bot.send_message(message.chat.id, f"⚡️ Привет, <b>{message.from_user.first_name}</b>", reply_markup=keyboard, parse_mode='HTML')


@bot.message_handler(content_types=["text"])
def show_answer(message):
    if message.text == "Показать возможности":
        bot.send_message(message.chat.id, help_message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
