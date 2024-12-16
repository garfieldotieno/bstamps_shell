from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply, InputMediaVideo

def clear_prev_markup():
    clear_prev_keyboard = ReplyKeyboardRemove(selective=False)
    return clear_prev_keyboard

def prompt_input_markup():
    markup = ForceReply(selective=False)
    return markup


def main_markup():
    print(f"\n\ncalled button markup : main_markup")

    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    browse_btn = KeyboardButton('Browse')
    select_btn = KeyboardButton('Select')
    cancel_btn = KeyboardButton('Cancel')
    markup.add(browse_btn,select_btn, cancel_btn)
    return markup

# useful during slot filling process

def cancel_markup():
    print(f"\n\ncalled button markup : cancel_markup")

    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cancel_btn = KeyboardButton('Cancel')
    markup.add(cancel_btn)
    return markup

# for selecting session type
def session_type_markup():
    print(f"\n\ncalled button markup : session_type_markup")

    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    vendor_btn = KeyboardButton('Vendor')
    customer_btn = KeyboardButton("Customer")
    cancel_btn = KeyboardButton("Cancel")
    markup.add(vendor_btn, customer_btn, cancel_btn)
    return markup

