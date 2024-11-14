from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply, InputMediaVideo
from api_master.config import stickers_object
from api_master.db import base_bot_db, swatsika_db
from api_master.models import UserSessionProfile

import json
import yaml

import datetime

import os


class BaseBot():
       
    __private_class_value = 'swatika-off'
        
    __mk40_master_id_list = ['821320826']
    
    def __init__(self, model_dict, ingress_message):
        self.user_id = str(model_dict['uid'])
        self.bot_id = str(model_dict['bot_id'])
        self.ingress_data = str(ingress_message.text)

        existing_session = UserSessionProfile.get(self.user_uid)

        if existing_session is None:
            print('should be creating a new\n1.session')
            self.clear_user_session(self.user_uid)
            session_init = {
                'uid': self.user_uid, 
                'is_admin': self.is_admin(),
                'is_authorized': False, 
                'bot_id': self.bot_id, 
                'activity_json': {
                    'last_input': None,
                    'current_input': self.ingress_data, 
                    'slot_filling': False,
                    'menu_base': 'auth_menu_navigation',
                    'menu_item_count': 0,
                    'intent_key': 'start',
                    'expected_input_list': [],
                },
                'response_json': {}
            }
            
            print(f"session to be initiated is : {session_init}")
            
            session_init = UserSessionProfile(**session_init)
            session_init.save()
                        
        else:
            print('session is existing and needs to be updated with ingress data')
            self.process_input(ingress_message)


    def is_admin(self):
        if self.user_uid in UserSessionProfile.__mk40_master_id_list:
            return True
        else:
            return False

    @staticmethod
    def process_input(message):
        print(f"about to process message: {message}")
        pass 


