from platform import platform
from flask import Flask, json, render_template, request, abort, redirect, make_response, url_for, session, send_file, jsonify, send_file
from flask_restful import Api,Resource
from api_master import config, np, cv2, datetime, timedelta
import uuid
from api_master.BaseBotModule import BaseBot
import hashlib

# from api_master.Mk40BotModule import jarvis
from api_master.BluBotModule import blu
# from api_master.Mk41BotModule import herby 

from werkzeug.utils import secure_filename

from functools import wraps

from flask_cors import  CORS

from api_master.philate import secrets, generate_qrcode_image, generate_transaction_card, generate_big_card, generate_receipt, decode_qr_code, calculate_file_hash
import telebot
from api_master.BaseBotModule import yaml

from api_master.models import Item, Transaction, Payment, Order, Task, Geo, UserSessionProfile, Card
from api_master.new_models import Location, Auth

from api_master.db import base_bot_db, Session
from api_master.new_models import Auth


import time
import os
import io 

platform_api = Flask(__name__)
platform_api.secret_key = b"Z'(\xac\xe1\xb3$\xb1\x8e\xea,\x06b\xb8\x0b\xc0"

api = Api(platform_api)



UPLOAD_FOLDER = os.path.abspath('./static/media_store')
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])
platform_api.config['UPLOADER_FOLDER'] = UPLOAD_FOLDER
# 10 mb max for upload
platform_api.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 
def allowed_file(filename):
    return filename[-3:].lower() in ALLOWED_EXTENSIONS


@platform_api.template_filter()
def numberFormat(value):
    return format(int(value), 'd')

CORS(platform_api)



# Define the GeneralMiddleware class
class GeneralMiddleware:

    __swatsika_master_id_list = ['821320826']

    def __init__(self):
        self.routes_requiring_authorization = [
            '/',
            '/web_bot',
            '/rest_bot',
            f"/{config.mk41_config['WEBHOOK_URL_PATH']}",
            f"/{config.blu_config['WEBHOOK_URL_PATH']}",
            f"/{config.mk40_config['WEBHOOK_URL_PATH']}"
            ]
        
            
    def check_route_group(self):
        if request.path == '/' :
            return 'web_bot'
        elif request.path == '/web_bot':
            return 'web_bot'
        elif request.path == '/rest_bot':
            return 'rest_bot'
        elif request.path == f"/{config.mk41_config['WEBHOOK_URL_PATH']}":
            return 'tel_bot'
        elif request.path == f"/{config.blu_config['WEBHOOK_URL_PATH']}":
            return 'tel_bot'
        elif request.path == f"/{config.mk40_config['WEBHOOK_URL_PATH']}":
            return 'tel_bot'
        else:
            return 'unknown_bot'
    

    def dump_request(self):
        # show all content in the request object
        print(f" request path : {request.path}")
        print(f" request method : {request.method}")
        print(f" request headers : {request.headers}")
        print(f" request cookies : {request.cookies}")
        print(f" request data : {request.data}")
        print(f" request form : {request.form}")
        print(f" request files : {request.files}")
            
        print(f" request args : {request.args}")
        print(f" request values : {request.values}")
        print(f" request endpoint : {request.endpoint}")
        print(f" request full_path : {request.full_path}")
        print(f" request host : {request.host}")
        print(f" request host_url : {request.host_url}")
        print(f" request path : {request.path}")
        print(f" request query_string : {request.query_string}")
        print(f" request referrer : {request.referrer}")
        print(f" request remote_addr : {request.remote_addr}")
        print(f" request scheme : {request.scheme}")
        print(f" request url : {request.url}")
        print(f" request url_root : {request.url_root}")
        print(f" request user_agent : {request.user_agent}")
        print(f" request blueprint : {request.blueprint}")
        print(f" request max_content_length : {request.max_content_length}") 
        print(f" request max_form_memory_size : {request.max_form_memory_size}")
        
        print(f" request is_secure : {request.is_secure}")
        
        print(f" request is_multiprocess : {request.is_multiprocess}")
            
                      

        # Dump the HTTP-only cookie value
        print("HTTP-only Cookie Value: ", request.cookies.get('user_data'))
        # Dump the session cookie value
        print("Session Cookie Value: ", request.cookies.get('session'))
        # Dump the CSRF cookie value
        print("CSRF Cookie Value: ", request.cookies.get('csrf_token'))                                                                                             


    def get_telegram_id_from_request(self,request_json):
        try:
            print(f"recievd data for telegram at middleware, {request_json}")
            telegram_id = request_json['message']['from']['id']
            return telegram_id
        except Exception as e:
            print(f"Error parsing Telegram ID: {str(e)}")
            return None

    def create_telegram_session(self, telegram_id):
        session_data = {
            'uid': telegram_id,
            'session_type': 'Regular',
            'session_duration':time.time() + 3600,
            'is_authorized': False,
            'bot_type': 'Tel_Bot',
            'activity_json': {
                'contact':0,
                'slot_filling': False,
                'acceptable_intent_input' : ['Check-in', 'Refresh', 'Call', 'Mail', 'About'],
                'current_input': None,
                'current_intent': None,
                'updated_list':[]
            },
            'response_json': {
                'data': {
                    'current_resource': 'Item',
                },
                'current_bot_buttons':['Browse', 'Select', 'Cancel'],
                'current_bot_screen_media':[],
                'current_bot_Header':[]
            }
        }
        session_data = UserSessionProfile(**session_data)
        session_data.save()
        return session_data
    

    def create_web_session(self, session_uid):
        session_data = {
            'uid': session_uid,
            'session_type': 'Regular',
            'session_duration':time.time() + 3600,
            'is_authorized': False,
            'bot_type': 'Web_Bot',
            'activity_json': {
                'contact':0,
                'slot_filling':False,
                'acceptable_intent_input':['Check-in', 'Refresh', 'Call', 'Mail', 'About'],
                'current_input':None,
                'current_intent': None,
                'updated_card_list':[]
            },

            'response_json': {
                'data':{
                    'current_resource':'Item',
                },
                'session_swap':False,
                'session_swap_data':{},
                'current_bot_buttons':[({"label":'Check-in', "icon":'fa fa-qrcode'}, {"label":'Refresh', "icon":'fa fa-refresh'}), ({"label":'Call', "icon":'fa fa-phone'}, {"label":'Mail', "icon":'fa fa-envelope'}, {"label":'About', "icon":'fa fa-info-circle'})],
                'current_bot_screen_media':['static/bot_media/wake_up_big.gif', 'static/bot_media/wake_up_small.gif'],
                'current_bot_header':[]
            }
        }
        session_data = UserSessionProfile(**session_data)
        session_data.save()
        return session_data

    
    def generate_auth_card(self,lookup_data):
        print(f"generating auth card from GeneralMiddleWare")
        json_data = lookup_data
        new_code = uuid.uuid4().hex[:4].upper()

        hashed_code = hashlib.sha256(new_code.encode()).hexdigest()

        rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()


        card_data = {}
        card_data['session_data'] = {}
        card_data['print_data'] = {}
        card_data['verify_data'] = {}


        card_data['session_data']['card_type'] = "Auth_Card"
        card_data['session_data']['level'] = 1
        card_data['session_data']['session_type']= json_data['payload']['session_data']['session_type']
        card_data['session_data']['redeem_code']= True
        card_data['session_data']['redeem_code_value']= hashed_code
        card_data['session_data']['duration_in_seconds'] = 60*60
        card_data['session_data']['active_days'] = 7


        card_data['print_data']['item_media_plate_url'] = 'static/media_store/session_plates/plate_session_full_centerd.jpg'
        card_data['print_data']['heading'] = 'Auth'
        card_data['print_data']['sub_heading'] = 'Sub_heading'
        card_data['print_data']['indicator'] = "Au"

        card_data['created_at'] = time.asctime(time.localtime(time.time()))

        print(f'received payload data is: {json_data}')
        

        if rehashed_code == hashed_code:
            print("Generated Verification Code successful.")
            res = generate_qrcode_image(card_data)
            final_res = generate_big_card(res[0], res[1])
            final_res['new_code'] = new_code

            if final_res['status']:
                image_path = final_res['url']
                # return send_file(image_path, mimetype='image/jpeg')
                return final_res
            else:
                print(f"logging final_res => {final_res}")
                return {'status': False, 'message': 'Failed to generate ticket image', 'final_res': {final_res}}
             
        else:
            message = "Generated Code Verification Failed"
            print(message)
            return {'status': False, 'message': message}

        
        
    def swap_web_session_init(self,lookup_data):
        init_web_uid = request.cookies.get('user_data')
        curr_sess = UserSessionProfile.get(init_web_uid)
        if curr_sess is None:
            return {"status":False, "message":"unable to fetch user session"}
        try:
            payload = {"init_web_uid":init_web_uid, "card_uid":lookup_data['uid']}
            payload["session_data"] = lookup_data["payload"]["session_data"]
            payload['session_swap_complete'] = False
            curr_sess.update_response_json_session_swap(True, payload)
            return {"status":True, "message":"session_wap triggered"}

        except Exception as e:
            return {"status":False, "message":"error => {e}"}


    def revert_swap_web_init(self):
        init_web_uid = request.cookies.get('user_data')
        curr_sess = UserSessionProfile.get(init_web_uid)
        if curr_sess is None:
            return {"status":False, "message":"unable to fetch user session"}
        try:
            
            curr_sess.update_response_json_revert_session_swap()
            return {"status":True, "message":"session_wap reverted"}

        except Exception as e:
            return {"status":False, "message":"error => {e}"}


    def complete_swap_web_session(self):
        init_web_uid = request.cookies.get('user_data')
        curr_sess = UserSessionProfile.get(init_web_uid)
        if curr_sess is None:
            return {"status":False, "message":"unable to fetch user session"}
        try:
            
            curr_sess.complete_session_swap()
            return {"status":True, "message":"session_wap comlpete"}

        except Exception as e:
            return {"status":False, "message":"error => {e}"}
         
        
    def before_first_request(self):
        if request.path in self.routes_requiring_authorization:
            print(f"===== processing very_first_request")
            print(f"should log this event to the redis db")
            print("HTTP-only Cookie Value: ", request.cookies.get('user_data'))
                   
                   
    def before_request(self):
        if request.path in self.routes_requiring_authorization:
            print(f"===== processing before_request")
            print(f" request path : {request.path}")
                    # Iterate through the request arguments
            print(" request args:")
            for key, value in request.args.items():
                print(f"    {key}: {value}")

            # Iterate through the request values
            print(" request values:")
            for key, value in request.values.items():
                print(f"    {key}: {value}")

            print(f"\n\n")
            print(f" request form : {request.form}")
            
            print(f"should check session status and update where needs bee")
            print(self.check_route_group())
            

    def after_request(self, response):
        if request.path in self.routes_requiring_authorization:
            print(f"===== processing after_request")
            print(f"processes the response by just returning it as is")
            # print response object
            print(f"response status : {response.status}")
            
                
             
        return response
    

# Register the middleware function with the hooks
platform_api.before_first_request(GeneralMiddleware().before_first_request)
platform_api.before_request(GeneralMiddleware().before_request)
platform_api.after_request(GeneralMiddleware().after_request)


# Web_bot endpoint
# Rest_bot endpoint
@platform_api.route('/clear_generated_card', methods=['POST'])
def clear_generated_card():
    json_data = request.get_json()
    print(f'recieved json data is : {json_data}')
    try:
        os.remove(f"{json_data['receipt_url']}")
        return {'status':True}
    except Exception as e:
        print(f"unable to delete the requested url because => {e}")
        return {'status':False}



# Web_bot endpoint
# Rest_bot endpoint
@platform_api.route('/request_item_insta_card', methods=['POST'])
def process_item_insta_card():
    json_data = request.get_json()
    print(f'recieved json data is : {json_data}')

    if json_data['session_data']['redeem_code']:
        # Generating a random 4-character hexadecimal string
        new_code = uuid.uuid4().hex[:4].upper()

        
        # Hashing the generated code
        hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
        print(f"new code : {new_code} and hashed_code : {hashed_code} ")

        # Replace the provided value with the hashed code
        json_data['session_data']['redeem_code_value'] = hashed_code

        # To verify, you can re-hash the new code and compare it with the stored hashed value
        rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()

        if rehashed_code == hashed_code:

            print("Generated Verification Code successful.")
            res = generate_qrcode_image(json_data)
            final_res = generate_big_card(res[0], res[1])
            final_res['new_code'] = new_code

            if final_res['status']:
                image_path = final_res['url']
                return jsonify(final_res)
            else:
                return jsonify({'status': False, 'message': 'Failed to generate card image'})

        else:

            message = "Generated Code Verification  failed"
            print(message)
            return jsonify({'status': False, 'message': message})



# Web_bot endpoint
# Rest_bot endpoint
@platform_api.route('/request_order_transaction_card', methods=['POST'])
def process_transaction_card():
    json_data = request.get_json()
    print(f'recieved json data is : {json_data}')

    if json_data['session_data']['redeem_code']:
        # Generating a random 4-character hexadecimal string
        new_code = uuid.uuid4().hex[:4].upper()

        
        # Hashing the generated code
        hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
        print(f"new code : {new_code} and hashed_code : {hashed_code} ")

        # Replace the provided value with the hashed code
        json_data['session_data']['redeem_code_value'] = hashed_code

        # To verify, you can re-hash the new code and compare it with the stored hashed value
        rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()

        if rehashed_code == hashed_code:
            print("Generated Verification Code successful.")
            res = generate_qrcode_image(json_data)
            final_res = generate_transaction_card(res[0], res[1])
            final_res['new_code'] = new_code

            if final_res['status']:
                image_path = final_res['url']
                return jsonify(final_res)
            else:
                return jsonify({'status': False, 'message': 'Failed to generate card image'})

        else:
            message = "Generated Code Verification  failed"
            print(message)
            return jsonify({'status': False, 'message': message})



# Web_bot endpoint
# Rest_bot endpoint
@platform_api.route('/request_receipt', methods=['POST'])
def process_receipt():
    json_data = request.get_json()
    print(f'recieved json data is : {json_data}')

    if json_data['session_data']['redeem_code']:
        # Generating a random 4-character hexadecimal string
        new_code = uuid.uuid4().hex[:4].upper()

        
        # Hashing the generated code
        hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
        print(f"new code : {new_code} and hashed_code : {hashed_code} ")

        # Replace the provided value with the hashed code
        json_data['session_data']['redeem_code_value'] = hashed_code

        # To verify, you can re-hash the new code and compare it with the stored hashed value
        rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()

        if rehashed_code == hashed_code:
            print("Generated Verification Code successful.")
            res = generate_qrcode_image(json_data)
            final_res = generate_receipt(res[0], res[1])
            final_res['new_code'] = new_code

            if final_res['status']:
                image_path = final_res['url']
                return jsonify(final_res)
            else:
                return jsonify({'status': False, 'message': 'Failed to generate card image'})

        else:
            message = "Generated Code Verification  failed"
            print(message)
            return jsonify({'status': False, 'message': message})



# Web_bot endpoint
# Rest_bot endpoint
@platform_api.route('/request_auth_reset_card', methods=['POST'])
def process_auth_reset_card():
    json_data = request.get_json()
    print(f'recieved json data is : {json_data}')

    if json_data['session_data']['redeem_code']:
        # Generating a random 4-character hexadecimal string
        new_code = uuid.uuid4().hex[:4].upper()

        
        # Hashing the generated code
        hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
        print(f"new code : {new_code} and hashed_code : {hashed_code} ")

        # Replace the provided value with the hashed code
        json_data['session_data']['redeem_code_value'] = hashed_code

        # To verify, you can re-hash the new code and compare it with the stored hashed value
        rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()

        if rehashed_code == hashed_code:
            print("Generated Verification Code successful.")
            res = generate_qrcode_image(json_data)
            final_res = generate_big_card(res[0], res[1])
            final_res['new_code'] = new_code

            if final_res['status']:
                image_path = final_res['url']
                return jsonify(final_res)
            else:
                return jsonify({'status': False, 'message': 'Failed to generate card image'})

        else:
            message = "Generated Code Verification  failed"
            print(message)
            return jsonify({'status': False, 'message': message})

    

# Web_bot endpoint
# Rest_bot endpoint
@platform_api.route('/recognize_artifact', methods=['POST'])
def recognize_card():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Get the input value submitted from the JS counterpart
    user_input = request.form.get('userInput')  # Assuming 'userInput' is the key used to send the input value
    

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        file_path = f'/tmp/uploaded_artifact.jpg'
        
        image = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        decode_status = decode_qr_code(image)
        
        if decode_status['status']:
            # Rest of your code remains the same
            print("recognized")
            print(type(decode_status['message']))

            decoded_list = decode_status['message']

            if len(decoded_list) > 0:
                hash_key = decoded_list[0][0].decode('utf-8')
                print(f"hash_key => {hash_key}")
           
                card = Card.get(hash_key)

                if card:
                    lookup_data = card.dict()
                    print(f"testing dump on lookup_data : {lookup_data['payload']}")
                else:
                    message = "unable to retrieve card data"
                    return jsonify({"status" : False, "message":message})

                if user_input:
                    print(f"recieved user input {user_input}")

                    hashed_input = hashlib.sha256(user_input.encode()).hexdigest()  # You can use a suitable hashing algorithm
                    print(f"calculated hash from user_input , {hashed_input}")

                    redeem_hash = lookup_data['payload']['session_data']['redeem_code_value']
                    print(f"redeem_hash, {redeem_hash}, and type is {type(redeem_hash)}")

                    if hashed_input == redeem_hash:
                        # Proceed with the rest of your logic
                        print('User input matches the hashed value.')

                        # check session data
                        retrieved_session_data = lookup_data['payload']['session_data']
                        print(f"Card Type : {retrieved_session_data['card_type']} and Session Type: {retrieved_session_data['session_type']}")

                        if retrieved_session_data['level'] == 0:
                            print('level 0 artifact')

                            if retrieved_session_data['card_type'] == "Auth_Reset_Card":
                                print('level 0 artifact')
                                res = GeneralMiddleware().generate_auth_card(lookup_data)
                                swap_status = GeneralMiddleware().swap_web_session_init(lookup_data)


                                return jsonify(
                                    {"status":swap_status['status'], 
                                    "message":swap_status['message'], 
                                    "auth_card_gen":res,
                                    "card_operation": retrieved_session_data['card_type']
                                    })
                            
                            else:
                                print("Non auth reset card") 
                                return jsonify(lookup_data)
                            

                        elif retrieved_session_data['level'] == 1:
                            print('level 1 artifact')
                            print('attempting binary verification')
                            file.save(file_path)
                            ver_status = calculate_file_hash(file_path)

                            if ver_status['status']:
                                print(f"calculated file_hash is => {ver_status['message']}")

                                if retrieved_session_data['card_type'] == "Auth_Card":
                                    swap_status = GeneralMiddleware().swap_web_session_init(lookup_data)
                                    
                                    return jsonify(
                                        {"status":swap_status['status'], 
                                        "message":swap_status['message'],
                                        "card_operation": retrieved_session_data['card_type']
                                        })

                            else:
                                print("unable to calculate the received artifact's hash")
                                return jsonify({'error': 'Unable to calculate the received artifact\'s hash'})                       
                    
                    else:
                        message = 'User input does not match the hashed value.'
                        print(message)
                        return jsonify({'status':False, "message": message})
                else:
                    message = f"no user input recieved, {user_input}"
                    print(message)
                    return jsonify({'status':False, "message": message})

            else:
                message = 'No QR code found in the image'
                return jsonify({'status':False, "message": message})
        else:
            message = 'QR code not recognized'
            return jsonify({'status':False, "message": message})
            
    
    os.remove(file_path)
    message = "invalide file format"
    return jsonify({'status':False, "message": message})



# Tel_bot Blu_bot endpoint
@platform_api.route(f"/{config.blu_config['WEBHOOK_URL_PATH']}", methods=['POST'])
def process_blu_webhook():
    telegram_id = GeneralMiddleware().get_telegram_id_from_request(request.json)
    print(f"fetching telgram_id, {telegram_id}")
    redis_session = UserSessionProfile.get(telegram_id)
    if redis_session is None:
        print(f"redis session for telegram id not present, creating")
        GeneralMiddleware().create_telegram_session(telegram_id)
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        blu.process_new_updates([update])
        print(blu.next_step_handlers)
        return ''
    else:
        print(f"redis session for telegramid present => {redis_session.dict()}")
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        blu.process_new_updates([update])
        print(blu.next_step_handlers)
        return ''


# Tel_bot Mk41_bot endpoint    
# @platform_api.route(f"/{config.mk41_config['WEBHOOK_URL_PATH']}", methods=['POST'])
# def process_herby_webhook():
#     telegram_id = GeneralMiddleware().get_telegram_id_from_request(request.json)
#     print(f"fetching telgram_id, {telegram_id}")

#     if telegram_id == 821320826:
#         print(f"authorized user")
#         redis_session = UserSessionProfile.get(telegram_id)

#         if redis_session is None:
#             print(f"redis session for telegram id not present, creating")
#             GeneralMiddleware().create_telegram_session(telegram_id)
#             json_string = request.get_data().decode('utf-8')
#             update = telebot.types.Update.de_json(json_string)
#             herby.process_new_updates([update])
#             print(herby.next_step_handlers)
#             return ''
#         else:
#             print(f"redis session for telegram id present => {redis_session.dict()}")
#             json_string = request.get_data().decode('utf-8')
#             update = telebot.types.Update.de_json(json_string)
#             herby.process_new_updates([update])
#             print(herby.next_step_handlers)
#             return ''
    
#     else:
#         print(f"non-authorized user")
#         return ''


# Web_bot endpoint
# check for data if post
@platform_api.route('/web_bot', methods=['POST'])
def process_web_bot():
    print(f"Posted request from web_bot")
    if request.method == 'POST':
        content_type = request.headers.get('Content-type')
        if content_type == 'application/json':
            json_data = request.json
            print(f'Received JSON data: {json_data}')
            # Process JSON data here
        elif content_type == 'application/x-www-form-urlencoded':
            # Handle form data if needed
            form_data = request.form
            print(f'Received form data: {form_data}')
            # Process form data here
        else:
            return {'status': False, 'message': 'Error, unsupported data format!'}

        # Continue processing based on the data type received

    else:
        return {'status': False, 'message': 'Error, unsupported HTTP method!'}

    # Return a response if needed
    return {'status': True, 'message': 'Data received and processed successfully'}


# Web_bot get endpoint
@platform_api.route('/web_bot', methods=['GET'])
def process_web_bot_get():
    return redirect(url_for('index'))

@platform_api.route('/favicon.ico')
def favicon():
    return '' 

# Web_bot endpoint
@platform_api.route('/' , methods=['GET'])
def index():
    print(f"======now-processing-index-view-request=======")
    cookie_id = request.cookies.get('user_data')
    print(f"checking cookie_id at / {cookie_id}")

    # section A
    redis_session = UserSessionProfile.get(request.cookies.get('user_data'))
    if redis_session is None:
        print(f"session in redis, not present")
        session_uid = str(uuid.uuid4())
        GeneralMiddleware().create_web_session(session_uid)
        redis_session2 = UserSessionProfile.get(session_uid)

        # redis_session2.count_activity()
        
        # Z0
        print(f"calling z0")
        print(f"created rd_session => {redis_session2.dict()}")
        bot_view_data = redis_session2.dict()['response_json']
        resource_data = Item.get_all()
        print(f"fetched bot_view_data button_stack_1 => \n {bot_view_data['current_bot_buttons'][0]} \n\n button_stack_2 {bot_view_data['current_bot_buttons'][1]} \n\n")
        response = make_response(render_template('web_bot.html', session_data=redis_session2.dict(), resource_data=resource_data, bot_view=bot_view_data))
        
        session_duration = time.time() + 3600
        response.set_cookie('user_data', session_uid, httponly=True, expires=session_duration)
        return response

    else:
        request_args = request.args 
        if len(request_args) == 0:
            # check current_intent at redis_store
            redis_session.count_activity()
            current_intent = redis_session.activity_json['current_intent']
            

            if redis_session.dict()['activity_json']['slot_filling']:
                print(f"slot-filling happening here")

                return f"current intent is {current_intent}"
                 

            else:
                
                message = f"no slot filling happening here, current int {current_intent}"
                print(message)  

                # Z1Abase
                print(f"calling z1abase")
                print(f"fetched rd_session => {redis_session.dict()}")

                
                if redis_session.session_type == "Developer":
                    return redirect('/dev')
                
                if redis_session.session_type == "Admin":
                    return redirect('/admin')
                
                if redis_session.session_type == "Regular":
                    bot_view_data = redis_session.dict()['response_json']
                    resource_data = Item.get_all()
                    response = make_response(render_template('web_bot.html', session_data=redis_session.dict(), resource_data=resource_data, bot_view=bot_view_data))
                    return response
                        
                    
        # section C             
        else:
            print(f"no slot-filling happening here")                
            current_intent = request_args['intent']
                    
            if current_intent == 'Landing_page':
                redis_session.update_activity_intent(current_intent)
                payload = [({"label":'Check-in', "icon":'fa fa-qrcode'}, {"label":'Refresh', "icon":'fa fa-refresh'}), ({"label":'Call', "icon":'fa fa-phone'}, {"label":'Mail', "icon":'fa fa-envelope'}, {"label":'About', "icon":'fa fa-info-circle'})]
                redis_session.update_response_json_buttons(payload)
                return redirect('/')

            elif current_intent == "Cancel":
                redis_session.update_activity_intent('Landing_page')
                payload = [({"label":'Check-in', "icon":'fa fa-qrcode'}, {"label":'Refresh', "icon":'fa fa-refresh'}), ({"label":'Call', "icon":'fa fa-phone'}, {"label":'Mail', "icon":'fa fa-envelope'}, {"label":'About', "icon":'fa fa-info-circle'})]
                redis_session.update_response_json_buttons(payload)
                return redirect('/')

            elif current_intent == "Refresh":
                redis_session.update_activity_intent('Landing_page')
                payload = [({"label":'Check-in', "icon":'fa fa-qrcode'}, {"label":'Refresh', "icon":'fa fa-refresh'}), ({"label":'Call', "icon":'fa fa-phone'}, {"label":'Mail', "icon":'fa fa-envelope'}, {"label":'About', "icon":'fa fa-info-circle'})]
                redis_session.update_response_json_buttons(payload)
                return redirect('/')
                     
            elif current_intent == 'About':
                redis_session.update_activity_intent(current_intent)
                payload = [
                    {
                        'label': 'Introduction',
                        'paragraph':'Welcome to Wowza.Africa, your one-stop destination for seamless online services. At Wowza.africa, we are dedicated to providing you with a revolutionary online experience, redefining the way you search, purchase, create, and receive deliveries. Our cutting-edge bot platform is designed to streamline your online transactions, making the entire process smooth and hassle-free.',
                        'lottie_url': "https://assets6.lottiefiles.com/packages/lf20_OKry2Fjrb9.json"
                    },
                    {
                        'label': 'Setup',
                        'paragraph':"Headquartered in the bustling city of Nairobi, Kenya, we are strategically located at the heart of innovation and technological advancement in Africa. Our platform has been meticulously crafted to cater to the needs of the modern urban population, offering an intuitive and user-friendly interface that resonates with the dynamic lifestyle of today's youth.",
                        'lottie_url': "https://assets6.lottiefiles.com/packages/lf20_7fy2yzzs.json"
                    },
                    {
                        'label': 'Payoff',
                        'paragraph':"At Wowza.Africa, we pride ourselves on delivering convenience and efficiency right to your fingertips. With our unique transaction artifacts and cards, we ensure that your checkout and check-in activities across multiple channels, including websites, social media pages, and chat bots, are effortlessly managed. Embrace the future of online services with Wowza.africa and experience a new level of digital empowerment that simplifies your life.",
                        'lottie_url': "https://assets4.lottiefiles.com/packages/lf20_ofa3xwo7.json"
                    }
                ]
                redis_session.update_response_json_data(payload)
                payload2 = [({"label":'Check-in', "icon":'fa fa-qrcode'}, {"label":'Refresh', "icon":'fa fa-refresh'}), ({"label":'Call', "icon":'fa fa-phone'}, {"label":'Mail', "icon":'fa fa-envelope'}, {"label":'About', "icon":'fa fa-info-circle'})]
                redis_session.update_response_json_buttons(payload2)
                return redirect('/')

            elif current_intent == "Call":
                redis_session.update_activity_intent(current_intent)
                payload = [({"label":'Check-in', "icon":'fa fa-qrcode'}, {"label":'Refresh', "icon":'fa fa-refresh'}), ({"label":'Call', "icon":'fa fa-phone'}, {"label":'Mail', "icon":'fa fa-envelope'}, {"label":'About', "icon":'fa fa-info-circle'})]
                redis_session.update_response_json_buttons(payload)
                return redirect('/')

            elif current_intent == "Mail":
                redis_session.update_activity_intent(current_intent)
                payload = [({"label":'Check-in', "icon":'fa fa-qrcode'}, {"label":'Refresh', "icon":'fa fa-refresh'}), ({"label":'Call', "icon":'fa fa-phone'}, {"label":'Mail', "icon":'fa fa-envelope'}, {"label":'About', "icon":'fa fa-info-circle'})]
                redis_session.update_response_json_buttons(payload)           
                return redirect('/')

            elif current_intent == "Check-in":
                redis_session.update_activity_intent(current_intent)
                payload = [({'label':'Upload', 'icon':'fa fa-upload'}, {'label':'Cancel', 'icon':'fa fa-times'}),]
                redis_session.update_response_json_buttons(payload)

                    
                # this would be a good place to stitch
                # check for swap_session flag in respons_json
                return redirect('/')

            
            elif current_intent == "make_order_item_id":
                make_order_item_id = request_args['make_order_item_id']
                
                order_card_data = {}
                order_card_data['session_data'] = {}
                order_card_data['print_data'] = {}
                order_card_data['verity_data'] = {}


                order_card_data['session_data']['card_type'] = "Order_Card"
                order_card_data['session_data']['level'] = 1
                # could be Regular
                order_card_data['session_data']['session_type']= "Customer"
                order_card_data['session_data']['redeem_code']= True
                order_card_data['session_data']['redeem_code_value']= ''
                order_card_data['session_data']['duration_in_seconds'] = 60*60
                order_card_data['session_data']['active_days'] = 7

                # auth_reset_card['print_data']['item_id'] = 28
                order_card_data['print_data']['item_media_plate_url'] = 'static/media_store/plate_two_half_reverse.jpg'
                order_card_data['print_data']['heading'] = 'Order'
                order_card_data['print_data']['sub_heading'] = 'OrderCard'
                order_card_data['print_data']['indicator'] = 'Or'

                order_card_data['created_at'] = time.asctime(time.localtime(time.time()))
                json_data = order_card_data

                print(f'recieved json data is : {json_data}')

                if json_data['session_data']['redeem_code']:
                        # Generating a random 4-character hexadecimal string
                        new_code = uuid.uuid4().hex[:4].upper()
        
                        # Hashing the generated code
                        hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
                        print(f"new code : {new_code} and hashed_code : {hashed_code} ")

                        # Replace the provided value with the hashed code
                        json_data['session_data']['redeem_code_value'] = hashed_code

                        # To verify, you can re-hash the new code and compare it with the stored hashed value
                        rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()


                        if rehashed_code == hashed_code:
                            print("Generated Verification Code successful.")
                            res = generate_qrcode_image(json_data)
                            final_res = generate_transaction_card(res[0], res[1])
                            final_res['new_code'] = new_code

                            if final_res['status']:
                                image_path = final_res['url']
                                print(final_res)
                                if final_res['status']:  
                                    cards = Card.get_all()
                                    # the common thing is the last card created (check timestamp diffrenece) is the owner of the code
                                    updated_card_list = [{f"{card.uid}" : final_res['new_code']} for card in cards if card.id == max([i.id for i in cards ])  ]
                                    print(f"updated list {updated_card_list}")
                                    redis_session.update_activity_updated_card_list(updated_card_list)
                                    
                                    
                                    return redirect("/dev")

                                else:
                                    # update bot buttons
                                    return redirect("/dev")

                                
                            else:
                                return jsonify({'status': False, 'message': 'Failed to generate card image'})
 
                else:
                    message = "Generated Code Verification failed"
                    print(message)
                    return jsonify({"status":False, "message":message})
            
            
            
            else:
                redis_session.update_activity_intent('Landing_page') 
                return redirect('/') 


# dev dashboard
@platform_api.route('/dev', methods=['GET'])
def dev_index():
    try:
        cookie_id = request.cookies.get('user_data')
        print(f"checking cookie_id at /dev {cookie_id}")

        if cookie_id is None:
            return redirect ('/')
            
        redis_session = UserSessionProfile.get(cookie_id)
        
        
        if redis_session is None:
            return redirect('/') 
        else:
            request_args = request.args 
            if len(request_args) == 0:

                current_intent = redis_session.activity_json['current_intent']

                if current_intent == "Landing_page":
                    # update bot buttons
                    payload = [({'label':'Logout', 'icon':'fa fa-sign-out'}),]
                    cards = Card.get_all()
                    redis_session.update_response_json_buttons(payload)
                    bot_view_data = redis_session.dict()['response_json']

                    updated_list = redis_session.dict()['activity_json']['updated_card_list']
                    print(f"testing /dev for updated_list : {type(updated_list)}")

                    if updated_list != []:
                        response = make_response(render_template('web_dev_bot.html', session_data=redis_session.dict(), bot_view=bot_view_data, cards=cards, new_list=updated_list))
                    else:
                        response = make_response(render_template('web_dev_bot.html', session_data=redis_session.dict(), bot_view=bot_view_data, cards=cards))
                    return response
            
            else:
                # update bot buttons
                keys_available = [ key for key,value in request_args.items()]
                print(f"args is of type {type(request_args)} and keys are : {keys_available}")

                if 'download_card_uid' in keys_available:
                    download_card_uid = request_args['download_card_uid']
                    card = Card.get(download_card_uid)
                    url = card.url
                    print(f"download url : {url}")
                    url_split = url.split("/api_master_v1")[1]
                    print(f"send file status : {send_file(url, as_attachment=True)}")

                    return redirect('/dev') 


                if 'delete_card_uid' in keys_available:
                    delete_card_uid = request_args['delete_card_uid']
                    card = Card.get(delete_card_uid)
                    if card:
                        card.delete()
                        # remove file
                        os.remove(card.url)
                        return redirect('/dev')
                        
                    else:
                        return jsonify({'message': 'Card not found'}), 404
                

                if 'auth_card_uid' in keys_available:
                    uid = request_args['auth_card_uid']
                    card = Card.get(uid)
                    if card:
                        lookup_data = card.dict()
                        print(f"testing dump on lookup_data : {lookup_data['payload']}")
                        res = GeneralMiddleware().generate_auth_card(lookup_data)
                        cards = Card.get_all()
                        # the common thing is the last card created (check timestamp diffrenece) is the owner of the code
                        updated_card_list = [{f"{card.uid}" : res['new_code']} for card in cards if card.id == max([i.id for i in cards ])  ]
                        print(f"updated list {updated_card_list}")
                        redis_session.update_activity_updated_card_list(updated_card_list)
                        

                        return redirect("/dev")

                    else:
                        message = "unable to retrieve card data"
                        return jsonify({"status" : False, "message":message})

                if 'new_auth_reset_card_uid' in keys_available:
                    uid = request_args['new_auth_reset_card_uid']
                    auth_reset_card_dev = {}
                    auth_reset_card_dev['session_data'] = {}
                    auth_reset_card_dev['print_data'] = {}
                    auth_reset_card_dev['verity_data'] = {}


                    auth_reset_card_dev['session_data']['card_type'] = "Auth_Reset_Card"
                    auth_reset_card_dev['session_data']['level'] = 0
                    auth_reset_card_dev['session_data']['session_type']= "Admin"
                    auth_reset_card_dev['session_data']['redeem_code']= True
                    auth_reset_card_dev['session_data']['redeem_code_value']= ''
                    auth_reset_card_dev['session_data']['duration_in_seconds'] = 60*60
                    auth_reset_card_dev['session_data']['active_days'] = 7

                    # auth_reset_card['print_data']['item_id'] = 28
                    auth_reset_card_dev['print_data']['item_media_plate_url'] = 'static/media_store/session_plates/plate_session_full_centerd.jpg'
                    auth_reset_card_dev['print_data']['heading'] = 'Auth'
                    auth_reset_card_dev['print_data']['sub_heading'] = 'Sub_heading'
                    auth_reset_card_dev['print_data']['indicator'] = 'Re'



                    auth_reset_card_dev['created_at'] = time.asctime(time.localtime(time.time()))
                    json_data = auth_reset_card_dev

                    print(f'recieved json data is : {json_data}')

                    if json_data['session_data']['redeem_code']:
                        # Generating a random 4-character hexadecimal string
                        new_code = uuid.uuid4().hex[:4].upper()

        
                        # Hashing the generated code
                        hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
                        print(f"new code : {new_code} and hashed_code : {hashed_code} ")

                        # Replace the provided value with the hashed code
                        json_data['session_data']['redeem_code_value'] = hashed_code

                        # To verify, you can re-hash the new code and compare it with the stored hashed value
                        rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()

                        if rehashed_code == hashed_code:
                            print("Generated Verification Code successful.")
                            res = generate_qrcode_image(json_data)
                            final_res = generate_big_card(res[0], res[1])
                            final_res['new_code'] = new_code

                            if final_res['status']:
                                image_path = final_res['url']
                                print(final_res)
                                if final_res['status']:  
                                    cards = Card.get_all()
                                    # the common thing is the last card created (check timestamp diffrenece) is the owner of the code
                                    updated_card_list = [{f"{card.uid}" : final_res['new_code']} for card in cards if card.id == max([i.id for i in cards ])  ]
                                    print(f"updated list {updated_card_list}")
                                    redis_session.update_activity_updated_card_list(updated_card_list)
                                    
                                    
                                    return redirect("/dev")

                                else:
                                    # update bot buttons
                                    return redirect("/dev")

                                
                            else:
                                return jsonify({'status': False, 'message': 'Failed to generate card image'})

                    else:
                        message = "Generated Code Verification  failed"
                        print(message)
                        return jsonify({'status': False, 'message': message})

                 

    except Exception as e :
        return f"error {e}"

    
   
# dev dashboard
@platform_api.route('/admin', methods=['GET'])
def admin_index():
    try:
        cookie_id = request.cookies.get('user_data')
        print(f"checking cookie_id at /admin {cookie_id}")

        if cookie_id is None:
            return redirect("/")

        redis_session = UserSessionProfile.get(cookie_id)
        

        if redis_session is None:
            return redirect("/")
        else:
            request_args = request.args 
            if len(request_args) == 0:

                current_intent = redis_session.activity_json['current_intent']

                print(f"redis session current_intent is {current_intent}")

                if current_intent == "Landing_page":
                    # update bot buttons
                    payload = [ ({'label':'Home', 'icon':'fa fa-home'}, {'label':'Items', 'icon':'fa fa-shopping-cart'}, {'label':'Refresh', 'icon':'fa fa-refresh'}),
                                ({'label':'Transaction', 'icon': 'fa fa-list'},{'label':'Payment', 'icon': 'fa fa-money'},{'label':'Order', 'icon':'fa fa-shopping-basket'}),
                                ({'label':'Task', 'icon': 'fa fa-sticky-note'},{'label':'Geo', 'icon': 'fa fa-map-pin'}),
                                ({'label':'Logout', 'icon':'fa fa-sign-out'},)
                            ]

                    cards = Card.get_all()
                    redis_session.update_response_json_buttons(payload)
                    bot_view_data = redis_session.dict()['response_json']
                    print(f"testing button set\n\nindex-0 : {bot_view_data['current_bot_buttons'][0]}\n\nindex-1 : {bot_view_data['current_bot_buttons'][1]}\n\nindex-2 : {bot_view_data['current_bot_buttons'][2]}\n\nindex-3 : {bot_view_data['current_bot_buttons'][3]}\n\n")
                    print(f"testing redis_session.dict() : {redis_session.dict()}")

                    updated_list = redis_session.dict()['activity_json']['updated_card_list']
                    print(f"testing retrieval of updated_list : {updated_list}")
                    print(f"testing /dev for updated_list : {type(updated_list)}")
                        
                    if (updated_list is not None) and (updated_list != []):
                        response = make_response(render_template('web_admin_bot.html', session_data=redis_session.dict(), bot_view=bot_view_data, cards=cards, new_list=updated_list))
                    else:
                        response = make_response(render_template('web_admin_bot.html', session_data=redis_session.dict(), bot_view=bot_view_data, cards=cards))
                    return response
                
                if current_intent == "Items_page":
                    payload = [ ({'label':'Home', 'icon':'fa fa-home'}, {'label':'Items', 'icon':'fa fa-shopping-cart'}, {'label':'Refresh', 'icon':'fa fa-refresh'}),
                                ({'label':'Transaction', 'icon': 'fa fa-list'},{'label':'Payment', 'icon': 'fa fa-money'},{'label':'Order', 'icon':'fa fa-shopping-basket'}),
                                ({'label':'Task', 'icon': 'fa fa-sticky-note'},{'label':'Geo', 'icon': 'fa fa-map-pin'}),
                                ({'label':'Logout', 'icon':'fa fa-sign-out'},)
                            ]
                    resource_data = Item.get_all()
                    
                    redis_session.update_response_json_buttons(payload)
                    bot_view_data = redis_session.dict()['response_json']
                    response = make_response(render_template('web_admin_bot.html', session_data=redis_session.dict(), resource_data=resource_data, bot_view=bot_view_data))
                    return response

            else:

                keys_available = [key for key,value in request_args.items()] 
                print(f"args is of type {type(request_args)} and keys are : {keys_available}")

                if 'download_card_uid' in keys_available:
                    download_card_uid = request_args['download_card_uid']
                    card = Card.get(download_card_uid)
                    url = card.url
                    print(f"download url : {url}")
                    url_split = url.split("/api_master_v1")[1]
                    print(f"send file status : {send_file(url)}")

                    return redirect('/admin') 


                if 'delete_card_uid' in keys_available:

                    delete_card_uid = request_args['delete_card_uid']
                    card = Card.get(delete_card_uid)
                    if card:
                        card.delete()
                        # remove file
                        os.remove(card.url)
                        return redirect('/admin')
                        
                    else:
                        return jsonify({'message': 'Card not found'}), 404
                
                if 'delete_item_id' in keys_available:
                    
                    delete_item_id = request_args['delete_item_id']
                    item = Item.get(delete_item_id)
                    if item:
                        item.delete()
                        # remove accompanying files
                        # os.remove(item.url)
                        return redirect('/admin')
                        
                    else:
                        return jsonify({'message': 'Item not found'}), 404
                
                if 'make_public_item_id' in keys_available:
                    
                    make_public_item_id = request_args['make_public_item_id']
                    item = Item.get(make_public_item_id)
                    if item:
                        item.update({'public':True})
                        return redirect('/admin')
                        
                    else:
                        return jsonify({'message': 'Item not found'}), 404

                if 'make_private_item_id' in keys_available:
                    
                    make_private_item_id = request_args['make_private_item_id']
                    item = Item.get(make_private_item_id)
                    if item:
                        item.update({'public':False})
                        return redirect('/admin')
                        
                    else:
                        return jsonify({'message': 'Item not found'}), 404



                if 'intent' in keys_available:
                    # switch intent Items_page
                    if request_args['intent'] == "Items":

                        redis_session.update_activity_intent("Items_page")
                        return redirect("/admin")
                    
                    if request_args['intent'] == "Home":

                        redis_session.update_activity_intent("Landing_page")
                        return redirect("/admin")
                
                    if request_args['intent'] == "Refresh":

                        redis_session.update_activity_intent("Landing_page")
                        return redirect("/admin")


                if 'make_insta_pu_item_id' in keys_available:
                    item_id = request_args['make_insta_pu_item_id']
                    item = Item.get(item_id)
                    item = item.dict()

                    print(f"fetched item is {item}\n\nand type is {type(item)}")

                    p_url = item['item_media_instacard_big_plate_url']
                    print(f"testing url : { p_url }")

                    if item:
                        print(f"making instaticket public for item id : {item_id} and url to use is : {p_url}")
                        insta_pu_card_data = {}
                        insta_pu_card_data['session_data'] = {}
                        insta_pu_card_data['print_data'] = {}
                        insta_pu_card_data['verity_data'] = {}


                        insta_pu_card_data['session_data']['card_type'] = "Insta_Pu_Card"
                        insta_pu_card_data['session_data']['level'] = 0
                        # could be Regular
                        insta_pu_card_data['session_data']['session_type']= "Customer"
                        insta_pu_card_data['session_data']['redeem_code']= True
                        insta_pu_card_data['session_data']['redeem_code_value']= ''
                        insta_pu_card_data['session_data']['duration_in_seconds'] = 60*60
                        insta_pu_card_data['session_data']['active_days'] = 7

                        insta_pu_card_data['print_data']['item_id'] = item['id']
                        insta_pu_card_data['print_data']['item_media_plate_url'] = f"static/media_store{item['item_media_instacard_big_plate_url']}"
                        insta_pu_card_data['print_data']['heading'] = f"Insta-{item['name']}"
                        insta_pu_card_data['print_data']['sub_heading'] = 'Sub_heading'
                        insta_pu_card_data['print_data']['indicator'] = 'Pu'



                        insta_pu_card_data['created_at'] = time.asctime(time.localtime(time.time()))

                        json_data = insta_pu_card_data

                        print(f'recieved json data is : {json_data}')

                        if json_data['session_data']['redeem_code']:
                            # Generating a random 4-character hexadecimal string
                            new_code = uuid.uuid4().hex[:4].upper()

        
                            # Hashing the generated code
                            hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
                            print(f"new code : {new_code} and hashed_code : {hashed_code} ")

                            # Replace the provided value with the hashed code
                            json_data['session_data']['redeem_code_value'] = hashed_code

                        # To verify, you can re-hash the new code and compare it with the stored hashed value
                            rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()

                            if rehashed_code == hashed_code:
                                print("Generated Verification Code successful.")
                                res = generate_qrcode_image(json_data)
                                final_res = generate_big_card(res[0], res[1])
                                final_res['new_code'] = new_code

                                if final_res['status']:
                                    image_path = final_res['url']
                                    print(final_res)
                                    if final_res['status']:
                                        print(f"here, now")
                                        cards = Card.get_all()
                                        # the common thing is the last card created (check timestamp diffrenece) is the owner of the code
                                        updated_card_list = [{f"{card.uid}" : final_res['new_code']} for card in cards if card.id == max([i.id for i in cards ])  ]
                                        print(f"updated list {updated_card_list}")
                                        redis_session.update_activity_updated_card_list(updated_card_list)
                                        
                                        redis_session.update_activity_intent("Landing_page")

                                        return redirect("/admin")

                                    else:
                                        # update bot buttons
                                        redirect("/admin")

                                
                                else:
                                    return jsonify({'status': False, 'message': 'Failed to generate card image'})

                        else:
                            message = "Generated Code Verification  failed"
                            print(message)
                            return jsonify({'status': False, 'message': message})



                        return redirect('/admin')
                    else:
                        return jsonify({"message":"item not found"})
                
                if 'make_insta_pr_item_id' in keys_available:
                    item_id = request_args['make_insta_pr_item_id']
                    item = Item.get(item_id)
                    item = item.dict()

                    print(f"fetched item is {item}\n\nand type is {type(item)}")

                    p_url = item['item_media_instacard_big_plate_url']
                    print(f"testing url : { p_url }")

                    if item:
                        print(f"making instaticket public for item id : {item_id} and url to use is : {p_url}")
                        insta_pr_card_data = {}
                        insta_pr_card_data['session_data'] = {}
                        insta_pr_card_data['print_data'] = {}
                        insta_pr_card_data['verity_data'] = {}


                        insta_pr_card_data['session_data']['card_type'] = "Insta_Pr_Card"
                        insta_pr_card_data['session_data']['level'] = 1
                        # could be Regular
                        insta_pr_card_data['session_data']['session_type']= "Customer"
                        insta_pr_card_data['session_data']['redeem_code']= True
                        insta_pr_card_data['session_data']['redeem_code_value']= ''
                        insta_pr_card_data['session_data']['duration_in_seconds'] = 60*60
                        insta_pr_card_data['session_data']['active_days'] = 7

                        insta_pr_card_data['print_data']['item_id'] = item['id']
                        insta_pr_card_data['print_data']['item_media_plate_url'] = f"static/media_store{item['item_media_instacard_big_plate_url']}"
                        insta_pr_card_data['print_data']['heading'] = f"Insta-{item['name']}"
                        insta_pr_card_data['print_data']['sub_heading'] = 'Sub_heading'
                        insta_pr_card_data['print_data']['indicator'] = 'Pr'



                        insta_pr_card_data['created_at'] = time.asctime(time.localtime(time.time()))

                        json_data = insta_pr_card_data

                        print(f'recieved json data is : {json_data}')

                        if json_data['session_data']['redeem_code']:
                            # Generating a random 4-character hexadecimal string
                            new_code = uuid.uuid4().hex[:4].upper()

        
                            # Hashing the generated code
                            hashed_code = hashlib.sha256(new_code.encode()).hexdigest()
    
                            print(f"new code : {new_code} and hashed_code : {hashed_code} ")

                            # Replace the provided value with the hashed code
                            json_data['session_data']['redeem_code_value'] = hashed_code

                        # To verify, you can re-hash the new code and compare it with the stored hashed value
                            rehashed_code = hashlib.sha256(new_code.encode()).hexdigest()

                            if rehashed_code == hashed_code:
                                print("Generated Verification Code successful.")
                                res = generate_qrcode_image(json_data)
                                final_res = generate_big_card(res[0], res[1])
                                final_res['new_code'] = new_code

                                if final_res['status']:
                                    image_path = final_res['url']
                                    print(final_res)
                                    if final_res['status']:
                                        print(f"here, now")
                                        cards = Card.get_all()
                                        # the common thing is the last card created (check timestamp diffrenece) is the owner of the code
                                        updated_card_list = [{f"{card.uid}" : final_res['new_code']} for card in cards if card.id == max([i.id for i in cards ])  ]
                                        print(f"updated list {updated_card_list}")
                                        redis_session.update_activity_updated_card_list(updated_card_list)
                                        
                                        redis_session.update_activity_intent("Landing_page")

                                        return redirect("/admin")

                                    else:
                                        # update bot buttons
                                        redirect("/admin")

                                
                                else:
                                    return jsonify({'status': False, 'message': 'Failed to generate card image'})

                        else:
                            message = "Generated Code Verification  failed"
                            print(message)
                            return jsonify({'status': False, 'message': message})



                        return redirect('/admin')
                    else:
                        return jsonify({"message":"item not found"})


    except Exception as e :
        return f"error {e}"



@platform_api.route('/login', methods=['GET'])
def signin_web_user():
    args = request.args
    if 'swap' in args:
        swap_value = args['swap']
        # Process the 'swap' value as needed
        # Add your code logic here based on the value of 'swap'
        print(f"Received swap value: {swap_value}")
        redis_session = UserSessionProfile.get(request.cookies.get('user_data'))
        if redis_session is None:
            return redirect(url_for('index'))
        else:
            redis_session.complete_session_swap()
            return redirect(url_for('index'))
    else:
        # Handle the case when 'swap' is not present
        return jsonify({"error": "No arguments provided for 'swap'."})


        
# Web_bot endpoint
# logout endpoint, which updates the redis_session session_type to Regular
@platform_api.route('/logout' , methods=['GET'])
def logout():
    redis_session = UserSessionProfile.get(request.cookies.get('user_data'))
    if redis_session is None:
        return redirect(url_for('index'))
    else:
        redis_session.reset_user_session_profile()
        return redirect(url_for('index'))


# Web_bot endpoint
# cards
@platform_api.route('/cards', methods=['POST'])
def create_card():
    data = request.get_json()
    card = Card(**data)
    card.save()
    return jsonify(card.dict())


@platform_api.route('/cards/<uid>', methods=['GET'])
def get_card(uid):
    print(f"card check reached")
    card = Card.get(uid)
    if card:
        return jsonify(card.dict())
    else:
        return jsonify({'message': 'Card not found'}), 404


@platform_api.route('/cards/<uid>', methods=['DELETE'])
def delete_card(uid):
    card = Card.get(uid)
    if card:
        card.delete()
        return jsonify({'message': 'Card deleted'})
    else:
        return jsonify({'message': 'Card not found'}), 404


# items
@platform_api.route('/items', methods=['GET'])
def get_all_items():
    try:
        items = Item.get_all()
        return jsonify([item.dict() for item in items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@platform_api.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    try:
        item = Item.get(id)
        if item:
            return jsonify(item.dict()), 200
        return jsonify({'message': 'Item not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@platform_api.route('/items', methods=['POST'])
def create_item():
    try:
        print(f"checking for files")
        recieved_files = request.files
        print(f"checking for files  {recieved_files}")

        # Process item_media_file
        if 'item_media_file' in recieved_files:
            print(f"checking item_media_file")
            file = recieved_files['item_media_file']
            extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{extension}"
            file.save(os.path.join(UPLOAD_FOLDER, 'landing_images', unique_filename))
            item_media_file = f'/landing_images/{unique_filename}'

        # Process other files
        item_order_media_file = None
        item_receipt_media_file = None
        item_instacard_file = None
        for key in ['item_order_media_file', 'item_receipt_media_file', 'item_instacard_file']:
            print(f"checking {key}")
            if key in recieved_files:
                file = recieved_files[key]
                extension = file.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4()}.{extension}"
                file.save(os.path.join(UPLOAD_FOLDER, 'plates', unique_filename))
                if key == 'item_order_media_file':
                    item_order_media_file = f'/plates/{unique_filename}'
                elif key == 'item_receipt_media_file':
                    item_receipt_media_file = f'/plates/{unique_filename}'
                elif key == 'item_instacard_file':
                    item_instacard_file = f'/plates/{unique_filename}'


        new_item = Item(
            public=True,
            item_type=request.form['item_type'],
            title=request.form['item_title'],
            name=request.form['item_name'],
            price=request.form['item_price'],
            description=request.form['item_description'],
            item_media_url=item_media_file,
            item_media_order_plate_url=item_order_media_file,
            item_media_receipt_plate_url=item_receipt_media_file,
            item_media_instacard_big_plate_url=item_instacard_file,
        )

        new_item.save()
        return jsonify(new_item.__dict__), 201
    except Exception as e:
        res = {'error': str(e)}
        print(res)
        return jsonify(), 500



@platform_api.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    try:
        item = Item.get(id)
        if item:
            update_data = request.json
            item.update(update_data)
            return jsonify(item.dict()), 200
        return jsonify({'message': 'Item not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@platform_api.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        item = Item.get(id)
        if item:
            item.delete()
            return jsonify({'message': 'Item deleted.'}), 200
        return jsonify({'message': 'Item not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# new update
@platform_api.route('/api/auth', methods=['GET'])
def get_all_auths():
    """Retrieve all Auth records."""
    session = Session()
    try:
        auths = Auth.index(session)
        return jsonify(auths), 200
    finally:
        session.close()  # Ensure the session is closed


@platform_api.route('/api/auth', methods=['POST'])
def create_auth():
    """Create a new Auth record."""
    data = request.json
    session = Session()
    try:
        new_auth = Auth.store(session, data['user_email'], data['password_hash'], data.get('role', 'user'))
        return jsonify(new_auth), 201
    finally:
        session.close()  # Ensure the session is closed


@platform_api.route('/api/auth/<int:uid>', methods=['GET'])
def get_auth(uid):
    """Retrieve a specific Auth record by uid."""
    session = Session()
    try:
        auth_record = Auth.show(session, uid)
        if auth_record:
            return jsonify(auth_record), 200
        return jsonify({'message': 'Auth record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed


@platform_api.route('/api/auth/<int:uid>', methods=['PUT'])
def update_auth(uid):
    """Update an Auth record."""
    data = request.json
    session = Session()
    try:
        # Convert current_auth_token_expiry to a datetime object if it exists
        if 'current_auth_token_expiry' in data:
            data['current_auth_token_expiry'] = datetime.fromisoformat(data['current_auth_token_expiry'])

        updated_auth = Auth.update(session, uid, **data)
        if updated_auth:
            return jsonify(updated_auth), 200
        return jsonify({'message': 'Auth record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed


@platform_api.route('/api/auth/<int:uid>', methods=['DELETE'])
def delete_auth(uid):
    """Delete an Auth record."""
    session = Session()
    try:
        success = Auth.destroy(session, uid)
        if success:
            return jsonify({'message': 'Auth record deleted'}), 204
        return jsonify({'message': 'Auth record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed

@platform_api.route('/api/auth/reset/<int:uid>', methods=['POST'])
def reset_auth(uid):
    """Reset authentication for a user."""
    session = Session()
    try:
        updated_auth = Auth.resetAuth(session, uid)
        if updated_auth:
            return jsonify(updated_auth), 200
        return jsonify({'message': 'Auth record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed

@platform_api.route('/api/auth/token/update/<int:uid>', methods=['POST'])
def update_auth_token(uid):
    """Update the authentication token for a user."""
    data = request.json
    session = Session()
    try:
        # Convert expiry to a datetime object if it exists
        if 'expiry' in data:
            data['expiry'] = datetime.fromisoformat(data['expiry'])

        updated_auth = Auth.updateAuthToken(session, uid, data['new_token'], data['expiry'])
        if updated_auth:
            return jsonify(updated_auth), 200
        return jsonify({'message': 'Auth record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed
    
@platform_api.route('/api/auth/token/verify/<int:uid>', methods=['POST'])
def verify_auth_token(uid):
    """Verify the authentication token for a user."""
    data = request.json
    session = Session()
    try:
        is_valid = Auth.verifyAuthToken(session, uid, data['token'])
        if is_valid is True:
            return jsonify({'message': 'Token is valid'}), 200
        elif is_valid is False:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        return jsonify({'message': 'Auth record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed






# Location
# Retrieve all Location records
@platform_api.route('/api/location', methods=['GET'])
def get_all_locations():
    """Retrieve all Location records."""
    session = Session()
    try:
        locations = Location.index(session)
        return jsonify(locations), 200
    finally:
        session.close()  # Ensure the session is closed

# Create a new Location record
@platform_api.route('/api/location', methods=['POST'])
def create_location():
    """Create a new Location record."""
    data = request.json
    session = Session()
    try:
        new_location = Location.store(session, data['uid'], data['name'], data['location_pin_type'], data['latitude'], data['longitude'])
        return jsonify(new_location), 201
    finally:
        session.close()  # Ensure the session is closed


# Retrieve a specific Location record by UID
@platform_api.route('/api/location/<int:uid>', methods=['GET'])
def get_location(uid):
    """Retrieve a specific Location record by uid."""
    session = Session()
    try:
        location_record = Location.show(session, uid)
        if location_record:
            return jsonify(location_record), 200
        return jsonify({'message': 'Location record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed


# Update a Location record
@platform_api.route('/api/location/<int:uid>', methods=['PUT'])
def update_location(uid):
    """Update a Location record."""
    data = request.json
    session = Session()
    try:
        updated_location = Location.update(session, uid, **data)
        if updated_location:
            return jsonify(updated_location), 200
        return jsonify({'message': 'Location record not found'}), 404
    finally:
        session.close()  # Ensure the session is closed


# Delete a Location record
@platform_api.route('/api/location/<int:uid>', methods=['DELETE'])
def delete_location(uid):
    """Delete a Location record."""
    session = Session()
    try:
        success = Location.destroy(session, uid)
        if success:
            return jsonify({'message': 'Location record deleted'}), 204
        return jsonify({'message': 'Location record not found'}), 404
    finally:
        session.close()  





# Ensure the session is closed
# Web_bot Custom 404 error handler
@platform_api.errorhandler(404)
def page_not_found(error):
    print(f"error is : {error}")
    return redirect(url_for('index'))



if __name__ == '__main__':
    
    platform_api.run(host='0.0.0.0', port=5009,debug=True)
