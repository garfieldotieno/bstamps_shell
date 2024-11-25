import os
from flask import Flask, request, jsonify
import telebot
from dotenv import load_dotenv
from blu import Session
import string 
import random
import time 
from models import SessionLocal, SlotQuestion
import uuid 
from Markup  import clear_prev_markup, main_markup 
import re 
import json 
import requests
import asyncio
import aiohttp 

load_dotenv()

# Retrieve Telegram bot token from environment variable
BOT_TOKEN = os.getenv('telegram_bot_auth_token')
PORT = int(os.getenv('PORT', 1000))

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

# Sampling menu listing

# MAINMENU
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


# SUB1MENU
authenticate_sub1_menu_listing = [
    {
        'menu_code':'REDEEM-SESSION',
        'media':['https://ibb.co/CmvrRDs'],
        'menu_message':'Redeem menu\n\nProceed by selecting one of the buttons',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'PURCHASE-SESSION',
        'media':['https://ibb.co/pWQ3gxM'],
        'menu_message':'Purchase menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

abt_sub1_menu_listing = [
    {
        'menu_code':'ABOUT-A',
        'media':['https://ibb.co/vvWcvvg'],
        'menu_message':'About menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

search_sub1_menu_listing = [
    {
        'menu_code':'SHOP-A',
        'media':'https://ibb.co/RTTJ7Bq',
        'menu_message':'Search menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'SHOP-B',
        'media':'https://ibb.co/bQfwJwW',
        'menu_message':'Basket menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

upload_sub1_menu_listing = [
    {
        'menu_code':'INVENTORY-A',
        'media':'https://ibb.co/3FvZMKv',
        'menu_message':'Location menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'INVENTORY-B',
        'media':'https://ibb.co/1L13jRZ',
        'menu_message':'Item menu\n\nProceed by selecting one of the buttons',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

referall_sub1_menu_listing = [
    {
        'menu_code':'REFERRAL-A',
        'media':'https://ibb.co/wWVcLM4',
        'menu_message':'New referrals\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'REFERRAL-B',
        'media':'https://ibb.co/Wc23R3M',
        'menu_message':'Act on referrals menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'REFERRAL-C',
        'media':'https://ibb.co/QQYzPCR',
        'menu_message':'Redeem referrals menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

delivery_customer_sub1_menu_listing = [
    {
        'menu_code':'DELIVERY-C-A',
        'media':'https://ibb.co/q5Wbwnr',
        'menu_message':'Drops menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'DELIVERY-C-B',
        'media':'https://ibb.co/zX7m9mn',
        'menu_message':'Drops menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

delivery_vendor_sub1_menu_listing = [
    {
        'menu_code':'DELIVERY_V-A',
        'media':'https://ibb.co/YbkzM11',
        'menu_message':'Pickup menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'DELIVERY_V-B',
        'media':'https://ibb.co/M9pnmh9',
        'menu_message':'Pickup menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

# MENU STACK
menu_stack = {}
menu_stack['main_menu_no_session_listing'] = main_menu_no_session_listing
menu_stack['main_menu_customer_session_listing'] = main_menu_customer_session_listing
menu_stack['main_menu_vendor_session_listing'] = main_menu_vendor_session_listing

menu_stack['authenticate_sub1_menu_listing'] = authenticate_sub1_menu_listing
menu_stack['abt_sub1_menu_listing'] = abt_sub1_menu_listing
menu_stack['search_sub1_menu_listing'] = search_sub1_menu_listing
menu_stack['upload_sub1_menu_listing'] = upload_sub1_menu_listing
menu_stack['referall_sub1_menu_listing'] = referall_sub1_menu_listing
menu_stack['delivery_customer_sub1_menu_listing'] = delivery_customer_sub1_menu_listing
menu_stack['delivery_vendor_sub1_menu_listing'] = delivery_vendor_sub1_menu_listing


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
        try:
            print(f"\n\nstep one : getting the contents from json input \n\n")

            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
        except Exception as e:
            print(f"error t step one : {e}") 

        # Process the update only once
        tele_bot.process_new_updates([update])
        
        if update.message:
            print(f"\n\nstep two : getting messge from update.messge object \n\n")
            try:

                user_id = update.message.from_user.id
                user_name = update.message.from_user.username
                client_input = update.message.text.lower() if update.message.text else ''

                # Print or process the extracted data
                print(f"User ID: {user_id}, Username: {user_name}, Client Input: {client_input}")
                db = SessionLocal()

            except Exception as e:
                print(f"error at step two : {e}")

            if Session.is_first_time_contact(user_id):
                print(f"\n\nstep three calling F_C \n\n")
                print(f"is continuing user")
                
                try:
                    
                    if Session.is_active(user_id):
                        print(f"and user is active")
                        return 'ok'
                    else:
                        print(f"user is not active")
                        if int(Session.is_main_menu_nav(user_id)) == 1:
                            print(f"\n\nis main menu navigation\n\n")


                            if client_input in ["browse", "select", "cancel"]:
                                if client_input == "cancel":
                                    print(f"\n\nmain menu input -- cancel\n\n")
                                    # cancel selected

                                    acc_type = Session.get_session_type(user_id)
                                    
                                    if acc_type == "First":
                                        Session.reset_browsing_count(user_id)
                                        Session.reset_navigation(user_id)

                                        current_count = Session.get_browsing_count(user_id)
                                        menu_payload = main_menu_no_session_listing[current_count]
                                        print(f"current payload after reseting \n\n {menu_payload}")
                                        # Send the message with buttons and media

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                        return 'ok'
                                    
                                    if acc_type == "Customer":
                                        Session.reset_browsing_count(user_id)
                                        Session.reset_navigation(user_id)

                                        current_count = Session.get_browsing_count(user_id)
                                        menu_payload = main_menu_customer_session_listing[current_count]
                                        print(f"current payload after reseting \n\n {menu_payload}")
                                        # Send the message with buttons and media

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                        return 'ok' 

                                    if acc_type == "Vendor":
                                        Session.reset_browsing_count(user_id)
                                        Session.reset_navigation(user_id)

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
                                    print(f"\n\nmain menu input -- select\n\n")

                                    acc_type = Session.get_session_type(user_id)
                                    current_count = Session.get_browsing_count(user_id)
                                    print(f"current count is : {current_count}")

                                    
                                    if acc_type == "First":
                                        
                                        main_menu_select = Session.get_main_menu_select(user_id)
                                        
                                        if main_menu_select in ['ACCOUNT', 'ABOUT'] :

                                            Session.reset_browsing_count(user_id)

                                            if main_menu_select == "ACCOUNT":
                                                Session.on_sub1_menu_nav(user_id, 'authenticate_sub1_menu_listing')
                                                # Session.load_submenu(user_id, 'acc_submenu_listing')

                                                # load
                                                submenu_payload = authenticate_sub1_menu_listing[0]
                                                submenu_message = submenu_payload['menu_message']
                                                submenu_sticker = submenu_payload['menu_sticker']
                                                submenu_media = submenu_payload['media'][0]

                                                tele_bot.send_sticker(user_id, submenu_sticker)
                                                tele_bot.send_photo(user_id, submenu_media)
                                                tele_bot.send_message(user_id, submenu_message)
                                                return 'ok' 

                                            if main_menu_select == "ABOUT":
                                                Session.on_sub1_menu_nav(user_id, 'abt_sub1_menu_listing')
                                                # Session.load_submenu(user_id, 'acc_submenu_listing')

                                                # load
                                                submenu_payload = abt_sub1_menu_listing[0]
                                                submenu_message = submenu_payload['menu_message']
                                                submenu_sticker = submenu_payload['menu_sticker']
                                                submenu_media = submenu_payload['media'][0]

                                                tele_bot.send_sticker(user_id, submenu_sticker)
                                                tele_bot.send_photo(user_id, submenu_media)
                                                tele_bot.send_message(user_id, submenu_message)
                                                return 'ok' 

                                             

                                    if acc_type == "Customer":
                                        pass 
                                    if acc_type == "Vendor":
                                        pass 

                                    return 'ok'

                                if client_input == "browse":
                                    print(f"\n\nmain menu input -- browse\n\n")
                                    
                                    acc_type = Session.get_session_type(user_id)

                                    if acc_type == "First":
                                        Session.browse_main(user_id, len(main_menu_no_session_listing))

                                        current_count = Session.get_browsing_count(user_id)

                                        print(f"check menu type, then load response, with browsing current_count being : {current_count}")
                                    

                                        menu_payload = main_menu_no_session_listing[current_count]
                                        print(f"First : current payload during main browsing \n\n {menu_payload}")

                                        # Send the message with buttons and media

                                        menu_code = menu_payload['menu_code']
                                        Session.update_main_menu_select(user_id, menu_code)

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())

                                        return 'ok' 

                                    if acc_type == "Customer":
                                        Session.browse_main(user_id, len(main_menu_no_session_listing))

                                        current_count = Session.get_browsing_count(user_id)

                                        print(f"check menu type, then load response, with browsing current_count being : {current_count}")
                                    
                                        menu_payload = main_menu_no_session_listing[current_count]
                                        print(f"Customer : current payload during main browsing \n\n {menu_payload}")

                                        # Send the message with buttons and media

                                        menu_code = menu_payload['menu_code']
                                        Session.update_main_menu_select(user_id, menu_code)

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())

                                        return 'ok' 

                                    if acc_type == "Vendor":
                                        menu_payload = main_menu_vendor_session_listing[current_count]
                                        print(f"Vendor : current payload during main browsing \n\n {menu_payload}")
                                        # Send the message with buttons and media

                                        menu_code = menu_payload['menu_code']
                                        Session.update_main_menu_select(user_id, menu_code)

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())

                                        return 'ok'
                                
                                         

                                    
                                    
                        else :
                            print(f"could be sub_menu[1,2] or slot filling")

                            if Session.is_sub1_menu_navigation(user_id):
                                print(f"is sub1 navigation")

                                if client_input in ["browse", "select", "cancel"]:
                                    if client_input == "browse":
                                        sub1_menu_select = Session.get_sub1_menu_select(user_id)
                                        

                                        if sub1_menu_select == 'authenticate_sub1_menu_listing':

                                            browsing_count = Session.get_browsing_count(user_id)

                                            print(f"browsing submenu, select is : {sub1_menu_select}, and browsing count is : {browsing_count}")

                                            sub_menu_count = len(menu_stack[sub1_menu_select])

                                            print(f"sub_menu_count is : {sub_menu_count}")

                                            Session.browse_submain(user_id, sub_menu_count)

                                            current_count = Session.get_browsing_count(user_id)

                                            menu_payload = authenticate_sub1_menu_listing[current_count]
                                            
                                            tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                            sticker_file_id = menu_payload['menu_sticker']
                                            image_link = menu_payload['media'][0]

                                            tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                            tele_bot.send_photo(update.message.chat.id, image_link)
                                            tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                            return 'ok'

                                        if sub1_menu_select == "abt_sub1_menu_listing":

                                            browsing_count = Session.get_browsing_count(user_id)

                                            print(f"browsing submenu, select is : {sub1_menu_select}, and browsing count is : {browsing_count}")

                                            sub_menu_count = len(menu_stack[sub1_menu_select])

                                            print(f"sub_menu_count is : {sub_menu_count}")

                                            Session.browse_submain(user_id, sub_menu_count)

                                            current_count = Session.get_browsing_count(user_id)

                                            print(f"reached here at : {sub1_menu_select}")

                                            menu_payload = abt_sub1_menu_listing[current_count]

                                            tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                            sticker_file_id = menu_payload['menu_sticker']
                                            image_link = menu_payload['media'][0]

                                            tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                            tele_bot.send_photo(update.message.chat.id, image_link)
                                            tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                            return 'ok'

                                    if client_input == "select" :
                                        pass 

                                    if client_input == "cancel" :

                                        print(f"cancelling submenu, cancel")
                                        Session.reset_browsing_count(user_id)
                                        Session.reset_navigation(user_id)

                                        current_count = Session.get_browsing_count(user_id)
                                        session_type = Session.get_session_type(user_id)

                                        if session_type == "First":
                                            menu_payload = main_menu_no_session_listing[current_count]
                                            print(f"current payload after resetting is : {menu_payload}")

                                            tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                            sticker_file_id = menu_payload['menu_sticker']
                                            image_link = menu_payload['media'][0]

                                            tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                            tele_bot.send_photo(update.message.chat.id, image_link)
                                            tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                            return 'ok'
                                             
                                         

                                     
                                else:
                                    print(f"sub1_menu navigation input warning") 
                                    return_message = "please use the buttons below to proceed"
                                    tele_bot.send_message(user_id, return_message)
                                    return 'ok'
                            

                            if Session.is_sub2_menu_navigation(user_id):
                                print(f"is sub2 navigation")
                                pass
                            

                            return 'ok'
                
                    
                except Exception as e:
                    print(f"error at step three : {e}")
            else:
                print(f"\n\nstep four : calling A\n\n")
                try:
                        
                    print(f"is user first time, creating session")

                    new_count = 0

                    if client_input:
                        print(f"\n\nstep five, creating user session \n\n")

                        try:


                            print(f"starting to process first input, /start")

                            new_user_session = Session(
                            uid=generate_uid(),
                            waid=user_id,
                            name=user_name,

                            current_menu_code='',
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
                            slot_quiz_count='',

                            current_slot_handler='',
                            session_active=0,
                            session_type='First'
                            )

                            new_user_session.save() 
                            # ommitting account summary
                            current_count = Session.get_browsing_count(user_id)

                            menu_payload = main_menu_no_session_listing[current_count]
                            print(f"current menu payload : {menu_payload}")

                            menu_message = menu_payload['menu_message']
                            menu_code = menu_payload['menu_code']

                            Session.update_main_menu_select(user_id, menu_code)

                            tele_bot.send_chat_action(update.message.chat.id, 'typing')
                            sticker_file_id = menu_payload['menu_sticker']
                            image_link = menu_payload['media'][0]

                            tele_bot.send_sticker(update.message.chat.id, sticker_file_id)

                            tele_bot.send_photo(update.message.chat.id, image_link)

                            tele_bot.send_message(user_id, menu_message, reply_markup=main_markup())

                            return 'ok'
                        
                        except Exception as e:
                            print(f"error at step five : {e}")
                
                except Exception as e:
                    print(f"error at step four : {e}")
        
        
        else:
            return 'ok'

                
    else:
        return 'invalid request', 403













@app.route('/test_box_endpoint', methods=['POST'])
def process_client_input():
    try:
        data = request.get_json()
        print(f"\n\n recieved data is  : {data}\n\n and keys are : {data.keys()}")
        user_id  = data["message"]["from_user"]["id"]
        user_name = data["message"]["from_user"]["user_name"]
        client_input = data["message"]["from_user"]["text"].lower() if data["message"]["from_user"]["text"] else ''
        print(f"\n\n user id : {user_id} \n\n user_name :{user_name}  \n\n client_input : {client_input}")
        
        if Session.is_first_time_contact(user_id):
            print(f"user is continuing user")
            print(f"calling for auth session creation")

            current_count = Session.get_browsing_count(user_id)

            menu_payload =  main_menu_no_session_listing[current_count]

            print(f"\n\n current bot output payload is : {menu_payload}")


            return jsonify(menu_payload)
        else:
            print(f"new user")
            new_count = 0
            new_user_session = Session(
                uid=generate_uid(),
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
                slot_quiz_count='',

                current_slot_handler='',
                session_active=0,
                session_type='First' 
            )

            new_user_session.save()

            current_count = Session.get_browsing_count(user_id)

            menu_payload = main_menu_no_session_listing[current_count]
            
            menu_message = menu_payload['menu_message']
            menu_code = menu_payload['menu_code']

            Session.update_main_menu_select(user_id, menu_code)

            print(f"\n\n current bot output payload is : {menu_payload}")

            return jsonify(menu_payload)
    
    except Exception as e:
        print(f"error : {e}")

        return 'ok'
    
    
    
if __name__ == '__main__':
    with app.app_context():
        # time.sleep(0.5)
        tele_bot.set_webhook(url="https://mutually-advanced-pegasus.ngrok-free.app/telegram")

    app.run(debug=True, port=1000)