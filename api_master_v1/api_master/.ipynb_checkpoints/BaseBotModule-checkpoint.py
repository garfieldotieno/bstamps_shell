from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply, InputMediaVideo
from api_master.config import stickers_object
from api_master.db import base_bot_db, swatsika_db
from api_master.models import usersessionprofile, shopping

import json
import yaml

import datetime

import os


class BaseBot():
       
    __private_class_value = 'swatika-off'
        
    __mk40_master_id_list = ['821320826']
    
    
    def __init__(self, message, bot_id):
        self.user_id = str(message.chat.id)
        self.bot_id = str(bot_id)
        self.ingress_data = str(message.text)

        existing_session = BaseBot.check_is_existing_user(message.chat.id) 

        if existing_session == None:
            
            print('should be creating a new\n1.session')
            BaseBot.clear_user_session(self.user_id)
            session_init = {
                'uid':self.user_id, 
                'is_admin':self.is_admin(),
                'is_authorized':False, 
                'bot_name':self.bot_id, 
                'activity_json':{
                    'last_input':None,
                    'current_input':self.ingress_data, 
                    'slot_filling':False,
                    'menu_base':'auth_menu_navigation',
                    'menu_item_count':0,
                    'intent_key' : 'start',
                    'expected_input_list':[],
                },
                'response_json' : {}
                }
            
            print(f"session to be initiated is : {session_init}")
            
            session_init = usersessionprofile(**session_init)
            BaseBot.create_user_session(self.user_id, session_init.dict())
                        
        else:
            print('session is existing and needs to be updated with ingress data')
            BaseBot.process_input(message)
               
    
    def is_admin(self):
        if self.user_id in BaseBot.__mk40_master_id_list:
            return True
        else:
            return False
    
    def is_authorized(self):
        return base_bot_db.json().get(f'user:{self.user_id}:session', '.is_authorized')
     

    @staticmethod
    def check_is_existing_user(user_id):
        return base_bot_db.json().get(f'user:{user_id}:session') 

      
    @staticmethod
    def create_user_session(user_id,session_payload):
        base_bot_db.sadd('users:client_id:set', str(user_id))
        base_bot_db.json().set(f'user:{str(user_id)}:session', '$', session_payload)
        base_bot_db.expire(f'user:{str(user_id)}:session',session_payload['session_duration'])
    

    @staticmethod
    def clear_user_session(user_id):
        try:
            return base_bot_db.srem('users:client_id:set', user_id)
        except Exception as e :
            return {'status':False, 'message':f'unable to clear user  {user_id} session :> {e}'} 

    


    @staticmethod
    def update_user_session_ttl(user_id, ttl):
        try:
            return base_bot_db.expire(f'user:{user_id}:session', ttl)
        except Exception as e :
            return {'status':False, 'message':f'unable to update user  {user_id} session :> {e}'} 


    @staticmethod
    def check_user_session_ttl(user_id):
        try:
            return base_bot_db.ttl(f'user:{user_id}:session')
        except Exception as e :
            return {'status':False, 'message':f'unable to get ttl for user {user_id} session :> {e}'}
    
     
    @staticmethod
    def process_input(message, bot_object):
        print("calling process_input function")
        print("updating *_input in activity_json")
        last_input = base_bot_db.json().get(f"user:{message.chat.id}:session", ".activity_json.current_input")
        base_bot_db.json().set(f"user:{message.chat.id}:session", ".activity_json.current_input", message.text)
        base_bot_db.json().set(f"user:{message.chat.id}:session", ".activity_json.last_input", last_input)
        
        print("testing for function x()")
        if BaseBot.is_slot_filling(message):
            # passing to p*
            BaseBot.recover_in_slot_filling(message)
        else:
            if BaseBot.is_acceptable_input(message):
                if BaseBot.is_cancel(message):
                    BaseBot.reset_user_navigation(message) 
                else:
                    # passing to eval
                    BaseBot.run_user_eval(message)
            else: 
                show_error_ui(message, BaseBot.reset_user_navigation)
    
    @staticmethod 
    def process_one(message, base_object):
        print("calling process_one method")
        if base_bot_db.json().get(f"user:{message.chat.id}:session", ".bot_name") == "MK40_BOT":
            bot_scope = yaml.load(open(f"{os.getcwd()}/api_master/mk40.yml"), Loader=yaml.FullLoader)
            response = bot_scope['auth_menu_navigation']['items'][0]
            expected_input_list = bot_scope['auth_menu_navigation']['item_intent_hash']['start']
        # update user activity json
        BaseBot.update_expected_user_input_list(message, expected_input_list)
        # update usersessionprofile response_json
        BaseBot.update_user_response(message, response) 
    
    
    @staticmethod
    def recover_in_slot_filling(message):
        print("calling recover_in_slot_filling")
        print("about to revocer in open_slot_filling")
        pass 

    @staticmethod 
    def run_user_eval(message):
        print("calling run_user_eval method")
        print("abot to start user evaluation")
        pass 
    
    
    
    @staticmethod
    def render_bot_ui(message, handler_function):
        # fetch and render response_dict
        user_session =  BaseBot.check_is_existing_user(message.chat.id)
        jarvis.send_message(message.chat.id, user_session['response_json']['message'], reply_markup=Mk40Markup.render_response_button_markup(user_session['activity_json']['expected_input_list']))
        jarvis.send_photo(message.chat.id, user_session['response_json']['media'][0]['uid'])              
        msg = jarvis.send_message(message.chat.id, user_session['response_json']['navigation_title'])
        jarvis.register_next_step_handler(msg, handler_function)

    @staticmethod
    def show_error_ui(message, handler_function):
        user_session =  BaseBot.check_is_existing_user(message.chat.id)
        jarvis.send_sticker(message.chat.id, user_session['response_json']['media'][1]['uid'])
        jarvis.send_message(message.chat.id, user_session['response_json']['message'], reply_markup=Mk40Markup.render_response_button_markup(user_session['activity_json']['expected_input_list']))
        jarvis.send_photo(message.chat.id, user_session['response_json']['media'][0]['uid'])              
        msg = jarvis.send_message(message.chat.id, user_session['response_json']['navigation_title'])
        jarvis.register_next_step_handler(msg, handler_function)
    
    
    
    
    
    
    
    
    

    @staticmethod    
    def is_slot_filling(message):
        print("calling is_slot_filling method")
        return base_bot_db.json().get(f"user:{message.chat.id}:session", ".activity_json.slot_filling")
        

    @staticmethod
    def is_acceptable_input(message):
        print("calling is_acceptable method")
        # should check the .activity_json.intent_key then look it up from the auth_menu_navigation.iten_intent_hash.key
        activity_json = base_bot_db.json().get(f"user:{message.chat.id}:session", '.activity_json')
        return activity_json['current_input'] in activity_json['expected_input_list']
        
        
    @staticmethod
    def is_cancel(message):
        print(f"calling is_cancel method with input {message.text}")
        if message.text == 'Cancel':
            return True
        else:
            return False

    @staticmethod 
    def is_continue(message):
        print('calling is_continue method')
        pass 

    @staticmethod
    def reset_user_navigation(message):
        print("calling reset_user_navigation")
        # get *_base key for ref with the yml file
        base_key = base_bot_db.json().get(f"user:{message.chat.id}:session", ".activity_json.menu_base")
        intent_key = base_bot_db.json().get(f"user:{message.chat.id}:session", ".activity_json.intent_key")

        if base_bot_db.json().get(f"user:{message.chat.id}:session", ".bot_name") == "MK40_BOT":
            bot_scope = yaml.load(open(f"{os.getcwd()}/api_master/mk40.yml"), Loader=yaml.FullLoader)
            response = bot_scope[base_key]['items'][0]
            expected_input_list = bot_scope[base_key]['item_intent_hash'][intent_key]
        
        base_bot_db.json().set(f"user:{message.chat.id}:session", '.activity_json.menu_item_count', 0)
        base_bot_db.json().set(f"user:{message.chat.id}:session", ".activity_json.expected_input_list", expected_input_list)
        base_bot_db.json().set(f"user:{message.chat.id}:session", ".activity_json.slot_filling", False)
        base_bot_db.json().set(f"user:{message.chat.id}:session", ".response_json", response)   

        
 
        
    def get_activity_dict(self):
        return base_bot_db.json().get(f"user:{self.user_id}:session", ".activity_json")
    
    
    def get_response_dict(self):
        return base_bot_db.json().get(f"user:{self.user_id}:session", ".response_json")
    


    @staticmethod
    def update_expected_user_input_list(message, expected_input_list):
        return base_bot_db.json().set(f"user:{message.chat.id}:session", ".activity_json.expected_input_list", expected_input_list)
    
    @staticmethod
    def update_user_response(message, response):
        return base_bot_db.json().set(f"user:{message.chat.id}:session", ".response_json", response)
         

 


 

    