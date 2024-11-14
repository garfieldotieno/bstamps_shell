from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply, InputMediaVideo
from api_master.db import base_bot_db

def clear_prev_markup():
    clear_prev_keyboard = ReplyKeyboardRemove(selective=False)
    return clear_prev_keyboard

def prompt_input_markup():
    markup = ForceReply(selective=False)
    return markup

def render_response_button_markup(payload):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    for item in payload:
        btn = KeyboardButton(str(item))
        markup.add(btn)
    return markup



    
def start_one_markup():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    browse_btn = KeyboardButton('Browse')
    select_btn = KeyboardButton('Select')
    cancel_btn = KeyboardButton('Cancel')
    markup.add(browse_btn, select_btn, cancel_btn)
    return markup
