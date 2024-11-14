"""
This module helps with matters philate.
It will be responsible for generating and reading receipts 
"""
from api_master import datetime, timedelta, secrets, string, token_urlsafe, time
from api_master import Image, ImageDraw, ImageFont, pyzbar, qrcode
from api_master import generate_password_hash, check_password_hash, secure_filename, send_file
from api_master import hashlib, os 

from api_master.db import base_bot_db
from api_master.models import Card, Transaction

alphanumerics = string.ascii_letters + string.digits


def comma(number):
    return "{:,}".format(number)


def hash_qrcode_data(receipt_data):
    string_holder=''
    for key_value in receipt_data.keys():
        string_holder += str(receipt_data[key_value])
    
    return generate_password_hash(string_holder)

def sale_receipt_chunker(line_character_max, string_text):
    # identify the number of words in the input_string with their start and stop position
    # map splitting points in the input_string
    # count the words in the word_set and each time evaluate if the current word is an add_to_sentence or start_new_line
    word_set = string_text.split(' ')
    print_character_count = 0
    word_set_map = []
    print_digest = ''

    for word in word_set:
        start_point = print_character_count
        for char in word:
            print_character_count = print_character_count + 1
        word_set_map.append(f'{word}:{start_point}:{print_character_count}')
    
    print(f'current word-map : {word_set_map}')

    current_line_char_max = line_character_max
        

    for word_node in word_set_map:
        node_split = word_node.split(':')
        
        if int(node_split[2]) < current_line_char_max:
            print_digest = print_digest + ' ' +  node_split[0]
        else:
            print_digest = print_digest + '\n' + node_split[0]
            current_line_char_max = current_line_char_max + line_character_max
            

    return print_digest


def generate_qrcode_image(data):
    qr = qrcode.QRCode(
        version=2,
        box_size=10,
        border=2
    )
    data_hash = hash_qrcode_data(data)
    qr.add_data(data_hash)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color='black', back_color='white')
    print(f'size for qr_image is : {qr_image.size}')
    # data['qr_code_size'] = [qr_image.size[0], qr_image.size[1]]
    data['verity_data']['qr_data_hash'] = data_hash
    return qr_image, data


def generate_transaction_card(image, data):
    try:
        # used for all order transactions 
        print(f'data from generating card qrcode {data}')
        staging_path=os.path.abspath('./static/out_store/')
   
        top_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 50)
        middle_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-Bold.ttf', 40)
        lower_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-Bold.ttf', 30)
    
        top_anchor = (260, 215)
        middle_anchor = (260,720)
        lower_anchor = (280,780)

        plate_one_half_reverse_template = Image.open(data['print_data']['item_media_plate_url'])
        editable_plate_one_half_reverse_template = ImageDraw.Draw(plate_one_half_reverse_template)
        display_date = datetime.utcnow().strftime("%d-%m-%Y")
    
        editable_plate_one_half_reverse_template.text(top_anchor, data['print_data']['heading'], 'black', font=top_font)
        editable_plate_one_half_reverse_template.text(middle_anchor, data['print_data']['sub_heading'], 'black', font=middle_font)
        editable_plate_one_half_reverse_template.text(lower_anchor, display_date, 'black', font=lower_font)
     
        card_file_name =''
        for i in range(10):
            card_file_name +=  secrets.choice(alphanumerics)

        temp_save_path = f'{staging_path}/'+f'{display_date}:card:'+f'{card_file_name}.jpg'
        plate_one_half_reverse_template.save(temp_save_path)

        new_qr_size = (300,300)
        image = image.get_image()
        pil_image = image.resize(new_qr_size)
    
        card_qr_code_anchor = ((960-new_qr_size[0]), (955-new_qr_size[1]))
    
        print(card_qr_code_anchor)
        template  = Image.open(temp_save_path)
        template.paste(pil_image, card_qr_code_anchor)
        template.save(temp_save_path)
        print(temp_save_path)

        # Save the payload_hash_string, {value} to Redis
        print(f"type for data is {type(data)}")
        print(f"type for qr_data_hash is {type(data['verity_data']['qr_data_hash'])}")
        print(f"qr_data_hash value is {data['verity_data']['qr_data_hash']}")


        if data['session_data']['level'] == 0:
            # update : card listing with $data payload
            card = Card(payload=data, uid=data['verity_data']['qr_data_hash'], url=temp_save_path)
            card.save()

        else:
            # Calculate the hash of the modified image
            image_hash = calculate_file_hash(temp_save_path)
            data['verity_data']['tx_file_hash'] = image_hash['message']
            # update : card listing with $data payload
            card = Card(payload=data, uid=data['verity_data']['qr_data_hash'], url=temp_save_path)
            card.save()

        split_list = temp_save_path.split('/')
        print(f'split_list => {split_list}, and length is => {len(split_list)}')
        ret_url =  split_list[-3] + '/' + split_list[-2] + '/' + split_list[-1]
        return {'status':True, 'url':ret_url}
    
    except Exception as e:
        return {'status':False, 'message':f"unable to generate card => {e}", "url":"/static/landing_images/processing_error_image.jpg"} 
 


def generate_big_card(image, data):
    try:
        print(f'recieved data is : {data}')

        staging_path = os.path.abspath('./static/out_store/')
        header_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 60)
        indicator_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 60)

        sub_header_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-SemiBold.ttf', 40)
        r_l_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 40)
        l_l_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-SemiBold.ttf', 40)
        
        

        header_anchor = (240, 640)
        indicator_anchor = (700, 640)
        sub_header_anchor = (270, 720)
        l_l_anchor = (270, 1210)
        r_l_anchor = (700, 1210)

        plate_one_full_centered_template = Image.open(f"{data['print_data']['item_media_plate_url']}")
        editable_plate_one_full_centered_template = ImageDraw.Draw(plate_one_full_centered_template)
        
        editable_plate_one_full_centered_template.text(header_anchor, data['print_data']['heading'], 'black', font=header_font)
        editable_plate_one_full_centered_template.text(indicator_anchor, data['print_data']['indicator'], 'black', font=indicator_font)

        display_date_data = data['created_at']
        split = display_date_data.split(" ")
        print(f"testing split display date: {split}")

        display_date_data = f"{split[0]} {split[1]} {split[2]} {split[4]}"
        editable_plate_one_full_centered_template.text(sub_header_anchor, display_date_data, 'black', font=sub_header_font)

        editable_plate_one_full_centered_template.text(l_l_anchor, split[3], 'black', font=l_l_font)
        editable_plate_one_full_centered_template.text(r_l_anchor, data['session_data']['session_type'][:3], 'black', font=r_l_font)
        card_file_name = ''
        for _ in range(10):
            card_file_name += secrets.choice(alphanumerics)

        temp_save_path = f'{staging_path}/{display_date_data}:one_full_centered:{card_file_name}.png'
        plate_one_full_centered_template.save(temp_save_path)

        new_qr_size = (300, 300)
        image = image.get_image()
        pil_image = image.resize(new_qr_size)
        card_qr_code_anchor = ((960 - new_qr_size[0]), (1120 - new_qr_size[1]))

        print(card_qr_code_anchor)
        template = Image.open(temp_save_path)
        template.paste(pil_image, card_qr_code_anchor)
        template.save(temp_save_path)
        print(temp_save_path)

        
        # Save the payload_hash_string, {value} to Redis
        print(f"type for data is {type(data)}")
        print(f"type for qr_data_hash is {type(data['verity_data']['qr_data_hash'])}")
        print(f"qr_data_hash value is {data['verity_data']['qr_data_hash']}")


        if data['session_data']['level'] == 0:
            # update : card listing with $data payload
            card = Card(payload=data, uid=data['verity_data']['qr_data_hash'], url=temp_save_path)
            card.save()

        else:
            # Calculate the hash of the modified image
            image_hash = calculate_file_hash(temp_save_path)
            data['verity_data']['tx_file_hash'] = image_hash['message']
            # update : card listing with $data payload
            card = Card(payload=data, uid=data['verity_data']['qr_data_hash'], url=temp_save_path)
            card.save()
        
        print(f"during philate: generating_big_card, temp_save_path is : {temp_save_path}")

        split_list = temp_save_path.split('/')

        print(f"during philate: generating_big_card, split_list is : {split_list}, and the length is : {len(split_list)}")

        # ret_url = f'{split_list[-3]}/{split_list[-2]}/{split_list[-1]}'

        return {'status': True, 'url': temp_save_path}

    except Exception as e:
        response = {'status':False, 'message':f"unable to generate card => {e}",  'url':"/static/landing_images/processing_error_image.jpg"}
        print(f'errorr during generating_big_card {response}')
        return response
     

def generate_receipt(image, data):
    try:
        staging_path=os.path.abspath('./static/out_store/')

        header_font=ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 60)
        sub_header_font=ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-SemiBold.ttf', 40)
        service_topic_font=ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-Bold.ttf', 45)
        next_service_date_font=ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-SemiBold.ttf', 30)
        sale_description_font=ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-Bold.ttf', 25)
        sale_amount_font=ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 60)
    
    
        header_anchor=(240,280)
        sub_header_anchor=(260,360)
        service_topic_anchor=(540,1190)
        next_service_date_anchor=(540,1230)
        sale_description_anchor=(540,1300)
        sale_amount_anchor=(540, 1500)

        plate_full = Image.open(data['print_data']['item_media_plate_url'])
        editable_plate_full_template = ImageDraw.Draw(plate_full)
    
   
        next_service_date_display = data['print_data']['next_service_date']
    
        editable_plate_full_template.text(header_anchor, data['print_data']['heading'], 'black', font=header_font)
        editable_plate_full_template.text(sub_header_anchor, data['print_data']['sub_heading'], 'black', font=sub_header_font)
        editable_plate_full_template.text(service_topic_anchor, data['print_data']['service_heading'], 'black', font=service_topic_font, anchor='ms')
        editable_plate_full_template.text(next_service_date_anchor, str(next_service_date_display), 'black', font=next_service_date_font, anchor='ms')
        editable_plate_full_template.text(sale_description_anchor, sale_receipt_chunker(20, data['print_data']['sale_description']), 'black', font=sale_description_font, anchor='ms')
        editable_plate_full_template.text(sale_amount_anchor, f"Ksh {comma(data['print_data']['sale_amount'])}", 'black', font=sale_amount_font, anchor='ms')

        sale_card_file_name =''
        for i in range(10):
            sale_card_file_name +=  secrets.choice(alphanumerics)

        temp_save_path = f'{staging_path}'+'/'+f'{data["print_data"]["sub_heading"]}:receipt:sale:'+f'{sale_card_file_name}.png'
        plate_full.save(temp_save_path)

        new_qr_size = (300,300)
        pil_image = image.resize(new_qr_size)
    

        sale_card_qrcode_anchor = (960-new_qr_size[0], 400-new_qr_size[1])

        print(sale_card_qrcode_anchor)
        template = Image.open(temp_save_path)
        template.paste(pil_image, sale_card_qrcode_anchor)
        template.save(temp_save_path)
        print(temp_save_path)

        # Save the payload_hash_string, {value} to Redis
        print(f"type for data is {type(data)}")
        print(f"type for qr_data_hash is {type(data['verity_data']['qr_data_hash'])}")
        print(f"qr_data_hash value is {data['verity_data']['qr_data_hash']}")


        if data['session_data']['level'] == 0:
            # update : card listing with $data payload
            card = Card(payload=data, uid=data['verity_data']['qr_data_hash'], url=temp_save_path)
            card.save()

        else:
            # Calculate the hash of the modified image
            image_hash = calculate_file_hash(temp_save_path)
            data['verity_data']['tx_file_hash'] = image_hash['message']
            # update : card listing with $data payload
            card = Card(payload=data, uid=data['verity_data']['qr_data_hash'], url=temp_save_path)
            card.save()
    
        split_list = temp_save_path.split('/')
        ret_url = split_list[5] + '/' + split_list[6] + '/' + split_list[7]

        return {'status':True, 'url':temp_save_path} 

    except Exception as e :
        return {'status':False, 'message':f"unable to generate card => {e}", "url":"/static/landing_images/processing_error_image.jpg"}  


def decode_qr_code(image_binary):
    try:
        decoded_list = pyzbar.decode(image_binary)
        print(f"decoded list : {decoded_list}") 
        return {'status':True, 'message':decoded_list}
    except Exception as e:
        return {'status':False, 'message':e}



def calculate_file_hash(file_path):
    try:

        BUF_SIZE = 65536
        sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)

                if not data:
                    break
                sha256.update(data)
        calculated_hash =  sha256.hexdigest()
        return {'status':True, 'message':calculated_hash}
    except Exception as e:
        res = {'status':False, 'message':str(e)}
        print(f"error in calculating hash => {res}")
        return res 


