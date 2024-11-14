import telebot
from api_master import config,Mk40Markup
from api_master.BaseBotModule import BaseBot, yaml
import os
import time 


jarvis = telebot.TeleBot(config.mk40_config['API_TOKEN'])

def listener(message):
    """Whenever a message arrives for the mk40 bot (forwarded), Telebot will call this method"""
    for m in message:
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


jarvis.set_update_listener(listener)

time.sleep(0.5)

jarvis_set_webhook_url = config.mk40_config['WEBHOOK_URL_BASE'] + config.mk40_config['WEBHOOK_URL_PATH']
print(jarvis_set_webhook_url)

print('set_webhook', jarvis.set_webhook( url= jarvis_set_webhook_url))


@jarvis.message_handler(content_types=['text'])
def process_every_input(message):
    print(f"received message in MK40BotModule {message}")
    b_i = BaseBot(message, 'MK40_BOT')

    if b_i.is_admin():
        print('is admin')
        if b_i.is_authorized():
            print('admin is authorized')
            if BaseBot.process_input(message):
                jarvis.send_chat_action(message.chat.id, 'typing')
                render_bot_ui(message.chat.id) 
            else:
                show_error_ui(message.chat.id)
        else:
            print('admin is not authorized')
            if BaseBot.process_one(message):
                jarvis.send_chat_action(message.chat.id, 'typing') 
                render_bot_ui(message.chat.id)
            else:
                show_error_ui(message.chat.id)
    else:
        process_zero(message) 


def render_bot_ui(user_id):
    # fetch and render response_dict
    user_session =  BaseBot.check_is_existing_user(user_id)
    jarvis.send_message(user_id, user_session['response_json']['message'], reply_markup=Mk40Markup.render_response_button_markup(user_session['activity_json']['expected_input_list']))
    jarvis.send_photo(user_id, user_session['response_json']['media'][0]['uid'])              
    msg = jarvis.send_message(user_id, user_session['response_json']['navigation_title'])
    jarvis.register_next_step_handler(msg, process_every_input)

    
def show_error_ui(user_id):
    user_session =  BaseBot.check_is_existing_user(user_id)
    jarvis.send_sticker(user_id, user_session['response_json']['media'][1]['uid'])
    jarvis.send_message(user_id, user_session['response_json']['message'], reply_markup=Mk40Markup.render_response_button_markup(user_session['activity_json']['expected_input_list']))
    jarvis.send_photo(user_id, user_session['response_json']['media'][0]['uid'])              
    msg = jarvis.send_message(message.chat.id, user_session['response_json']['navigation_title'])
    jarvis.register_next_step_handler(msg, process_every_input)



def process_zero(message):
    print('non-Admin user')
    pass
     

