import telebot
from api_master import config,Mk40Markup
from api_master.BaseBotModule import BaseBot
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
    b_i = BaseBot(message.chat.id, 'MK40_BOT', message.text)

    if b_i.is_admin():
        print('is admin')
        render_bot_ui(message.chat.id)
    else:
        pass 
    pass 


def process_input(self):
        session_dict = BaseBot.check_is_existing_user(self.user_id)
        print(f"processing input, and session dict is : {session_dict}")
        activity = {}
        activity['last_input'] = session_dict['activity_json']['current_input']
        activity['current_input'] = self.ingress_data
        activity['slot_filling'] = session_dict['activity_json']['slot_filling']
        
        if 'navigation_count' in [key for key,value in session_dict['activity_json'].items()]:
            activity['navigation_count'] = session_dict['activity_json']['navigation_count']
            
        elif 'menu_count' in [key for key,value in session_dict['activity_json'].items()]:
            activity['menu_count'] = session_dict['activity_json']['menu_count']
        
        base_bot_db.json().set(f"user:{self.user_id}:session", ".activity_json", activity)
        

def render_bot_ui(user_id):
    # fetch and render response_dict
    user_session =  BaseBot.check_is_existing_user(user_id)
    jarvis.send_message(message.chat.id, user_session['response_json']['message'], reply_markup=Mk40Markup.render_response_button_markup(b_i.generate_response()['buttons']))
    jarvis.send_photo(message.chat.id, user_session['response_json']['media'][0]['uid'])
                  
    msg = jarvis.send_message(message.chat.id, user_session['response_json']['navigation_title'])
    jarvis.register_next_step_handler(msg, process_resource_input_navigation)
            
     