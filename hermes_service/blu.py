import redis
import time
import json
from payments import process_mpesa_string
import re

from config.database import hermes_bot_db


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
        print(f"fetched value is : {fetch} and is type : {type(fetch)}")
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
        return hermes_bot_db.hmset(key, {'sub1_menu_nav':1, 'sub1_menu_select':select, 'main_menu_nav':0}) 

    @staticmethod
    def get_sub1_menu_select(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hget(key, "sub1_menu_select")

    @staticmethod
    def off_sub1_menu_nav(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hmset(key, {'sub1_menu_nav':0, 'sub1_menu_select':'', 'main_menu_nav':1}) 

    
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
        return hermes_bot_db.hmset(key, {'sub2_menu_nav':1, 'sub2_menu_select':select})  
    
    @staticmethod
    def get_sub2_menu_select(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hget(key, "sub2_menu_select").decode('utf-8')
    

    @staticmethod
    def off_sub2_menu_nav(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hset(key, 'sub2_menu_nav', 0) 

    

    
    
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
        if Session.is_submenu_browsing(waid) == 1:
            print(f"calling reset navigation, sub_menu navigation")
            pass 
        else:
            print(f"calling reset navigation, main_menu navigation")
            pass
        key=f"session:{waid}"
        update_dict = {
            'main_menu_nav':1,
            'main_menu_select':'',
            'sub1_menu_nav':0,
            'sub1_menu_select':'',
            'sub2_menu_nav':0,
            'sub2_menu_select':''
        }
        hermes_bot_db.hmset(key,update_dict)


    # slot_filling navigation
    @staticmethod
    def is_slot_filling(waid):
        user_session = Session.get_session(waid)
        if user_session[b'slot_filling'].decode('utf-8') == '0':
            return False 
        else:
            return True
        
    @staticmethod
    def set_slot_filling_on(waid):
        user_session = Session.get_session(waid)
        print(f"setting slot filling on, session:{user_session}")
        return hermes_bot_db.hset(f"session:{waid}", "slot_filling", 1)
    
    @staticmethod
    def off_slot_filling(waid):
        key=f"session:{waid}"
        return hermes_bot_db.hset(key, "slot_filling", 0)
    
    @staticmethod
    def load_handler(waid, handler, slot_code, current_slot_count, quiz_count):
        key = f"session:{waid}"

        print(f"calling load_handler function, and key is :{key}")

        update = {"current_slot_handler":handler, 
                "current_slot_code":slot_code, 
                "current_slot_count":current_slot_count,
                "slot_quiz_count":quiz_count,
                "slot_filling":1,
                "main_menu_nav":0}
        
        hermes_bot_db.hmset(key, update)
        hermes_bot_db.hset(key, 'main_menu_nav', 0)
    
    
    @staticmethod
    def fetch_slot_details(waid):
        user_session = Session.get_session(waid)
        
        return {
            "slot_code":user_session[b'current_slot_code'].decode('utf-8'),
            "slot_count":user_session[b'current_slot_count'].decode('utf-8'),
            "quiz_count":user_session[b'slot_quiz_count'].decode('utf-8'),
            "slot_handler":user_session[b'current_slot_handler'].decode('utf-8')
        }
    
    @staticmethod
    def return_current_slot_quiz(waid, quiz_payload):
        print(f"recieved slot quiz_pack is {quiz_payload}")
        current_slot_count = hermes_bot_db.hget(f"session:{waid}", "current_slot_count").decode('utf-8')
        print(f"current_slot_count is {current_slot_count}")
        return quiz_payload[current_slot_count]
    
    @staticmethod
    def step_slotting(waid, quiz_payload):
        current_slot_count = hermes_bot_db.hget(f"session:{waid}", "current_slot_count").decode('utf-8')
        quiz_length = len(quiz_payload)
        quiz_index_length = quiz_length - 1
        count_ = int(current_slot_count) 
        print(f"stepping from count_ : {count_}")

        if count_ == quiz_index_length :
            print(f"questions over, not stepping, should be resetting")
            pass 
        elif count_ < quiz_index_length:
            count_ += 1
            hermes_bot_db.hset(f"session:{waid}", "current_slot_count", count_)


    @staticmethod
    def load_ans_payload(waid):
        ans_payload = hermes_bot_db.hget(f"session:{waid}", "answer_payload")
        return ans_payload.decode('utf-8')

    @staticmethod
    def save_reg_answer(waid, curr_count_, ans):
        current_ans_payload = Session.load_ans_payload(waid)
        curr_count = int(curr_count_) - 1
        # new_entry = {curr_count: ans}
        new_entry = ans
        new_payload = ''

        if current_ans_payload == '[]':
            print("Empty answer payload")
            new_payload = json.dumps([new_entry])  # Create a list with the new entry
        else:
            print(f"Not empty answer payload : {current_ans_payload}")
            existing_payload = json.loads(current_ans_payload)
            if len(existing_payload) >= 2:
                existing_payload.append(new_entry)
                new_payload = json.dumps(existing_payload)
                 
            else:
            
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


    # ending slot_filling
    @staticmethod
    def complete_reg_slotting(waid):
        print(f"calling complete registeration function")
        current_ans_payload = Session.load_ans_payload(waid)
        json_loaded = json.loads(current_ans_payload)
        print(f"current answer payload is : {json_loaded}, and type is {type(json_loaded)}")
        payload_length = len(json_loaded)
        print(f"payload length is  {payload_length}")
         
        if payload_length == 2:
            if json_loaded[0] == json_loaded[1]:
                print(f"answer is the same")
                Session.clear_answer_slot(waid)
                return True
            else:
                print(f"answers not the same")
                return False 
        
        if payload_length == 1:
            print(f"current answer is : {json_loaded[0]}")
            return False 

         
    @staticmethod
    def complete_sm_slotting(waid):
        print(f"calling complete send_money function")
        current_ans_payload = Session.load_ans_payload(waid)
        json_loaded = json.loads(current_ans_payload)
        print(f"current answer payload is : {json_loaded}, and type is {type(json_loaded)}")
        payload_length = len(json_loaded)
        print(f"payload length is  {payload_length}")
         
        
        if payload_length == 1:
            print(f"current answer is : {json_loaded[0]}")
            return False
        
        if payload_length == 3:
            print(f"payload_length : {payload_length}")
            if json_loaded[0] == json_loaded[1]:
                print(f"answer is the same")
                # Session.clear_answer_slot(waid)
                return True
            else:
                print(f"answers not the same")
                return False
    
    @staticmethod
    def complete_wd_slotting(waid):
        print(f"calling complete send_money function")
        current_ans_payload = Session.load_ans_payload(waid)
        json_loaded = json.loads(current_ans_payload)
        print(f"current answer payload is : {json_loaded}, and type is {type(json_loaded)}")
        payload_length = len(json_loaded)
        print(f"payload length is  {payload_length}")
         
        
        if payload_length == 2:
            if json_loaded[0] == json_loaded[1]:
                print(f"answer is the same")
                Session.clear_answer_slot(waid)
                return True
            else:
                print(f"answers not the same")
                return False 
        
        if payload_length == 1:
            print(f"current answer is : {json_loaded[0]}")
            return False 
    
    @staticmethod
    def complete_sa_slotting(waid):
        print(f"calling complete set saving percentage")
        current_ans_payload = Session.load_ans_payload(waid)
        json_loaded = json.loads(current_ans_payload)
        print(f"current answer payload is : {json_loaded}, and type is {type(json_loaded)}")
        payload_length = len(json_loaded)
        print(f"payload length is  {payload_length}")
         
        
        if payload_length == 2:
            if json_loaded[0] == json_loaded[1]:
                print(f"answer is the same")
                Session.clear_answer_slot(waid)
                return True
            else:
                print(f"answers not the same")
                return False 
        
        if payload_length == 1:
            print(f"current answer is : {json_loaded[0]}")
            return False 
         


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