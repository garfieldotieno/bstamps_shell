import telebot
from api_master import config, BluMarkup
import api_master.payments as payments
import os
import time 


blu = telebot.TeleBot(config.blu_config['API_TOKEN'])

def listener(message):
    """Whenever a message arrives for the blu bot (forwarded), Telebot will call this method"""
    for m in message:
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


blu.set_update_listener(listener)

time.sleep(0.5)

blu_set_webhook_url = config.blu_config['WEBHOOK_URL_BASE'] + config.blu_config['WEBHOOK_URL_PATH']
print(blu_set_webhook_url)

print('set_webhook', blu.set_webhook( url= blu_set_webhook_url))

@blu.message_handler(commands=['start'])
def starter(message):
    blu.send_chat_action(message.chat.id,'typing')
    blu.send_message(message.chat.id, "Sure !", reply_markup=BluMarkup.clear_prev_markup())
    blu.send_message(message.chat.id, "What would you like to do ?", reply_markup=BluMarkup.clear_prev_markup())
    local_host = f'{os.getcwd()}/static/bot_media/wakeup_it0_small.gif'
    img = open(local_host, 'rb')
    blu.send_document(message.chat.id, data=img)
    blu.send_message(message.chat.id, "What would you like to do ?", reply_markup=BluMarkup.start_one_markup())