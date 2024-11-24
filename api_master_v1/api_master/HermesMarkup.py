from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply, InputMediaVideo

def clear_prev_markup():
    clear_prev_keyboard = ReplyKeyboardRemove(selective=False)
    return clear_prev_keyboard

def prompt_input_markup():
    markup = ForceReply(selective=False)
    return markup


def start_one_markup():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    browse_btn = KeyboardButton('Browse')
    select_btn = KeyboardButton('Select')
    return markup

