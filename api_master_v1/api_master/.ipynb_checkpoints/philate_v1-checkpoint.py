"""
This module helps with matters philate.
It will be responsible for generating and reading receipts 
"""
from api_master import datetime, timedelta, secrets, string, token_urlsafe
from api_master import Image, ImageDraw, ImageFont, pyzbar, qrcode
from api_master import generate_password_hash, check_password_hash, secure_filename, send_file
from api_master import hashlib, os 
from api_master.models import instaticket, order, sale


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


def generate_instaticket_qrcode_image(data):
    qr = qrcode.QRCode(
        version=2,
        box_size=10,
        border=2
    )
    instaticket_object = instaticket(**data['instaticket_data'])
    data['instaticket_data'] = instaticket_object.dict()
    instaticket_data_hash = hash_qrcode_data(data['instaticket_data'])
    qr.add_data(instaticket_data_hash)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color='black', back_color='white')
    print(f'size for qr_image is : {qr_image.size}')
    data['qr_code_size'] = {'width':qr_image.size[0], 'height':qr_image.size[1]}
    data['qr_data_hash'] = instaticket_data_hash
    return qr_image, data



def generate_instaticket_small(pil_image, data):
    staging_path=os.path.abspath('./static/out_store/')

    header_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 60)
    sub_header_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-SemiBold.ttf', 40)

    header_anchor = (240,220)
    sub_header_anchor = (280,300)

    plate_one_half_template = Image.open(receipt_templates['plate_one_half'])
    editable_plate_one_half_template = ImageDraw.Draw(plate_one_half_template)
    editable_plate_one_half_template.text(header_anchor, data['instaticket_data']['heading'], 'black', font=header_font)
    date_data = data['instaticket_data']['start_date']
    display_date_data = date_data.strftime("%d-%m-%Y")
    editable_plate_one_half_template.text(sub_header_anchor, display_date_data, 'black', font=sub_header_font)
    
    
    insta_ticket_file_name =''
    for i in range(10):
        insta_ticket_file_name +=  secrets.choice(alphanumerics)

    temp_save_path = f'{staging_path}'+'/'+f'{display_date_data}:one_half:'+f'{insta_ticket_file_name}.png'
    plate_one_half_template.save(temp_save_path)


   

    new_qr_size = (300,300)
    pil_image = pil_image.resize(new_qr_size)
    
    insta_ticket_qr_code_anchor = ((960-new_qr_size[0]), (700-new_qr_size[1]))
    
    print(insta_ticket_qr_code_anchor)
    template  = Image.open(temp_save_path)
    template.paste(pil_image, insta_ticket_qr_code_anchor)
    template.save(temp_save_path)
    print(temp_save_path)
    
    split_list = temp_save_path.split('/')
    ret_url = split_list[5] + '/' + split_list[6] + '/' + split_list[7]
    return {'status':True, 'url':ret_url}



def generate_instaticket_big(pil_image, data):
    staging_path=os.path.abspath('./static/out_store/')
    header_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 60)
    sub_header_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-SemiBold.ttf', 40)

    header_anchor = (240, 640)
    sub_header_anchor = (270, 720)
    

    plate_one_full_centerd_template = Image.open(receipt_templates['plate_one_full_centerd'])
    editable_plate_one_full_centerd_template =  ImageDraw.Draw(plate_one_full_centerd_template)
    editable_plate_one_full_centerd_template.text(header_anchor, data['instaticket_data']['heading'], 'black', font=header_font)
    display_date_data = data['instaticket_data']['start_date'].strftime("%d-%m-%Y")
    editable_plate_one_full_centerd_template.text(sub_header_anchor, display_date_data, 'black', font=sub_header_font)
    
    
    insta_ticket_file_name =''
    for i in range(10):
        insta_ticket_file_name +=  secrets.choice(alphanumerics)

    temp_save_path = f'{staging_path}'+'/'+f'{display_date_data}:one_full_centerd:'+f'{insta_ticket_file_name}.png'
    plate_one_full_centerd_template.save(temp_save_path)

   
    new_qr_size = (300,300)
    pil_image = pil_image.resize(new_qr_size)
    
    insta_ticket_qr_code_anchor = ((960-new_qr_size[0]), (1120-new_qr_size[1]))
    

    print(insta_ticket_qr_code_anchor)
    template  = Image.open(temp_save_path)
    template.paste(pil_image, insta_ticket_qr_code_anchor)
    template.save(temp_save_path)
    print(temp_save_path)
    
    
    split_list = temp_save_path.split('/')
    ret_url = split_list[5] + '/' + split_list[6] + '/' + split_list[7]
    return {'status':True, 'url':ret_url}




def generate_order_qrcode_image(data):
    qr = qrcode.QRCode(
        version=2,
        box_size=10,
        border=2
    )
    orderticket_object = order(**data)
    data['order_data'] = orderticket_object.dict()
    orderticket_data_hash = hash_qrcode_data(data['order_data'])
    qr.add_data(orderticket_data_hash)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color='black', back_color='white')
    print(f'size for qr_image is : {qr_image.size}')
    data['qr_code_size'] = {'width':qr_image.size[0], 'height':qr_image.size[1]}
    data['qr_data_hash'] = orderticket_data_hash
    return qr_image, data


def generate_order_ticket(pil_image, data):

    print(f'date from generating order qr code {data}')

    staging_path=os.path.abspath('./static/out_store/')
   
    top_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-ExtraBold.ttf', 50)
    middle_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-Bold.ttf', 40)
    lower_font = ImageFont.truetype('./api_master/stamp_fonts/static/OpenSans/OpenSans-Bold.ttf', 30)
    
    top_anchor = (260, 215)
    middle_anchor = (260,720)
    lower_anchor = (280,780)

    plate_one_half_reverse_template = Image.open(data['item_media_order_plate'])
    editable_plate_one_half_reverse_template = ImageDraw.Draw(plate_one_half_reverse_template)
    display_date = datetime.utcnow().strftime("%d-%m-%Y")
    
    editable_plate_one_half_reverse_template.text(top_anchor, data['order_data']['heading'], 'black', font=top_font)
    editable_plate_one_half_reverse_template.text(middle_anchor, data['order_data']['sub_heading'], 'black', font=middle_font)
    editable_plate_one_half_reverse_template.text(lower_anchor, display_date, 'black', font=lower_font)
     
    order_ticket_file_name =''
    for i in range(10):
        order_ticket_file_name +=  secrets.choice(alphanumerics)

    temp_save_path = f'{staging_path}/'+f'{display_date}:order:'+f'{order_ticket_file_name}.jpg'
    plate_one_half_reverse_template.save(temp_save_path)

    new_qr_size = (300,300)
    pil_image = pil_image.resize(new_qr_size)
    
    order_ticket_qr_code_anchor = ((960-new_qr_size[0]), (955-new_qr_size[1]))
    
    print(order_ticket_qr_code_anchor)
    template  = Image.open(temp_save_path)
    template.paste(pil_image, order_ticket_qr_code_anchor)
    template.save(temp_save_path)
    print(temp_save_path)
    split_list = temp_save_path.split('/')
    print(f'split_list => {split_list}, and length is => {len(split_list)}')
    ret_url =  split_list[-3] + '/' + split_list[-2] + '/' + split_list[-1]
    return {'status':True, 'url':ret_url}



def generate_sale_qrcode_image(data):
    qr = qrcode.QRCode(
        version=2,
        box_size=10,
        border=2
    )
    sales_object = sale(**data['receipt_data'])
    data['receipt_data'] = sales_object.dict()
    sales_data_hash = hash_qrcode_data(data['receipt_data'])
    qr.add_data(sales_data_hash)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color='black', back_color='white')
    print(f'size for qr_image is : {qr_image.size}')
    data['qr_code_size'] = {'width':qr_image.size[0], 'height':qr_image.size[1]}
    data['qr_data_hash'] = sales_data_hash
    return qr_image, data
     


def generate_general_sales_receipt(pil_image, data):
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

    plate_full = Image.open(receipt_templates['plate_one_full'])
    editable_plate_full_template = ImageDraw.Draw(plate_full)
    
   
    next_service_date_display = data['receipt_data']['next_service_date']
    
    editable_plate_full_template.text(header_anchor, data['receipt_data']['heading'], 'black', font=header_font)
    editable_plate_full_template.text(sub_header_anchor, data['receipt_data']['sub_heading'], 'black', font=sub_header_font)
    editable_plate_full_template.text(service_topic_anchor, data['receipt_data']['service_heading'], 'black', font=service_topic_font, anchor='ms')
    editable_plate_full_template.text(next_service_date_anchor, str(next_service_date_display), 'black', font=next_service_date_font, anchor='ms')
    editable_plate_full_template.text(sale_description_anchor, sale_receipt_chunker(20, data['receipt_data']['sale_description']), 'black', font=sale_description_font, anchor='ms')
    editable_plate_full_template.text(sale_amount_anchor, str(comma(data['receipt_data']['sale_amount'])), 'black', font=sale_amount_font, anchor='ms')

    sale_ticket_file_name =''
    for i in range(10):
        sale_ticket_file_name +=  secrets.choice(alphanumerics)

    temp_save_path = f'{staging_path}'+'/'+f'{data["receipt_data"]["sub_heading"]}:receipt:sale:'+f'{sale_ticket_file_name}.png'
    plate_full.save(temp_save_path)

    new_qr_size = (300,300)
    pil_image = pil_image.resize(new_qr_size)
    

    sale_ticket_qrcode_anchor = (960-new_qr_size[0], 400-new_qr_size[1])

    print(sale_ticket_qrcode_anchor)
    template = Image.open(temp_save_path)
    template.paste(pil_image, sale_ticket_qrcode_anchor)
    template.save(temp_save_path)
    print(temp_save_path)
    
    
    
    split_list = temp_save_path.split('/')
    ret_url = split_list[5] + '/' + split_list[6] + '/' + split_list[7]
    return {'status':True, 'url':ret_url}



def generate_vendor_qrcode():
    pass

def generate_vendor_receipt():
    pass 


def decode_binary_receipt(image_binary):
    try:
        return pyzbar.decode(image_binary) 
    except Exception as e:
        return f'unable to decode image binary => {e}'