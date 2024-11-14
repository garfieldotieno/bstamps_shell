from api_master.db import base_bot_db
from pydantic import BaseModel
from api_master import datetime, timedelta, time
import uuid


class BaseModel:
    def __init__(self, **data):
        if 'id' in data:
            self.id = data.pop('id')
        else:
            self.id = base_bot_db.incr(f"{self.__class__.__name__.lower()}_counter")
        
        if 'uid' in data:
            self.uid = data.pop('uid')
        else:
            self.uid = str(uuid.uuid4())
        
        if 'timestamp' in data:
            self.timestamp = data.pop('timestamp')
        else:
            self.timestamp = time.time()
        
        for field, value in data.items():
            setattr(self, field, value)

    # def dict(self):
    #     return {field: getattr(self, field) for field in self.__dict__ if not field.startswith('_')}


class UserSessionProfile(BaseModel):
    id: int
    uid: str
    is_admin: bool = False
    is_authorized: bool = False
    bot_id: str 
    # WEB_BOT. *TEL_BOT, Rest_BOT
    activity_json: dict = {}
    response_json: dict = {}
    session_duration: float = 30 * 60
    last_activity_time: float = time.time()
    timestamp: float = time.time()

    def __init__(self, **data):
        super().__init__(**data)
    


    @classmethod
    def get_all(cls):
        session_profiles = []
        profile_keys = base_bot_db.lrange("user_session_profile_listing", 0, -1)
        for key in profile_keys:
            if base_bot_db.sismember("user_session_profile_pool", key):
                key = key.decode('utf-8')
                print(f"key update: {key}")
                profile_data = base_bot_db.json().get(key)
                session_profile = cls(**profile_data)
                session_profiles.append(session_profile)
        return session_profiles


    @classmethod
    def get(cls, id):
        key = f"user_session_profile:{id}"
        if base_bot_db.sismember("user_session_profile_pool", key):
            profile_data = base_bot_db.json().get(key)
            return cls(**profile_data)
        return None


    def save(self):
        profile_data = self.dict()
        key = f"user:{self.uid}:session"  # Use uid as part of the key
        base_bot_db.json().set(key, '.', profile_data)
        base_bot_db.sadd("user_session_profile_pool", key)
        base_bot_db.rpush("user_session_profile_listing", key)
    
    def is_session_expired(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_activity_time
        return (elapsed_time > self.session_duration, elapsed_time)
    

    def expire_session(self, seconds):
        # Set the session expiry time using the EXPIRE command
        key = f"user_session_profile:{self.id}"
        if base_bot_db.sismember("user_session_profile_pool", key):
            base_bot_db.expire(key, seconds)


    def update(self, payload):
        key = f"user_session_profile:{self.id}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)
    
    def delete(self):
        key = f"user_session_profile:{self.id}"
        if base_bot_db.sismember("user_session_profile_pool", key):
            base_bot_db.delete(key)
            base_bot_db.srem("user_session_profile_pool", key)
            base_bot_db.lrem("user_session_profile_listing", 0, key)


    def is_authorized(self):
        session = UserSessionProfile.get(self.user_uid)
        if session:
            return session.is_authorized
        return False


    def get_activity_dict(self):
        if hasattr(self, 'uid'):
            key = f"user:{self.uid}:session"  # Use uid as part of the key
            return base_bot_db.json().get(key, ".activity_json")
        else:
            return None

    def get_response_dict(self):
        if hasattr(self, 'uid'):
            key = f"user:{self.uid}:session"  # Use uid as part of the key
            return base_bot_db.json().get(key, ".response_json")
        else:
            return None



class Item(BaseModel):
    id:int
    uid:str
    public:bool
    item_type:str
    title:str
    name:str
    price:float
    description:str
    item_media_url:str 
    item_media_order_plate_url:str
    item_media_receipt_plate_url:str 
    item_media_instacard_big_plate_url:str 
    item_media_instacard_small_plate_url:str
    timestamp:float = time.time()

    @classmethod
    def get_all(cls):
        items = []
        item_keys = base_bot_db.lrange("item_listing", 0, -1)
        for key in item_keys:
            if base_bot_db.sismember("item_pool", key):
                key = key.decode('utf-8')
                item_data = base_bot_db.json().get(key)
                item = cls(**item_data)
                items.append(item)
        return items
    
    @classmethod
    def get(cls, id):
        key = f"item:{id}"
        if base_bot_db.sismember("item_pool", key):
            item_data = base_bot_db.json().get(key)
            return cls(**item_data)
        return None
    
    def save(self):
        item_data = self.dict()
        key = f"item:{self.id}"
        base_bot_db.json().set(key, '.', item_data)
        base_bot_db.sadd("item_pool", key)
        base_bot_db.rpush("item_listing", key)

    def update(self, payload):
        key = f"item:{self.id}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)

    def delete(self):
        key =f"item:{self.id}"
        if base_bot_db.sismember("item_pool", key):
            base_bot_db.delete(key)
            base_bot_db.srem("item_pool", key)
            base_bot_db.lrem("item_listing", 0, key)
 

class Card(BaseModel):
    id:int
    uid:str
    payload:dict 
    timestamp:float = time.time()

    @classmethod
    def get_all(cls):
        cards = []
        card_keys = base_bot_db.lrange("card_listing", 0, -1)
        for key in card_keys:
            if base_bot_db.sismember("card_pool", key):
                key = key.decode('utf-8')
                card_data = base_bot_db.json().get(key)
                card = cls(**card_data)
                cards.append(card)
        return cards
    
    @classmethod
    def get(cls, uid):
        key = f"card:{uid}"
        if base_bot_db.sismember("card_pool", key):
            card_data = base_bot_db.json().get(key)
            return cls(**card_data)
        return None
    
    def save(self):
        card_data = self.dict()
        key = f"card:{self.uid}"
        base_bot_db.json().set(key, '.', card_data)
        base_bot_db.sadd("card_pool", key)
        base_bot_db.rpush("card_listing", key)

    def update(self, payload):
        key = f"card:{self.uid}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)

    def delete(self):
        key = f"card:{self.uid}"
        if base_bot_db.sismember("card_pool", key):
            base_bot_db.delete(f"card:{key}")
            base_bot_db.srem("card_pool", key)
            base_bot_db.lrem("card_listing", 0, key)


class Transaction(BaseModel):
    id: int
    uid:str
    user_type:str
    tx_type: str
    timestamp:float = time.time()

    @classmethod
    def get_all(cls):
        transactions = []
        transaction_keys = base_bot_db.lrange("transaction_listing", 0, -1)
        for key in transaction_keys:
            if base_bot_db.sismember("transaction_pool", key):
                key = key.decode('utf-8')
                transaction_data = base_bot_db.json().get(key)
                transaction = cls(**transaction_data)
                transactions.append(transaction)
        return transactions
    
    @classmethod
    def get(cls, id):
        key = f"transaction:{id}"
        if base_bot_db.sismember("transaction_pool", key):
            transaction_data = base_bot_db.json().get(key)
            return cls(**transaction_data)
        return None
    
    def save(self):
        transaction_data = self.dict()
        key = f"transaction:{self.id}"
        base_bot_db.json().set(key, '.', transaction_data)
        base_bot_db.sadd("transaction_pool", key)
        base_bot_db.rpush("transaction_listing", key)

    def update(self, payload):
        key = f"transaction:{self.id}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)

    def delete(self):
        key =f"transaction:{self.id}"
        if base_bot_db.sismember("transaction_pool", key):
            base_bot_db.delete(key)
            base_bot_db.srem("transaction_pool", key)
            base_bot_db.lrem("transaction_listing", 0, key)


class Payment(BaseModel):
    id:int
    uid:str
    item_uid:str
    amount_asked:float
    amount_received:float
    complete:bool
    customer_uid:str
    payment_type:str 
    customer_name:str
    payment_ref_id:str
    timestamp:float = time.time()


    @classmethod
    def get_all(cls):
        payments = []
        payment_keys = base_bot_db.lrange("payment_listing", 0, -1)
        for key in payment_keys:
            if base_bot_db.sismember("payment_pool", key):
                key = key.decode('utf-8')
                payment_data = base_bot_db.json().get(key)
                payment = cls(**payment_data)
                payments.append(payment)
        return payments
    
    @classmethod
    def get(cls, id):
        key = f"payment:{id}"
        if base_bot_db.sismember("payment_pool", key):
            payment_data = base_bot_db.json().get(key)
            return cls(**payment_data)
        return None
    
    def save(self):
        payment_data = self.dict()
        key = f"payment:{self.id}"
        base_bot_db.json().set(key, '.', payment_data)
        base_bot_db.sadd("payment_pool", key)
        base_bot_db.rpush("payment_listing", key)

    def update(self, payload):
        key = f"payment:{self.id}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)

    def delete(self):
        key = f"payment:{self.id}"
        if base_bot_db.sismember("payment_pool", key):
            base_bot_db.delete(key)
            base_bot_db.srem("payment_pool", key)
            base_bot_db.lrem("payment_listing", 0, key)


class Order(BaseModel):
    id:int
    uid:str
    item_uid:str
    payment_uid:str
    customer_uid:str
    timestamp:float = time.time()

    @classmethod
    def get_all(cls):
        orders = []
        order_keys = base_bot_db.lrange("order_listing", 0, -1)
        for key in order_keys:
            if base_bot_db.sismember("order_pool", key):
                key = key.decode('utf-8')
                order_data = base_bot_db.json().get(key)
                order = cls(**order_data)
                orders.append(order)
        return orders
    
    @classmethod
    def get(cls, id):
        key = f"order:{id}"
        if base_bot_db.sismember("order_pool", key):
            order_data = base_bot_db.json().get(key)
            return cls(**order_data)
        return None
    
    def save(self):
        order_data = self.dict()
        key = f"order:{self.id}"
        base_bot_db.json().set(key, '.', order_data)
        base_bot_db.sadd("order_pool", key)
        base_bot_db.rpush("order_listing", key)

    def update(self, payload):
        key = f"order:{self.id}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)

    def delete(self):
        key = f"order:{self.id}"
        if base_bot_db.sismember("order_pool", key):
            base_bot_db.delete(key)
            base_bot_db.srem("order_pool", key)
            base_bot_db.lrem("order_listing", 0, key)




class Task(BaseModel):
    id:int
    uid:str
    order_uid:str
    next_service_date:float = time.time()
    timestamp:float = time.time()

    @classmethod
    def get_all(cls):
        tasks = []
        task_keys = base_bot_db.lrange("task_listing", 0, -1)
        for key in task_keys:
            if base_bot_db.sismember("task_pool", key):
                key = key.decode('utf-8')
                task_data = base_bot_db.json().get(key)
                task = cls(**task_data)
                tasks.append(task)
        return tasks
    
    @classmethod
    def get(cls, id):
        key = f"task:{id}"
        if base_bot_db.sismember("task_pool", key):
            task_data = base_bot_db.json().get(key)
            return cls(**task_data)
        return None
    
    def save(self):
        task_data = self.dict()
        key = f"task:{self.id}"
        base_bot_db.json().set(key, '.', task_data)
        base_bot_db.sadd("task_pool", key)
        base_bot_db.rpush("task_listing", key)

    def update(self, payload):
        key = f"task:{self.id}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)

    def delete(self):
        key = self.id
        if base_bot_db.sismember("task_pool", key):
            base_bot_db.delete(key)
            base_bot_db.srem("task_pool", key)
            base_bot_db.lrem("task_listing", 0, key)


class Geo(BaseModel):
    id:int
    uid:str
    latitude:float
    longitude:float
    timestamp:float = time.time()

    @classmethod
    def get_all(cls):
        geos = []
        geo_keys = base_bot_db.lrange("geo_listing", 0, -1)
        for key in geo_keys:
            if base_bot_db.sismember("geo_pool", key):
                key = key.decode('utf-8')
                geo_data = base_bot_db.json().get(key)
                geo = cls(**geo_data)
                geos.append(geo)
        return geos
    
    @classmethod
    def get(cls, id):
        key = f"geo:{id}"
        if base_bot_db.sismember("geo_pool", key):
            geo_data = base_bot_db.json().get(key)
            return cls(**geo_data)
        return None
    
    def save(self):
        geo_data = self.dict()
        key = f"geo:{self.id}"
        base_bot_db.json().set(key, '.', geo_data)
        base_bot_db.sadd("geo_pool", key)
        base_bot_db.rpush("geo_listing", key)

    def update(self, payload):
        key = f"geo:{self.id}"
        for field, value in payload.items():
            self.__dict__[field] = value
            base_bot_db.json().set(key, f".{field}", value)

    def delete(self):
        key = self.id
        if base_bot_db.sismember("geo_pool", key):
            base_bot_db.delete(key)
            base_bot_db.srem("geo_pool", key)
            base_bot_db.lrem("geo_listing", 0, key)