from flask import Flask, jsonify, request, abort, render_template, redirect, session, make_response, json
from api_master import generate_instaticket_qrcode_image, generate_instaticket_big, generate_order_qrcode_image, generate_order_ticket, generate_sale_qrcode_image, generate_general_sales_receipt, secrets
server = Flask(__name__)
server.secret_key = b"Z'(\xac\xe1\xb3$\xb1\x8e\xea,\x06b\xb8\x0b\xc0"



session_middleware = {
    "Anonymous": {"allowed_routes": ['/', '/about']},
    "Admin" : {"allowed_routes":['/shop',]},  
}

def is_web_user_active():
    if 'session_user' in session :
        print("cookie session_user in place")
        return {"status":True, "middleware":session_middleware[session['session_user'].decode('utf-8').split(':')[0]] }
    else:
        reset_web_user_session()
        return {"status":False, "middleware":session_middleware['Anonymous'] }

def reset_web_user_session():
    session.clear()
    session['session_user'] = b'Anonymous'

def login_web_user(session_key_string):
    pass 

def load_web_user_from_session(session_key_string):
    pass 

def load_shop_data():
    import json
    json_file = open("shop_config.json")
    data = json.load(json_file)
    print(type(data))
    return data

   
@server.route('/')
def process_landing_webpage():
    query = is_web_user_active()
    print(f"query return type is, {type(query)}")
    if query['status'] and request.path in query['middleware']['allowed_routes']:
        print(request.path)
        response = make_response(render_template(
        'welcome.html',
        is_active = False,
        title=load_shop_data()['shop_name'],
        user_type=session['session_user'].decode('utf-8'),
        shop_data = [load_shop_data()]
        ))  
        return response
    return redirect(query['middleware']['allowed_routes'][0])


@server.route('/items_of_sale')
def get_items():
  with open('local_db.json', 'r') as f:
    db = json.load(f)
    items = db['items_of_purchase']
    return jsonify(items)


@server.route('/business_items_of_sale')
def get_business_items():
  with open('local_db.json', 'r') as f:
    db = json.load(f)
    items = db['business_items_of_sale']
    return jsonify(items)


@server.route('/about_info')
def get_about_info():
  with open('local_db.json', 'r') as f:
    db = json.load(f)
    items = db['about_shop']
    return jsonify(items)


@server.route('/shop_config')
def fetch_shop_meta():
    return load_shop_data()


@server.route('/request_order', methods=['POST'])
def process_order_request():
    json_data = request.get_json()
    print(f'recieved json data is : {json_data}')
    res = generate_order_qrcode_image(json_data)
    return generate_order_ticket(res[0], res[1])



if __name__ == '__main__':
    server.run(port=5013, debug=True)