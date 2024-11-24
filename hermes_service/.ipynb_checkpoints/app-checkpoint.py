import os
from flask import Flask, request
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
        'media':'https://ibb.co/CmvrRDs',
        'menu_message':'Redeem menu\n\nProceed by selecting one of the buttons',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    },
    {
        'menu_code':'PURCHASE-SESSION',
        'media':'https://ibb.co/pWQ3gxM',
        'menu_message':'Purchase menu\n\nProceed by selecting one of the buttons below',
        'menu_sticker':'CAACAgIAAxkBAAIE7mZy7_qRkDcbEmP3mGwAAeHd3qfyggACNAADwZxgDP8a5OfWWHRQNQQ'
    }
]

abt_sub1_menu_listing = [
    {
        'menu_code':'ABOUT-A',
        'media':'https://ibb.co/vvWcvvg',
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
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)

        # Process the update only once
        tele_bot.process_new_updates([update])
        
        return 'ok'
    else:
        return 'invalid request', 403


if __name__ == '__main__':
    with app.app_context():
        # time.sleep(0.5)
        tele_bot.set_webhook(url="https://b6f7-2c0f-2a80-10c8-4f10-7367-51a-b09d-3187.ngrok-free.app/telegram")
    app.run(debug=True, port=PORT)