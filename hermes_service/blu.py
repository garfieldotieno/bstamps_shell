import redis
import time
import json
from payments import process_mpesa_string
import re
import string, random
from config.database import hermes_bot_db

def generate_uid(length=10):
    chars = string.ascii_letters  + string.digits
    uid = "".join(random.choice(chars) for _ in range(length))
    return uid

print(f"testing redis connection, {hermes_bot_db.ping()}")

class Session():
    def __init__(
            self,
            uid,
            waid,
            name,

            current_menu_code,

            browsing_count,
            main_menu_nav,
            main_menu_select,
            sub1_menu_nav,
            sub1_menu_select,
            sub2_menu_nav,
            sub2_menu_select,
            
            
            is_slot_filling,
            
            answer_payload,
            user_flow,
            current_slot_code,
            current_slot_count,
            slot_quiz_count,
            current_slot_handler,

            session_active,
            session_type
    ):
        self.uid = uid
        self.waid = waid
        self.name = name

        self.current_menu_code = current_menu_code

        self.browsing_count = browsing_count
        self.main_menu_nav = main_menu_nav
        self.main_menu_select = main_menu_select
        self.sub1_menu_nav = sub1_menu_nav
        self.sub1_menu_select = sub1_menu_select
        self.sub2_menu_nav = sub2_menu_nav
        self.sub2_menu_select = sub2_menu_select

        self.slot_filling = is_slot_filling
        
        self.answer_payload = answer_payload if answer_payload is not None else []
        self.user_flow = user_flow
        self.current_slot_code = current_slot_code
        self.current_slot_count = current_slot_count
        self.slot_quiz_count = slot_quiz_count
        self.current_slot_handler = current_slot_handler

        self.sesion_active = session_active
        self.session_type = session_type


        self.created_at = time.time()
        self.updated_at = time.time()
    
    # session management
    def save(self):
        # Ensure name is set to an empty string if it is None
        if self.name is None:
            self.name = ''

        session_data = {
            'uid': self.uid,
            'waid': self.waid,
            'name': self.name,
            
            'current_menu_code':self.current_menu_code,

            "browsing_count":self.browsing_count,

            'main_menu_nav':self.main_menu_nav,
            'main_menu_select':self.main_menu_select,
            'sub1_menu_nav':self.sub1_menu_nav,
            'sub1_menu_select':self.sub1_menu_select,
            'sub2_menu_nav':self.sub2_menu_nav,
            'sub2_menu_select':self.sub2_menu_select,
            
            'slot_filling': self.slot_filling,  # Serialize the boolean
            
            'answer_payload': self.answer_payload,  # Serialize the list      
            'user_flow': self.user_flow,
            'current_slot_count': self.current_slot_count,
            'current_slot_code':self.current_slot_code,
            'slot_quiz_count': self.slot_quiz_count,
            'current_slot_handler': self.current_slot_handler,

            'session_active':self.sesion_active,
            'session_type':self.session_type,
            
            'created_at': time.time(),
            'updated_at': time.time()
        }

        print(f"checking session_data before : {session_data}")

        for key, value in session_data.items():
            hermes_bot_db.hset(f"session:{self.waid}", key, value)
        hermes_bot_db.sadd("user:set", self.waid)
    

    @staticmethod
    def general_session_update(waid, session_data):
        print(f"\n\ncalling general_session_update\n\n")

        label_key = f"session:{waid}"
        for key, value in session_data.items():
            print(f"now setting : {key}, whose value is : {value}")
            hermes_bot_db.hset(label_key, key, value)

        print(f"\n\n")
        hermes_bot_db.hset(label_key, 'updated_at', time.time())
        new_data = hermes_bot_db.hgetall(label_key) 
        return new_data 
        
    
    @staticmethod
    def get_session(waid):
        if hermes_bot_db.sismember("user:set", waid):
            session_data = hermes_bot_db.hgetall(f"session:{waid}")
            if session_data:
                return session_data
            return None
        return None
    
    def delete(self):
        if hermes_bot_db.sismember("user:set", self.waid):
            hermes_bot_db.srem("user:set", self.waid)
            return hermes_bot_db.delete(f"session:{self.waid}")
        return None
    

    def save_current_input(self, curr_input):
        self.answer_payload.append(curr_input)
        self.updated_at = time.time()
        self.save()
    
    @staticmethod
    def is_active(waid):
        key = f"session:{waid}"
        status = hermes_bot_db.hget(key, 'session_active')
        status=int(status)
        return status
    
    @staticmethod
    def activate_session(waid):
        pass 

    @staticmethod
    def get_session_type(waid):
        key=f"session:{waid}"
        acc_type = hermes_bot_db.hget(key, 'session_type')
        return acc_type
    


    # main_menu navigation
    @staticmethod
    def is_first_time_contact(waid):
        return hermes_bot_db.sismember('user:set', waid)
    
    
    @staticmethod
    def update_session_menu_code(waid,menu_code):
        key = f'session:{waid}'
        hermes_bot_db.hset(key, 'current_menu_code', menu_code)
    
    @staticmethod
    def get_session_menu_code(waid):
        key = f"session:{waid}"
        return hermes_bot_db.hget(key, 'current_menu_code')
    
    @staticmethod
    def update_main_menu_select(waid, menu_code):
        key = f"session:{waid}"
        hermes_bot_db.hset(key, 'main_menu_select', menu_code)
    
    @staticmethod
    def get_main_menu_select(waid):
        key=f"session:{waid}"
        print(f"calling main_menu_select for : {key}")
        return hermes_bot_db.hget(key, "main_menu_select")
    
    @staticmethod
    def on_main_menu_nav(waid,select):
        key=f"session:{waid}"
        update = {
            "main_menu_nav":0,
            "main_menu_select":select
        }
        hermes_bot_db.hmset(key, update)
    
    @staticmethod
    def off_main_menu_nav(waid):
        key=f"session:{waid}"
        update = {
            "main_menu_nav":0,
            "main_menu_select":''
        }
        return hermes_bot_db.hmset(key, update)
    
    
    @staticmethod
    def is_main_menu_nav(waid):
        key=f"session:{waid}"
        fetch = hermes_bot_db.hget(key,"main_menu_nav")
        print(f"is main menu navigation and is type : {type(fetch)}")
        return fetch


    # sub_menu navigation
    @staticmethod
    def is_sub1_menu_navigation(waid):
        key = f"session:{waid}"
        sub_1 = hermes_bot_db.hget(key, "sub1_menu_nav")
        if sub_1 =='1':
            return 1
        else:
            return 0
    
    
         

    @staticmethod
    def on_sub1_menu_nav(waid, select):
        key=f"session:{waid}"
        update_data = {'sub1_menu_nav':"1", 'sub1_menu_select':select, 'main_menu_nav':"0"}
        # return hermes_bot_db.hmset(key, update_data)
        Session.general_session_update(waid,update_data) 

    @staticmethod
    def get_sub1_menu_select(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hget(key, "sub1_menu_select")

    @staticmethod
    def off_sub1_menu_nav(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hmset(key, {'sub1_menu_nav':"0", 'sub1_menu_select':'', 'main_menu_nav':"1"}) 

    
    @staticmethod
    def is_sub2_menu_navigation(waid):
        key = f"session:{waid}"
        sub_2 = hermes_bot_db.hget(key, "sub2_menu_nav")
        if sub_2 == "1":
            return 1
        else:
            return 0
    

    @staticmethod
    def on_sub2_menu_nav(waid, select):
        key=f"session:{waid}"
        return hermes_bot_db.hmset(key, {'sub2_menu_nav':"1", 'sub2_menu_select':select})  
    
    @staticmethod
    def get_sub2_menu_select(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hget(key, "sub2_menu_select")
    

    @staticmethod
    def off_sub2_menu_nav(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hset(key, 'sub2_menu_nav', "0") 

    

    
    
    @staticmethod
    def get_browsing_count(waid):
        key=f"session:{waid}"
        return int(hermes_bot_db.hget(key, "browsing_count"))

    @staticmethod 
    def browse_main(waid, menu_count):
        key=f"session:{waid}"
        current_count = Session.get_browsing_count(waid)
        current_count = current_count+1
        if current_count == menu_count:
            current_count = 0
        
        hermes_bot_db.hset(key,"browsing_count",current_count)
    

    @staticmethod 
    def browse_submain(waid, menu_count):
        key=f"session:{waid}"
        current_count = Session.get_browsing_count(waid)
        current_count = current_count+1
        if current_count == menu_count:
            current_count = 0
        
        hermes_bot_db.hset(key,"browsing_count",current_count)
    
    @staticmethod
    def reset_browsing_count(waid):
        key=f"session:{waid}"
        current_count = 0
        hermes_bot_db.hset(key,"browsing_count",current_count)

        

    @staticmethod
    def reset_navigation(waid):
        print(f"calling reset_navigation")
        
        update_dict = {
            'main_menu_nav':"1",
            'main_menu_select':'',
            'sub1_menu_nav':"0",
            'sub1_menu_select':'',
            'sub2_menu_nav':"0",
            'sub2_menu_select':'',
            'current_menu_code':'',
            "slot_filling":"0",
            "current_slot_count":"0",
            "current_slot_code":'',
            "slot_quiz_count":"0",
            "current_slot_handler":''
        }
        Session.general_session_update(waid, update_dict)


    # slot_filling navigation
    @staticmethod
    def is_slot_filling(waid):
        user_session = Session.get_session(waid)
        if user_session['slot_filling'] == '0':
            return False 
        else:
            return True
        
    @staticmethod
    def set_slot_filling_on(waid):
        user_session = Session.get_session(waid)
        print(f"setting slot filling on, session:{user_session}")
        return hermes_bot_db.hset(f"session:{waid}", "slot_filling", "1")
    
    @staticmethod
    def off_slot_filling(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hset(key, "slot_filling", "0")
    
    @staticmethod
    def load_handler(waid, handler, slot_code, current_slot_count, quiz_count):
        
        print(f"calling load_handler function, and key is session:{waid}")

        update_dict = {
                "main_menu_nav":"0",
                "slot_filling":"1",
                "current_slot_count":current_slot_count,
                "current_slot_code":slot_code,
                "slot_quiz_count":quiz_count,
                "current_slot_handler":handler
                }
        
        Session.general_session_update(waid, update_dict)
        hermes_bot_db.hset(f"session:{waid}", "main_menu_nav", "0")
    

    @staticmethod
    def fetch_slot_details(waid):
        user_session = Session.get_session(waid)
        
        return {
            "slot_code":user_session['current_slot_code'],
            "slot_count":user_session['current_slot_count'],
            "quiz_count":user_session['slot_quiz_count'],
            "slot_handler":user_session['current_slot_handler']
        }

    @staticmethod
    def return_current_slot_quiz(waid, quiz_payload):
        print(f"\n\nrecieved slot quiz_pack is {quiz_payload}\n\n")
        current_slot_count = hermes_bot_db.hget(f"session:{waid}", "current_slot_count")
        print(f"\n\ncurrent_slot_count is {current_slot_count}\n\n")
        # return quiz_payload[int(current_slot_count)]
        return quiz_payload[current_slot_count]
        
    @staticmethod
    def slot_answer(user_id, slot_quiz_count, ans, SlotQuestion, db, slot_code):
        print(f"calling slot_answer function")
        
        quiz_pack = SlotQuestion.get_slot_questions(db, slot_code)
        Session.save_ans(user_id, ans)
        
        if Session.step_slotting(user_id, quiz_pack):
            
            next_quiz = Session.return_current_slot_quiz(user_id, quiz_pack)
            return next_quiz 
        
        else:
            print(f"should be clearing slot attributes\nand returning complete message")
            # Session.clear_answer_slot(user_id)
            next_quiz = "Congratulations, you have finished entering the required input. Please wait for the next message prompt!"
            return next_quiz
            
    
    @staticmethod
    def step_slotting(waid, quiz_payload):
        print(f"\n\njust called step slotting\n\n")
        
        current_slot_count = hermes_bot_db.hget(f"session:{waid}", "current_slot_count")
        
        quiz_length = len(quiz_payload)
        quiz_index_length = quiz_length - 1

        count_ = int(current_slot_count) 
        print(f"stepping from count_ : {count_}, while quiz_index_length : {quiz_index_length}")

        if count_ == quiz_index_length :
            print(f"questions over, not stepping, should be resetting")
            return False 

        elif count_ < quiz_index_length:
            count_ += 1
            hermes_bot_db.hset(f"session:{waid}", "current_slot_count", count_)
            return True 

    @staticmethod
    def load_ans_payload(waid):
        ans_payload = hermes_bot_db.hget(f"session:{waid}", "answer_payload")
        
        return ans_payload



    @staticmethod
    def save_ans(waid,ans):
        print(f"\n\nsaving answer as follows : {ans}\n\n")

        current_ans_payload = Session.load_ans_payload(waid)
        # curr_count = int(curr_count_) - 1
        # new_entry = {curr_count: ans}
        new_entry = ans
        new_payload = ''

        if current_ans_payload == '[]':
            print("Empty answer payload")
            new_payload = json.dumps([new_entry])  # Create a list with the new entry
        else:
            print(f"Not empty answer payload : {current_ans_payload}")
            existing_payload = json.loads(current_ans_payload)

            current_quiz_count = hermes_bot_db.hget(f"session:{waid}", "slot_quiz_count")
            
            print(f"fetched current_quiz_count, {current_quiz_count}")
            
            existing_payload.append(new_entry)
            new_payload = json.dumps(existing_payload)

        # Save the updated payload back to the session
        session = Session.get_session(waid)
        print(f"fetched session is : {session}")
        if session:
            hermes_bot_db.hmset(f"session:{waid}", {
                "answer_payload":new_payload,
                "updated_at":time.time()
            })


    @staticmethod
    def clear_answer_slot(waid):
        hermes_bot_db.hset(f"session:{waid}", "answer_payload", '[]')


    # first redeem_session
    @staticmethod
    def verify_input_code_match(test_waid, input_two):
        ans_list = json.loads(Session.load_ans_payload(test_waid))
        input_value_1 = ans_list[1]
        input_value_2 = input_two
        if input_value_1 == input_value_2:
            return True
        else:
            return False
    
    @staticmethod
    def verify_code(input_value):
        code_value = f"redeem:code:{input_value}"
        print(f"calling verify code, and code value is : {code_value}")
        if hermes_bot_db.sismember('session_redeem_code', code_value):
            return code_value 
        else:
            return None
    
    @staticmethod 
    def generate_redeem_code():
        print(f"calling generate_redeem_code")
        four_digit_code = generate_uid(6)
        four_digit_code = four_digit_code.lower()
        key = f"redeem:code:{four_digit_code}"
        hermes_bot_db.sadd('session_redeem_code', key)
        return four_digit_code


    @staticmethod
    def complete_R_S_H(waid):
        print(f"\n\ncalling complete_R_H_S\n\n")
        ans_list = Session.load_ans_payload(waid)
        ans_list = json.loads(ans_list)

        print(f"\nfetched ans_list is : {ans_list}, and is type : {type(ans_list)}\n")
        
        # Check if the length of ans_list is greater than 3
        if len(ans_list) > 3:
            # Trim values from index 2
            print(f"testing trim {ans_list[:3]}")

            ans_list = ans_list[:3]  # Keep only the first two elements
            print(f"Trimmed answer list to: {ans_list}")
        
        # Proceed with the rest of the logic
        if ans_list[0] == 'vendor':
            update_data = {
                'current_menu_code': '',
                'browsing_count': 0,
                'main_menu_nav': 1,
                'main_menu_select': '',
                'sub1_menu_nav': 0,
                'sub1_menu_select': '',
                'sub2_menu_nav': 0,
                'sub2_menu_select': '',
                'slot_filling': 0,
                'answer_payload': '[]',
                'user_flow': '',
                'current_slot_code': '',
                'current_slot_count': 0,
                'slot_quiz_count': '',
                'current_slot_handler': '',
                'session_active': 1,
                'session_type': 'Vendor'
            }

        elif ans_list[0] == 'customer':
            update_data = {
                'current_menu_code': '',
                'browsing_count': 0,
                'main_menu_nav': 1,
                'main_menu_select': '',
                'sub1_menu_nav': 0,
                'sub1_menu_select': '',
                'sub2_menu_nav': 0,
                'sub2_menu_select': '',
                'slot_filling': 0,
                'answer_payload': '[]',
                'user_flow': '',
                'current_slot_code': '',
                'current_slot_count': 0,
                'slot_quiz_count': '',
                'current_slot_handler': '',
                'session_active': 1,
                'session_type': 'Customer'  # Corrected to 'Customer'
            }
        
        Session.general_session_update(waid, update_data)


    
    # first purchase session
    @staticmethod
    def verify_input_mpesa_match(test_waid, input_two):
        ans_list = json.loads(Session.load_ans_payload(test_waid))
        input_value_1 = ans_list[1]
        input_value_2 = input_two 
        if input_value_1 == input_value_2:
            return True
        else:
            return False 
         

    @staticmethod
    def process_mpesa_payment(test_waid, client_input):
        pass

    @staticmethod
    def verify_payment(test_waid):
        pass 

    @staticmethod
    def export_mpesa_payment(mpesa_payload):
        pass 

    
    @staticmethod
    def complete_P_H_S(waid):
        print(f"\n\ncalling complete_P_H_S\n\n")
        ans_list = Session.load_ans_payload(waid)
        ans_list = json.loads(ans_list)

        print(f"\nfetched ans_list is : {ans_list}, and is type : {type(ans_list)}\n")
        
        # Check if the length of ans_list is greater than 3
        if len(ans_list) > 3:
            # Trim values from index 2
            print(f"testing trim {ans_list[:3]}")

            ans_list = ans_list[:3]  # Keep only the first two elements
            print(f"Trimmed answer list to: {ans_list}")
        
        # Proceed with the rest of the logic
        if ans_list[0] == 'vendor':
            update_data = {
                'current_menu_code': '',
                'browsing_count': 0,
                'main_menu_nav': 1,
                'main_menu_select': '',
                'sub1_menu_nav': 0,
                'sub1_menu_select': '',
                'sub2_menu_nav': 0,
                'sub2_menu_select': '',
                'slot_filling': 0,
                'answer_payload': '[]',
                'user_flow': '',
                'current_slot_code': '',
                'current_slot_count': 0,
                'slot_quiz_count': '',
                'current_slot_handler': '',
                'session_active': 1,
                'session_type': 'Vendor'
            }

        elif ans_list[0] == 'customer':
            update_data = {
                'current_menu_code': '',
                'browsing_count': 0,
                'main_menu_nav': 1,
                'main_menu_select': '',
                'sub1_menu_nav': 0,
                'sub1_menu_select': '',
                'sub2_menu_nav': 0,
                'sub2_menu_select': '',
                'slot_filling': 0,
                'answer_payload': '[]',
                'user_flow': '',
                'current_slot_code': '',
                'current_slot_count': 0,
                'slot_quiz_count': '',
                'current_slot_handler': '',
                'session_active': 1,
                'session_type': 'Customer'  # Corrected to 'Customer'
            }
        
        Session.general_session_update(waid, update_data)
         



class BluSlotQuestion():
    pass 

class BluItemInventory():
    pass 

class BluLocation():
    pass 

class BluDelivery():
    pass 

class BluInvoice():
    pass 


class BluPaymentTransaction():

    @staticmethod
    def process_mpesa_string(mpesa_string):
        # Determine if the message is a sent or received message
        if "sent to" in mpesa_string:
            # Sent message pattern
            phone_match = re.search(r'\d{10}', mpesa_string)
            if not phone_match:
                return "wrong sent/payment message input"
            phone = phone_match.group()
            
            code = re.search(r'^\w*', mpesa_string).group()
            payment_type = "Sent"
            amount = float(re.search(r'Ksh([\d,.]+)', mpesa_string).group(1).replace(",", ""))
            
            # Extract names
            person_names_match = re.search(r'sent to\s([\w\s]+)\s(\d{10})', mpesa_string)
            if person_names_match:
                first_name, second_name = person_names_match.group(1).strip().split(" ", 1)
            else:
                first_name, second_name = "Unknown", "Unknown"  # Default values if not found

            pay_date = re.search(r'\son\s(\d{2}/\d{2}/\d{2})', mpesa_string).group(1)
            pay_time = {
                "time": re.search(r'at\s([0-9]+:[0-9][0-9])\s(\w+)', mpesa_string).group(1),
                "meridien": re.search(r'at\s([0-9]+:[0-9][0-9])\s(\w+)', mpesa_string).group(2)
            }
            
        else:
            # Received message pattern
            phone_match = re.search(r'\d{10}', mpesa_string)
            if not phone_match:
                return "wrong sent/payment message input"
            phone = phone_match.group()
            
            code = re.search(r'^\w*', mpesa_string).group()
            payment_type = "Received"
            amount = float(re.search(r'Ksh([\d,.]+)', mpesa_string).group(1).replace(",", ""))
            
            # Extract names
            person_names_match = re.search(r'from\s([\w\s]+)\s(\d{10})', mpesa_string)
            if person_names_match:
                first_name, second_name = person_names_match.group(1).strip().split(" ", 1)
            else:
                first_name, second_name = "Unknown", "Unknown"  # Default values if not found

            pay_date = re.search(r'\son\s(\d{2}/\d{2}/\d{2})', mpesa_string).group(1)
            pay_time = {
                "time": re.search(r'at\s([0-9]+:[0-9][0-9])\s(\w+)', mpesa_string).group(1),
                "meridien": re.search(r'at\s([0-9]+:[0-9][0-9])\s(\w+)', mpesa_string).group(2)
            }

        return [phone, code, payment_type, amount, {"first_name": first_name, "second_name": second_name}, pay_date, pay_time]
 

    def client_mpesa_log():
        pass 

    def backend_mpesa_log():
        pass 

    def match():
        pass 

    def reconcile_payment():
        pass 