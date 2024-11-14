import telebot
from api_master import config, payments, Mk41BotMarkup, models
import os
import time 


herby = telebot.TeleBot(config.mk41_config['API_TOKEN'])

def listener(message):
    """Whenever a message arrives for the mk41 bot (forwarded), Telebot will call this method"""
    for m in message:
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


herby.set_update_listener(listener)

time.sleep(0.5)

herby_set_webhook_url = config.mk41_config['WEBHOOK_URL_BASE'] + config.mk41_config['WEBHOOK_URL_PATH']
print(herby_set_webhook_url)

print('set_webhook', herby.set_webhook( url= herby_set_webhook_url))


def telegram_page_view(telegram_id):
    pass 

def navigate_current_resource(telegram_id):
    pass 



# @herby.message_handler(commands=['start'])
# def starter(message):
#     herby.send_chat_action(message.chat.id,'typing')
#     herby.send_message(message.chat.id, "Sure !", reply_markup=Mk41BotMarkup.clear_prev_markup())


@herby.message_handler(func=lambda message: True, content_types=['text'])
def process_text_message(message):
    redis_session = models.UserSessionProfile.get(message.chat.id)
    user_input = message.text 
    activity_view_data = redis_session.dict()['activity_json']
    print(f"evaluating acceptable intent input, {activity_view_data['acceptable_intent_input']}")

    bot_view_data = redis_session.dict()['response_json']
    buttons = bot_view_data['current_bot_buttons']
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for btn in buttons:
        keyboard.add(telebot.types.KeyboardButton(btn))

    if user_input in activity_view_data['acceptable_intent_input']:
        
        if activity_view_data['slot_filling']:
            pass 
        else:
            print(f"no slot-filling happening here")
            if user_input == "Landing_page":
                pass 
            elif user_input == "Cancel":
                pass 
            elif user_input == "Refresh":
                pass 
            elif user_input == "About":
                pass 
            elif user_input == "Call":
                pass 
            elif user_input == "Mail":
                pass 
            else:
                redis_session.update_activity_intent("Landing_page")

        herby.send_chat_action(message.chat.id, 'typing')
        herby.send_message(message.chat.id, "Sure!", reply_markup=Mk41BotMarkup.clear_prev_markup())
        herby.send_message(message.chat.id, f"You entered: {message.text}", reply_markup=keyboard)
        
    else:
        herby.send_chat_action(message.chat.id, 'typing')
        herby.send_message(message.chat.id, "Sure!", reply_markup=Mk41BotMarkup.clear_prev_markup())
        herby.send_message(message.chat.id, "Unfortunately, the entered input is not acceptable! Use the buttons below", reply_markup=keyboard)