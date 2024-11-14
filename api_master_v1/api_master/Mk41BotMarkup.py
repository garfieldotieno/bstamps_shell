from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply, InputMediaVideo

def clear_prev_markup():
    clear_prev_keyboard = ReplyKeyboardRemove(selective=False)
    return clear_prev_keyboard

def prompt_input_markup():
    markup = ForceReply(selective=False)
    return markup

def fetch_button_markup():
    pass 