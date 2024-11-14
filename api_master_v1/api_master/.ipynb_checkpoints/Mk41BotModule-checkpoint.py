import telebot
from api_master import config, payments, Mk41BotMarkup
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

@herby.message_handler(commands=['start'])
def starter(message):
    herby.send_chat_action(message.chat.id,'typing')
    herby.send_message(message.chat.id, "Sure !", reply_markup=Mk41BotMarkup.clear_prev_markup())
   