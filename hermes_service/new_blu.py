import random, string, time 
import redis 
from redis.commands.json.path import Path

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)



class Session:
    def __init__(self, uid, waid, name, current_menu_code, browsing_count, main_menu_nav,
                 main_menu_select, sub1_menu_nav, sub1_menu_select, sub2_menu_nav,
                 sub2_menu_select, slot_filling, answer_payload, user_flow,
                 current_slot_code, current_slot_count, slot_quiz_count,
                 current_slot_handler, session_active, session_type):
        self.uid = uid
        self.waid = waid
        self.name = name or ''
        self.current_menu_code = current_menu_code
        self.browsing_count = browsing_count
        self.main_menu_nav = main_menu_nav
        self.main_menu_select = main_menu_select
        self.sub1_menu_nav = sub1_menu_nav
        self.sub1_menu_select = sub1_menu_select
        self.sub2_menu_nav = sub2_menu_nav
        self.sub2_menu_select = sub2_menu_select
        self.slot_filling = slot_filling
        self.answer_payload = answer_payload if answer_payload is not None else []
        self.user_flow = user_flow
        self.current_slot_code = current_slot_code
        self.current_slot_count = current_slot_count
        self.slot_quiz_count = slot_quiz_count
        self.current_slot_handler = current_slot_handler
        self.session_active = session_active
        self.session_type = session_type
        self.created_at = time.time()
        self.updated_at = time.time()

    def save(self):
        session_data = {
            'uid': self.uid,
            'waid': self.waid,
            'name': self.name,
            'current_menu_code': self.current_menu_code,
            'browsing_count': self.browsing_count,
            'main_menu_nav': self.main_menu_nav,
            'main_menu_select': self.main_menu_select,
            'sub1_menu_nav': self.sub1_menu_nav,
            'sub1_menu_select': self.sub1_menu_select,
            'sub2_menu_nav': self.sub2_menu_nav,
            'sub2_menu_select': self.sub2_menu_select,
            'slot_filling': self.slot_filling,
            'answer_payload': self.answer_payload,
            'user_flow': self.user_flow,
            'current_slot_code': self.current_slot_code,
            'current_slot_count': self.current_slot_count,
            'slot_quiz_count': self.slot_quiz_count,
            'current_slot_handler': self.current_slot_handler,
            'session_active': self.session_active,
            'session_type': self.session_type,
            'created_at': self.created_at,
            'updated_at': time.time()
        }

        # Save JSON to Redis
        redis_client.json().set(f"session:{self.waid}", Path.root_path(), session_data)
        redis_client.sadd("user:set", self.waid)

    
    @staticmethod
    def delete(waid):
        redis_client.delete(f"session:{waid}")
        redis_client.srem("user:set", waid)
    
    @staticmethod
    def general_session_update(waid, session_data):
        """Update session data for a given waid."""
        print(f"calling general session update")
        redis_client.json().set(f"session:{waid}", Path.root_path(), session_data)

    @staticmethod
    def get_session(waid):
        """Retrieve session data for a given waid."""
        session_data = redis_client.json().get(f"session:{waid}")
        return session_data if session_data else None

    @staticmethod
    def get_session_type(waid):
        """Retrieve the session type for a given waid."""
        session_data = Session.get_session(waid)
        if session_data:
            return session_data.get('session_type')
        return None

    @staticmethod
    def is_active(waid):
        """Check if the session is active for a given waid."""
        session_data = Session.get_session(waid)
        if session_data:
            return session_data.get('session_active') == "1"
        return False

    @staticmethod
    def activate_session(waid):
        """Activate the session for a given waid."""
        session_data = Session.get_session(waid)
        if session_data:
            session_data['session_active'] = "1"
            Session.general_session_update(waid, session_data)