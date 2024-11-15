import telebot
from api_master import config, BluMarkup
#import api_master.payments as payments
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
    blu.send_chat_action(message.chat.id, 'typing')
    blu.send_message(message.chat.id, "Sure!", reply_markup=BluMarkup.clear_prev_markup())
    local_host = f'{os.getcwd()}/static/bot_media/wake_up_small.gif'
    img = open(local_host, 'rb')
    blu.send_document(message.chat.id, data=img)
    blu.send_message(message.chat.id, "What would you like to do?", reply_markup=BluMarkup.start_one_markup())


@blu.message_handler(func=lambda message: True)  # This handler will catch all message types
def handle_all_messages(message):
# check content type and print message
    print(f"context type is, {message.content_type}")


# def handle photo message
def handle_photo_message(message):
    # print message
    print(f"handling photo, data recieved here {message}")
    # get the file id of the photo
    photo_id = message.photo[-1].file_id

    # Send the received photo back as a response
    blu.send_photo(message.chat.id, photo_id)

    # ... Your other code ...


def handle_text_message(message):
    # Your logic to handle text messages goes here
    blu.send_message(message.chat.id, f"You sent a text message: {message.text}")

def handle_location_message(message):
    # Your logic to handle location messages goes here
    latitude = message.location.latitude
    longitude = message.location.longitude
    blu.send_message(message.chat.id, f"You shared your location. Latitude: {latitude}, Longitude: {longitude}")

def handle_document_message(message):
    # Your logic to handle document messages goes here
    blu.send_message(message.chat.id, "You sent a document.")


def handle_sticker_message(message):
    # print message
    print(f"handling sticker, data recieved here {message}")
    sticker_id = message.sticker.file_id

    # Send the received sticker back as a response
    blu.send_sticker(message.chat.id, sticker_id)

    # ... Your other code ...

@blu.message_handler(commands=['share_location'])
def share_location(message):
    # Create a custom keyboard with a "Share Location" button
    custom_keyboard = [['Share Location']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)

    # Send a message with the custom keyboard
    blu.send_message(message.chat.id, "Please share your location:", reply_markup=reply_markup)


@blu.message_handler(func=lambda message: message.text == 'Share Location')
def handle_share_location(message):
    # Check if the message contains location data
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        # Use the send_location method to send the location back to the user
        blu.send_location(message.chat.id, latitude, longitude)

    else:
        # If the message does not contain location data, inform the user
        blu.send_message(message.chat.id, "Sorry, I couldn't retrieve your location. Please try again.")


