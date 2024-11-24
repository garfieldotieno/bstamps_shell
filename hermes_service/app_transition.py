import os
from flask import Flask, request
import telebot
from dotenv import load_dotenv
from blu import Session 
import string 
import random
import time 

from models import SessionLocal, SlotQuestion

from payments2 import send_user_stk, send_payment

import uuid
from Markup import clear_prev_markup, main_markup
import re 
import json
import requests
import asyncio 
import aiohttp 


# Load environment variables from .env file
load_dotenv()

# Retrieve Telegram bot token from environment variable
BOT_TOKEN = os.getenv('telegram_bot_auth_token')
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN', "123456")
GRAPH_API_TOKEN = os.getenv('GRAPH_API_TOKEN', "EAAUCpth1wAIBOwSjahZBybIoVOzcR97IOXRYWNpErmislpMWXvMdIHHTofe4s2zB8huYGWZCU5ZASWPdZBKQIrpRzzt524H0S3RpgaCUZB7ioNbGXRNu0muwzVX6UhM1QnRnlM0XmERkPc51pEwA7smsR5lTqHVinQEjWg2aBtOyXRZAD7uDG6zPPRvLxTlZCw6CtocxalCTyi1kIv0xKViRAR4CGIZD")
PORT = int(os.getenv('PORT'))



# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot
tele_bot = telebot.TeleBot(BOT_TOKEN)

def listener(messages):
    """Whenever a message arrives for the blu bot (forwarded), Telebot will call this method"""
    for message in messages:
        if message.content_type == 'text':
            print(f"{message.chat.first_name} [{message.chat.id}]: {message.text}")


tele_bot.set_update_listener(listener)


def generate_uid(length=10):
    chars = string.ascii_letters  + string.digits
    uid = "".join(random.choice(chars) for _ in range(length))
    return uid



main_menu_no_session_listing = [
    {
        'menu_code': 'ACCOUNT',
        'media': ['https://ibb.co/cJZMRLk'],
        'menu_message': "Account menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'ABOUT',
        'media': ['https://ibb.co/tsC248m'],
        'menu_message': "About menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE9mZy8gABviXQSyg6H2gk0fG1C4TQrQACbQADpsrIDMzP5klyYCgJNQQ'
    }
    ]



main_menu_customer_session_listing = [
    {
        'menu_code': 'ACCOUNT',
        'media': ['https://ibb.co/cJZMRLk'],
        'menu_message': "Account menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'SHOP',
        'media': ['https://ibb.co/bB6cNYN'],
        'menu_message': "Shop menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'ABOUT',
        'media': ['https://ibb.co/tsC248m'],
        'menu_message': "About menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE9mZy8gABviXQSyg6H2gk0fG1C4TQrQACbQADpsrIDMzP5klyYCgJNQQ'
    },
    {
        'menu_code': 'REFERALL',
        'media': ['https://ibb.co/6nrjhwy'],
        'menu_message': "Referall menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'DELIVERY',
        'media': ['https://ibb.co/6N3vRK0'],
        'menu_message': "Delivery menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]




main_menu_vendor_session_listing = [
    {
        'menu_code': 'ACCOUNT',
        'media': ['https://ibb.co/cJZMRLk'],
        'menu_message': "Account menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'UPLOAD_ITEM',
        'media': ['https://ibb.co/bQ6QsP8'],
        'menu_message': "Shop menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'ABOUT',
        'media': ['https://ibb.co/tsC248m'],
        'menu_message': "About menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE9mZy8gABviXQSyg6H2gk0fG1C4TQrQACbQADpsrIDMzP5klyYCgJNQQ'
    },
    {
        'menu_code': 'REFERALL',
        'media': ['https://ibb.co/6nrjhwy'],
        'menu_message': "Referall menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'DELIVERY',
        'media': ['https://ibb.co/6N3vRK0'],
        'menu_message': "Delivery menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]



# Sample menu listing
main_menu_listing = [
    {
        'menu_code': 'ACC',
        'media': ['https://ibb.co/NrKq46z'],
        'menu_message': "Account menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code': 'TSK',
        'media': ['https://ibb.co/cL3hmWQ'],
        'menu_message': "Request Task menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE8mZy8cczs7MMMxHnh_HY5oh2T9wpAAK3AAP3AsgPkPG2BzshSB01BA'
    },
    {
        'menu_code': 'ABT',
        'media': ['https://ibb.co/VjtwrcB'],
        'menu_message': "About menu\n\nProceed by selecting one of the buttons",
        'menu_sticker':'CAACAgIAAxkBAAIE9mZy8gABviXQSyg6H2gk0fG1C4TQrQACbQADpsrIDMzP5klyYCgJNQQ'
    } 
]


acc_submenu_listing = [{
    'menu_code':'acc_a',
    'media':['https://ibb.co/M12tDZc'],
    'menu_message':"Register sub menu\n\nProceed by selectingone of the buttons",
    'menu_sticker':'CAACAgIAAxkBAAIE_mZy8knmFGj0uTwgkfZeVcNT6X5QAAI8AAPBnGAMnT29Tay9Qbk1BA'
},
{
    'menu_code':'acc_b',
    'media':['https://ibb.co/hK7LXrm'],
    'menu_message':"Wallet sub menu\n\nProceed by selecting one of the buttons",
    'menu_sticker':'CAACAgIAAxkBAAIFAmZy8mFtAAHKIsabXRtHNtkbh7pphQACOAADwZxgDA6ToHc1KTAqNQQ'
},
{
    'menu_code':'acc_c',
    'media':['https://ibb.co/gTLH5hC'],
    'menu_message':"Withdraw sub menu\n\nProceed by selecting one of the buttons",
    'menu_sticker':'CAACAgIAAxkBAAIFBmZy8npVYgr5YruHVPnIJNFqDzDkAAJLAAPBnGAMAAH3CziPiOBmNQQ'
}]


tsk_submenu_listing = [{
    'menu_code':'tsk_a',
    'media':['https://ibb.co/hVRgBpM'],
    'menu_message':"Send money sub menu\n\nProceed by selecting one of the buttons",
    'menu_sticker':'CAACAgIAAxkBAAIFCmZy8qzJS9h4IzErfgQcyE338EcsAALDAAP3AsgPknDgAAFrl2NlNQQ'
}]

abt_submenu_listing = [{
    'menu_code':'abt_a',
    'media':['https://ibb.co/VjtwrcB'],
    'menu_message':'About summary\n\nProceed by selecting the button below',
    'menu_sticker':'CAACAgIAAxkBAAIFDmZy8utttisg1-BhZrlmHDORMi7mAAKGAAOmysgMdfHgn18JJQI1BA'
}]


menu_stack = {}
menu_stack['main_menu_vendor_session_listing'] = main_menu_vendor_session_listing
menu_stack['acc_submenu_listing'] = acc_submenu_listing
menu_stack['tsk_submenu_listing'] = tsk_submenu_listing
menu_stack['abt_submenu_listing'] = abt_submenu_listing


@tele_bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    # Retrieve the sticker file ID
    sticker_file_id = message.sticker.file_id
    
    # Log or print the sticker file ID for reference
    print(f"Received sticker with file ID: {sticker_file_id}")
    
    # Send a response message acknowledging the sticker
    tele_bot.send_message(message.chat.id, "Nice sticker! Thanks for sharing.")
    
    # Optionally, you can also send a sticker back to the user
    # Here, replace 'CAADAgADQAADyIsGAAE7MpzFPFQX7QI' with the file ID of the sticker you want to send
    response_sticker_file_id = sticker_file_id
    tele_bot.send_sticker(message.chat.id, response_sticker_file_id)



@app.route('/telegram', methods=['POST'])
def tele_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)

        # Process the update only once
        tele_bot.process_new_updates([update])
    
        if update.message:
            user_id = update.message.from_user.id
            user_name = update.message.from_user.username
            client_input = update.message.text.lower() if update.message.text else ''

                # Print or process the extracted data
            print(f"User ID: {user_id}, Username: {user_name}, Client Input: {client_input}")
            db = SessionLocal()

            if Session.is_first_time_contact(user_id):
                print(f"is continuing user")
                if int(Session.is_main_menu_nav(user_id)) == 1:

                    if client_input in ["browse", "select", "cancel"]:
                        if client_input == "browse":
                            print(f"main menu -- browse")
                            Session.browse_main(user_id, len(main_menu_vendor_session_listing))

                            current_count = Session.get_browsing_count(user_id)
                            menu_payload = main_menu_vendor_session_listing[current_count]
                            print(f"current payload during main browsing \n\n {menu_payload}")
                            # Send the message with buttons and media

                            menu_code = menu_payload['menu_code']
                            Session.update_session_menu_code(user_id, menu_code)

                            tele_bot.send_chat_action(update.message.chat.id, 'typing')
                            sticker_file_id = menu_payload['menu_sticker']
                            image_link = menu_payload['media'][0]

                            tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                            tele_bot.send_photo(update.message.chat.id, image_link)
                            tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())

                            return 'ok'
                        
                        if client_input == "cancel":
                            # cancel selected
                            print(f"main menu -- cancel")
                            Session.reset_browsing_count(user_id)

                            current_count = Session.get_browsing_count(user_id)
                            menu_payload = main_menu_vendor_session_listing[current_count]
                            print(f"current payload after reseting \n\n {menu_payload}")
                            # Send the message with buttons and media

                            tele_bot.send_chat_action(update.message.chat.id, 'typing')
                            sticker_file_id = menu_payload['menu_sticker']
                            image_link = menu_payload['media'][0]

                            tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                            tele_bot.send_photo(update.message.chat.id, image_link)
                            tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                            return 'ok'
                        
                        if client_input == "select":
                            print(f"main menu -- select")
                            current_count = Session.get_browsing_count(user_id)
                            print(f"current_count during main menu select is : {current_count}")

                            menu_payload = main_menu_vendor_session_listing[current_count]
                            print(f"selected payload\n\n {menu_payload}")

                            menu_code = menu_payload['menu_code']

                            if menu_code in ['ACC', 'TSK', 'ABT']:
                                # activate submenu navigation
                                # Session.off_main_menu_nav(user_id)
                                # Session.reset_navigation(user_id)
                                Session.reset_browsing_count(user_id)
                                
                                

                                if menu_code == "ACC":
                                    Session.on_sub1_menu_nav(user_id, 'acc_submenu_listing')
                                    # Session.load_submenu(user_id, 'acc_submenu_listing')

                                    # load
                                    submenu_payload = acc_submenu_listing[0]
                                    submenu_message = submenu_payload['menu_message']
                                    submenu_sticker = submenu_payload['menu_sticker']
                                    submenu_media = submenu_payload['media'][0]

                                    tele_bot.send_sticker(user_id, submenu_sticker)
                                    tele_bot.send_photo(user_id, submenu_media)
                                    tele_bot.send_message(user_id, submenu_message)
                                    return 'ok'
                                
                                elif menu_code == "TSK":
                                    Session.on_sub1_menu_nav(user_id, 'tsk_submenu_listing')
                                    # Session.load_submenu(user_id, 'tsk_submenu_listing')

                                    # load
                                    submenu_payload = tsk_submenu_listing[0]
                                    submenu_message = submenu_payload['menu_message']
                                    submenu_sticker = submenu_payload['menu_sticker']
                                    submenu_media = submenu_payload['media'][0]

                                    tele_bot.send_sticker(user_id, submenu_sticker)
                                    tele_bot.send_photo(user_id, submenu_media)
                                    tele_bot.send_message(user_id, submenu_message)
                                    return 'ok'
                                
                                elif menu_code == "ABT":
                                    Session.on_sub1_menu_nav(user_id, 'abt_submenu_listing')
                                    # Session.load_submenu(user_id, 'abt_submenu_listing')

                                    # load
                                    submenu_payload = abt_submenu_listing[0]
                                    submenu_message = submenu_payload['menu_message']
                                    submenu_sticker = submenu_payload['menu_sticker']
                                    submenu_media = submenu_payload['media'][0]

                                    tele_bot.send_sticker(user_id, submenu_sticker)
                                    tele_bot.send_photo(user_id, submenu_media)
                                    tele_bot.send_message(user_id, submenu_message)
                                    return 'ok'

                    else:
                        print(f"main menu navigation input warning")
                        return_message = "please use the buttons to navigate" 
                        tele_bot.send_message(user_id, return_message, main_markup())
                        return 'ok'

                else:
                    print(f"could be slotfilling or sub_menu [1,2] processing\n\n")
                    
                    if int(Session.is_submenu_browsing(user_id)) == 1:
                        
                        print(f"sub menu navigation, not slot filling ")
                        
                        if client_input in ['browse', 'select', 'cancel']:
                            if client_input == "browse":
                                print(f"sub menu --browse")
                                sub_menu = Session.get_current_submenu(user_id)
                                browsing_count = Session.get_browsing_count(user_id)

                                print(f"browsing submenu, should get the current submenu : {sub_menu}, and count is :{browsing_count}\n\n")

                                sub_menu_count = len(menu_stack[sub_menu])
                                # is not referencing the actual sub menu

                                print(f"current sub_menu is : {sub_menu}, and count is : {sub_menu_count}")

                                Session.browse_submain(user_id, sub_menu_count)


                                current_count = Session.get_browsing_count(user_id)

                                if sub_menu == "acc_submenu_listing":
                                    menu_payload = acc_submenu_listing[current_count]
                                    
                                    # Send the message with buttons and media

                                    tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                    sticker_file_id = menu_payload['menu_sticker']
                                    image_link = menu_payload['media'][0]

                                    tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                    tele_bot.send_photo(update.message.chat.id, image_link)
                                    tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                    return 'ok'
                                
                                elif sub_menu == "tsk_submenu_listing":
                                    menu_payload = tsk_submenu_listing[current_count]
                                    
                                    # Send the message with buttons and media

                                    tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                    sticker_file_id = menu_payload['menu_sticker']
                                    image_link = menu_payload['media'][0]

                                    tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                    tele_bot.send_photo(update.message.chat.id, image_link)
                                    tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                    return 'ok' 
                                
                                elif sub_menu == "abt_submenu_listing":
                                    menu_payload = abt_submenu_listing[current_count]
                                    
                                    # Send the message with buttons and media

                                    tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                    sticker_file_id = menu_payload['menu_sticker']
                                    image_link = menu_payload['media'][0]

                                    tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                    tele_bot.send_photo(update.message.chat.id, image_link)
                                    tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                    return 'ok' 

                                
                           
                            elif client_input == "cancel":
                                print(f"sub menu --cancel")
                                Session.reset_browsing_count(user_id)
                                Session.off_sub1_menu_nav(user_id)
                                

                                current_count = Session.get_browsing_count(user_id)
                                menu_payload = main_menu_vendor_session_listing[current_count]
                                print(f"current payload after reseting \n\n {menu_payload}")

                                tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                sticker_file_id = menu_payload['menu_sticker']
                                image_link = menu_payload['media'][0]

                                tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                tele_bot.send_photo(update.message.chat.id, image_link)
                                tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                return 'ok'
                             
                            elif client_input == "select":
                                print(f"sub menu --select")
                                print(f"begining slotfilling \n\n")
                                # get submenu
                                # get browsing count
                                # should off submenu browsing ?
                                # should activate slot filling
                                browsing_count = Session.get_browsing_count(user_id)
                                print(f"browsing_count is ; {browsing_count}")
                                sub_menu = Session.get_current_submenu(user_id)

                                if sub_menu == "acc_submenu_listing":
                                    if browsing_count == 0:
                                        pass 
                                     
                                elif sub_menu == "tsk_submenu_listing":
                                    if browsing_count == 0:
                                        print(f"selecting send money task\n\n")
                                        Session.load_handler(user_id, "sm_handler", "SM", 0, 3)
                                        curr_slot_details = Session.fetch_slot_details(user_id)
                                        print(f"fetched slot_details : {curr_slot_details}")
                                        
                                        
                                        slot_code = curr_slot_details['slot_code']

                                        quiz_pack = SlotQuestion.get_slot_questions(db,slot_code)

                                        quiz = Session.return_current_slot_quiz(user_id, quiz_pack)
                                        
                                        Session.step_slotting(user_id, quiz_pack)
                                        

                                        tele_bot.send_message(update.message.chat.id, quiz, clear_prev_markup())
                                        
                                        # sub1_menu should be off, slot_filling action
                                        Session.off_sub1_menu_nav(user_id)

                                        return 'ok'
                                         

                                     
                                elif sub_menu == "abt_submenu_listing":

                                    return 'ok'
                                
                                

                        else:
                            print(f"sub menu navigation input warning")
                            return_message = "please use the buttons below to proceed" 
                            tele_bot.send_message(user_id, return_message)
                            return 'ok'
                    
                    if Session.is_slot_filling(user_id):
                        print(f"yup user is slot_filling")
                        
                        current_handler = Session.get_session(user_id)[b'current_slot_handler'].decode('utf-8')
                        if current_handler == "ru_handler":
                            pass 
                        elif current_handler == "sm_handler":
                            print(f"\n\nprocessing sm_handler")
                            curr_slot_details = Session.fetch_slot_details(user_id)
                            slot_code = curr_slot_details['slot_code']
                            count_ = curr_slot_details['slot_count']
                            print(f"processing slot code {slot_code}, current_count {count_}")
                            print(f"type for count_ {type(count_)}")
                            count_ = int(count_)

                            if count_ == 0 or count_ == 1:
                                
                                print(f"count is either 0 or 1, {count_}")
                                # process quiz1
                                if is_valid_phone_number(client_input):
                                    print(f"{client_input}, is valid")
                                    Session.save_reg_answer(user_id, count_, client_input)

                                    if Session.complete_sm_slotting(user_id):
                                        message = f"Your request for Send Money task has been submitted,\n\nPlease wait for Mpesa prompt on +{user_id}\n\nThen enter your Mpesa PIN\n\nThank you 😊"
                                        Session.load_handler(user_id, 'st_handler', 'ST', 0, 1)
                                        Session.clear_answer_slot(user_id)

                                        print(f"user number is : {user_id}")
                                        tele_bot.send_message(update.message.chat.id, message, clear_prev_markup())

                                    else:
                                        quiz_pack = SlotQuestion.get_question_pack(db,slot_code)
                                        quiz = Session.return_current_slot_quiz(user_id, quiz_pack)
                                        Session.step_slotting(user_id, quiz_pack)
                                        tele_bot.send_message(update.message.chat.id, quiz, clear_prev_markup())

                                else:
                                    print(f"{client_input}, is invalid")
                                    message = "Error\n\nThat input was invalid"
                                    tele_bot.send_message(update.message.chat.id, message, clear_prev_markup())
                              

                            elif count_ == 2:
                                print(f"count is 2")

                                if is_valid_payment_amount(client_input):
                                    print(f"valid payment number : {client_input}")
                                    Session.save_answer(user_id, count_, client_input)
                                    if Session.complete_sm_slotting(user_id):
                                        message = f"Your request for Send Money task has been submitted,\n\nPlease wait for Mpesa prompt on +{user_id}\n\nThen enter your Mpesa PIN\n\nThank you 😊"
                                        Session.load_handler(user_id, 'st_handler', 'ST', 0, 1)

                                        print(f"user number is : {user_id}")
                                        end_number = Session.load_ans_payload(user_id)
                                        end_number = json.loads(end_number)
                                        print(f"end_number_list : {end_number}")
                                        print(f"end_number to set : {end_number[0]}, of type : {type(end_number[0])}")
                                        Session.clear_answer_slot(user_id)
                                        # send_user_stk(user_id, int(client_input), 'SM', end_number[0])
                                        send_user_stk('254703103960', int(client_input), 'SM', end_number[0])

                                        tele_bot.send_message(update.message.chat.id, message, clear_prev_markup())
                                    else:
                                        quiz_pack = SlotQuestion.get_question_pack(db,menu_code)
                                        quiz = Session.return_current_slot_quiz(user_id, quiz_pack)
                                        Session.step_slotting(user_id, quiz_pack)
                                        tele_bot.send_message(update.message.chat.id, quiz, clear_prev_markup())
                                else:
                                    print(f"{client_input}, is invalid")
                                    message = "Error\n\nThat input was invalid"
                                    tele_bot.send_message(update.message.chat.id, message, clear_prev_markup())
 

                        return 'ok'
            else:
                print(f"is user first time, creating session")
                new_count = 0

                if client_input:
                    print(f"starting to process /start\n\n")
                    new_user_session = Session(uid=generate_uid(),
                                           waid=user_id,
                                           name=user_name,

                                           current_menu_code='ACC',
                                           browsing_count=new_count,
                                           
                                           

                                           main_menu_nav=1,
                                           main_menu_select='',
                                           sub1_menu_nav=0,
                                           sub1_menu_select='',
                                           sub2_menu_nav=0,
                                           sub2_menu_select='',
                                           
                                           
                                           is_slot_filling=0,
                                           answer_payload='[]',
                                           user_flow='',
                                           current_slot_code='',
                                           current_slot_count=0,
                                           slot_quiz_count="",
                                           
                                           current_slot_handler='')
                    
                    new_user_session.save()

                    AccountSummary.add_summary(SessionLocal(), user_id)
                    current_count = Session.get_browsing_count(user_id)

                    menu_payload = main_menu_vendor_session_listing[current_count]
                    print(f"current menu payload : {menu_payload}")

                    menu_message = menu_payload['menu_message']
                    menu_code = menu_payload['menu_code']

                    Session.update_session_menu_code(user_id, menu_code)

                    tele_bot.send_chat_action(update.message.chat.id, 'typing')
                    sticker_file_id = menu_payload['menu_sticker']
                    image_link = menu_payload['media'][0]

                    tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                    tele_bot.send_photo(update.message.chat.id, image_link)
                    
                    # tele_bot.send_video(update.message.chat.id, "https://streamable.com/qbfpmz?src=player-page-share")
                    
                    tele_bot.send_message(user_id, menu_message, reply_markup=main_markup())

                    return 'ok' 
                else:
                    return 'ok' 
                
                
    else:
        return 'Invalid request', 403





        
     

async def send_post_request(url, json_data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data, headers=headers) as response:
            return await response.text()


@app.route('/webhook', methods=['POST'])
async def webhook():
    data = await request.get_json()
    print("Incoming webhook message:", data)

    message = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0]

    if message and message.get('type') == 'text':
        business_phone_number_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('phone_number_id')
        response_message = {
            "messaging_product": "whatsapp",
            "to": message.get('from'),
            "text": {"body": "Echo: " + message.get('text', {}).get('body')},
            "context": {
                "message_id": message.get('id')
            }
        }

        headers = {
            "Authorization": f"Bearer {GRAPH_API_TOKEN}"
        }

        # Send reply message
        await send_post_request(
            f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
            response_message,
            headers
        )


        # Mark incoming message as read
        mark_read_payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message.get('id')
        }

        await send_post_request(
            f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
            mark_read_payload,
            headers
        )

    return '', 200

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        return '', 403

def get_user_acc_summary_stmt(waid, user_name):
    acc_dict = AccountSummary.get_acc_summary(waid)
    if acc_dict:
        summary = {
            'total_deposit': acc_dict[b'total_deposit'].decode('utf-8'),
            'pending_settlement': acc_dict[b'pending_settlement'].decode('utf-8'),
            'total_settlement': acc_dict[b'total_settlement'].decode('utf-8'),
            'amount_deposited': acc_dict[b'amount_deposited'].decode('utf-8'),
            'amount_settled': acc_dict[b'amount_settled'].decode('utf-8'),
            'total_amount_saved':acc_dict[b'total_amount_saved'].decode('utf-8'),
            'last_amount_saved':acc_dict[b'last_amount_saved'].decode('utf-8')
        }
        return_string = f"""
=====================================
User: {user_name}

Total Deposit: {summary['total_deposit']}
Pending Settlement: {summary['pending_settlement']}
Total Settlement: {summary['total_settlement']}

Amount Deposited: {summary['amount_deposited']}
Amount Settled: {summary['amount_settled']}

Saving Percentage : 5%
Last Amount Saved: {summary['last_amount_saved']}
Total Amount Saved: {summary['total_amount_saved']}
=====================================
        """
        return return_string.strip()
    else:
        return f"No account summary found for user {user_name}."



def is_valid_yes_or_no(reg_ans):
    """Check if the input is 'yes' or 'no' after converting to lowercase."""
    reg_ans = reg_ans.lower()
    return reg_ans in ["yes", "no"] 

def is_valid_phone_number(phone_ans):
    phone_pattern = re.compile(r'^\d{10,15}$')
    return bool(phone_pattern.match(phone_ans))

def is_valid_paybill(paybill_ans):
    paybill_pattern = re.compile(r'^\d{5,10}$')
    return bool(paybill_pattern.match(paybill_ans))

def is_valid_till(till_ans):
    till_pattern = re.compile(r'^\d{5,10}$')
    return bool(till_pattern.match(till_ans))

def is_valid_payment_amount(payment):
    # Define the regex pattern for a valid payment amount
    pattern = r'^[\$\€\£]?\s*-?\d{1,3}(?:[,.\s]?\d{3})*(?:[.,]\d{1,2})?$'

    # Check if the input matches the pattern
    if re.match(pattern, payment):
        return True
    else:
        return False

def convert_phone_number(byte_phone_number):
    # Decode the byte string to a regular string
    phone_number_str = byte_phone_number.decode('utf-8')
    
    # Ensure the phone number starts with '0' before replacing it
    if phone_number_str.startswith('0'):
        phone_number_str = '254' + phone_number_str[1:]
    
    # Convert the resulting string to an integer
    phone_number_int = int(phone_number_str)
    
    return phone_number_int

# mpesa
@app.route("/mpesa_callback", methods=['POST'])
def process_callback():
    # check if is user cancelled also
    # update task as complete if user input pin
    # also update for settlement as complete
    print(f"recieved data is : {request}, and is of type : {type(request)}")

    in_data = request.get_json()
    print(f"recieved callback data is, {in_data}")

    ref = in_data['MerchantRequestID']
    requested_task = RequestTask.get_task(ref)
    print(f"fetched task is : {requested_task}")
    print("\n\n\n")
    requested_settlement = Settlement.get_customer_settlement(ref)
    print(f"fetched settlement is : {requested_settlement}")
    requested_acc_summary = AccountSummary.get_acc_summary(requested_task['customer_waid'])
    print(f"fetched account summary is : {requested_acc_summary}")
    
    if 'MerchantAccountBalance' in in_data.keys():
        # send-payment callback
        # update task and settlemtnt
        
        print(f"send_payment callback")
        Settlement.complete_customer_settlement(ref)
        RequestTask.complete_task(ref)
        # update acc summarys
        pass
    else:
        # send_user_stk : 0 or 1
        # send_payment()
        if in_data['ResultCode'] == '1032':
            print(f"user has cancelled stk push")
        else:
            end_number = requested_settlement['end_settlement_number']
            payment_amount = requested_settlement['amount']
            payment_amount = payment_amount.decode('utf-8')
            print(f"now settling payment")
            end_number = convert_phone_number(end_number)
            print(f"end_number : {end_number}")
            print(f"payment amount : {payment_amount}")
            # update acc summary, for pending settlements,total settlements , amount settlement, total amount saved and last amount saved

            summary_update = {
                'pending_settlement':0,
                'total_settlement': float(requested_acc_summary[b'total_settlement'].decode('utf-8')) + 1,
                'amount_settled' : float(requested_acc_summary[b'amount_settled'].decode('utf-8')) + float(payment_amount),
                'total_amount_saved':float(requested_acc_summary[b'total_amount_saved'].decode('utf-8')) + float(5),
                'last_amount_saved':float(requested_acc_summary[b'total_amount_saved'].decode('utf-8')) + float(5)

            }

            AccountSummary.update_acc_summary(requested_task['customer_waid'], summary_update)

            send_payment(str(end_number), payment_amount)
            
    
    return 'ok'


@app.route("/mpesa_callback_timeout", methods=['POST'])
def process_callback_timeout():
    print(f"recieved callback data is, {request.get_json()}")

    return 'ok'

@app.route("/test4")
def process_if_up():
    return 'yyup, up'

if __name__ == '__main__':
    with app.app_context():
        # time.sleep(0.5)
        tele_bot.set_webhook(url="https://cb3e-2c0f-2a80-10c8-4f10-a75d-4ae-e94a-e677.ngrok-free.app/telegram")

    app.run(debug=True, port=PORT)
    
# edit notes