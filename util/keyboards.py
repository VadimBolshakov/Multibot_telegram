from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from create import i18n

_ = i18n.gettext

main_menu = InlineKeyboardMarkup(row_width=2)
main_menu.add(InlineKeyboardButton(_('Weather'), callback_data='weather'),
              InlineKeyboardButton(_('Maps'), callback_data='maps'),
              InlineKeyboardButton(_('Translate'), callback_data='translate'),
              InlineKeyboardButton(_('Currency'), callback_data='currency_ru'),
              InlineKeyboardButton(_('News'), callback_data='news'),
              InlineKeyboardButton(_('Jokes'), callback_data='jokes')
              ).add(InlineKeyboardButton('ChatGPT', callback_data='chat_gpt'))

# main_menu = InlineKeyboardMarkup(row_width=2)
# main_menu.add(InlineKeyboardButton('Погода', callback_data='weather'),
#               InlineKeyboardButton('Локация', callback_data='maps'),
#               InlineKeyboardButton('Переводчик', callback_data='translate'),
#               InlineKeyboardButton('Валюты', callback_data='currency_ru'),
#               InlineKeyboardButton('Новости', callback_data='news'),
#               InlineKeyboardButton('Анекдоты', callback_data='jokes')
#               ).add(InlineKeyboardButton('ChatGPT', callback_data='chat_gpt'))


map_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('Get location', request_location=True)
button_2 = KeyboardButton('Get by IP')
button_3 = KeyboardButton("Cancel")
map_menu.row(button_1, button_2).add(button_3)


translate_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('English')
button_2 = KeyboardButton('Russian')
button_3 = KeyboardButton('Ukrainian')
button_4 = KeyboardButton('German')
button_5 = KeyboardButton('French')
button_6 = KeyboardButton('Italian')
button_7 = KeyboardButton('Spanish')
button_8 = KeyboardButton('Greek')
button_9 = KeyboardButton('Polish')
button_10 = KeyboardButton('Portuguese')
button_11 = KeyboardButton('Turkish')
button_12 = KeyboardButton('Arabic')
button_13 = KeyboardButton('Japanese')
button_14 = KeyboardButton('Chinese')
button_15 = KeyboardButton("Cancel")


translate_menu.row(button_1, button_2)\
    .row(button_3, button_4)\
    .row(button_5, button_6)\
    .row(button_7, button_8)\
    .row(button_9, button_10)\
    .row(button_11, button_12)\
    .row(button_13, button_14)\
    .add(button_15)


weather_menu_local = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('Get location', request_location=True)
button_2 = KeyboardButton('Enter city')
button_3 = KeyboardButton("Get by IP")
button_4 = KeyboardButton("Cancel")
weather_menu_local.add(button_1, button_2, button_3).add(button_4)


weather_period_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('Current')
button_2 = KeyboardButton('Hourly')
button_3 = KeyboardButton("Daily")
button_4 = KeyboardButton("Cancel")
weather_period_menu.add(button_1, button_2, button_3).add(button_4)


weather_volume_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('Short')
button_2 = KeyboardButton('Full')
button_3 = KeyboardButton("Cancel")
weather_volume_menu.add(button_1, button_2).add(button_3)


news_category_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('Business')
button_2 = KeyboardButton('Entertainment')
button_3 = KeyboardButton("General")
button_4 = KeyboardButton("Health")
button_5 = KeyboardButton('Science')
button_6 = KeyboardButton('Sports')
button_7 = KeyboardButton('Technology')
button_8 = KeyboardButton("Cancel")
news_category_menu.add(button_1, button_2)\
    .row(button_3, button_4)\
    .row(button_5, button_6)\
    .add(button_7, button_8)

news_query_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('All')
button_2 = KeyboardButton('Cancel')
news_query_menu.add(button_1, button_2)

language_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton('English')
button_2 = KeyboardButton('Русский')
button_3 = KeyboardButton("Cancel")
language_menu.add(button_1, button_2).add(button_3)

