from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float, Integer, Text, Boolean, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import time
import json
import random, string 

# SQLite database connection
DATABASE_URL = "sqlite:///./config/hermes.sqlite3"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_all_tables():
    # Create tables
    Base.metadata.create_all(bind=engine)

def generate_uid(length=10):
    chars = string.ascii_letters  + string.digits
    uid = "".join(random.choice(chars) for _ in range(length))
    return uid

class ItemInventory(Base):
    __tablename__ = 'item_inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    prompt_live_media = Column(Boolean, default=False)

    public = Column(Boolean, default=True)
    item_type = Column(String, nullable=False)

    item_media_url = Column(String, nullable=False)
    item_media_order_plate_url = Column(String, nullable=False)
    item_media_receipt_plate_url = Column(String, nullable=False)
    item_media_instacard_big_plate_url = Column(String, nullable=False)
    item_media_instacard_small_plate_url = Column(String, nullable=False)

    created_at = Column(Float, default=lambda : time.time())
    updated_at = Column(Float, default=lambda : time.time())

    def __repr__(self):
        return f"id : {self.id}, name : {self.name}"

    @staticmethod
    def add_item(db,data):
        pass 

    @staticmethod 
    def redis_step_fill(redis_db_conn, data):
        pass 

    @staticmethod
    def export_to_rdb(redis_item_key):
        pass 


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)
    
    location_type = Column(String, nullable=False)
    location_description = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    created_at = Column(Float, default=lambda : time.time())
    updated_at = Column(Float, default=lambda : time.time())

    def __repr__(self):
        return f"id : {self.id}, description : {self.location_description}"




class Delivery(Base):
    __tablename__ = "delivery"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)
    item_uid = Column(String, nullable=False)

    item_amount = Column(Float, nullable=False)
    delivery_type_amount = Column(Float, nullable=False)
    delivery_total_amount = Column(Float, nullable=False)
    
    delivery_type = Column(String, nullable=False)
    delivery_date = Column(Date, nullable=False)
    delivery_time = Column(Time, nullable=False)
    delivery_description = Column(String, nullable=False)

    delivery_location_uid = Column(String, nullable=False)
    vendor_uid = Column(String, nullable=False)
    customer_uid = Column(String, nullable=False)

    created_at = Column(Float, default=lambda : time.time())
    updated_at = Column(Float, default=lambda : time.time())

    def __repr__(self):
        return f"id:{self.id}, type:{self.delivery_type}"



class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)

    delivery_uid = Column(String, nullable=False)

    delivery_total_amount = Column(Float, nullable=False)
    delivery_complete = Column(Float, default=False)

    payment_status = Column(Boolean, default=False)
    payment_uid = Column(String, nullable=False)

    created_at = Column(Float, default=lambda : time.time())
    updated_at = Column(Float, default=lambda : time.time())

    def __repr__(self):
        return f"id : {self.id}"


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)

    invoice_uid = Column(String, nullable=False)

    payment_method = Column(String, nullable=False)
    payment_external_ref = Column(String, nullable=False)
    payment_total_amount = Column(Float, nullable=False)
    
    payment_reconciled_status = Column(Boolean, default=False)

    created_at = Column(Float, default=lambda : time.time())
    updated_at = Column(Float, default=lambda : time.time())

    def __repr__(self):
        return f"id : {self.id}"



class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String, unique=True, index=True)
    invoice_id = Column(String, index=True)
    client_service_number = Column(String)
    amount_received = Column(Float)
    name = Column(String)
    date = Column(Float, default=lambda: time.time())  # Store as a timestamp
    created_at = Column(Float, default=lambda: time.time())
    
    def __repr__(self):
        return f"PaymentTransaction(transaction_id={self.transaction_id}, amount_received={self.amount_received}, name={self.name})"

    

class SlotQuestion(Base):
    __tablename__ = "slot_question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)
    
    slot_code = Column(String, index=True, unique=True)
    
    slot_description = Column(String)
    question_payload = Column(Text)
    
    created_at = Column(Float, default=lambda: time.time())
    updated_at = Column(Float, default=lambda: time.time())

    def __repr__(self):
        return f"id : {self.id}, slot_code : {self.slot_code}"
    
    @staticmethod
    def add_slot_question(db, slot_code, slot_description, question_payload):
        # Check if a slot question with the same slot_code already exists
        existing_slot_question = db.query(SlotQuestion).filter(SlotQuestion.slot_code == slot_code).first()
        if existing_slot_question:
            raise ValueError(f"Slot question with slot_code {slot_code} already exists.")
        
        slot_question = SlotQuestion(
            slot_code=slot_code,
            slot_description=slot_description,
            question_payload=json.dumps(question_payload)
        )
        db.add(slot_question)
        db.commit()
        db.refresh(slot_question)
        return slot_question

    @staticmethod
    def get_question_pack(db, slot_code):
        print(f"\n\nAttempting get_question_pack\n\n")

        slot_question = db.query(SlotQuestion).filter(SlotQuestion.slot_code == slot_code).first()
        if slot_question:
            print(f"\n\nfetched slot_question is {slot_question.question_payload}\n\n")
            res = json.loads(slot_question.question_payload)
            res = list(res.keys())
            print(f"\n\nres for get_question_pack is : {res}\n\n")
            return res
        
        return None


    @staticmethod
    def get_slot_questions(db,slot_code):
        print(f"\n\n calling get_slot_questions \n\n")
        
        slot_question = db.query(SlotQuestion).filter(SlotQuestion.slot_code == slot_code).first()
        if slot_question:
            print(f"fetched slot_question is : {slot_question.question_payload}")
            res = json.loads(slot_question.question_payload)
            return res
        
        return None

    @staticmethod
    def get_slot_question(db, slot_code):
        slot_question = db.query(SlotQuestion).filter(SlotQuestion.slot_code == slot_code).first()
        if slot_question:
            slot_question_dict = slot_question.__dict__
            slot_question_dict['question_payload'] = json.loads(slot_question_dict['question_payload'])
            return slot_question_dict
        return None



def load_slotquizes(db):
    slot_data = [
        {
            "slot_code": "R_S_H",
            "slot_description" : "Redeem a free session and get 24-hr access to the platform",
            "question_payload" : {
                0 : "Select your preferred session type ",
                1 : "Enter your redeem code to proceed",
                2 : "Confirm code by repeating it"
            }
        },
        {
            "slot_code" : "P_S_H",
            "slot_description" : "Enter M-pesa payment information for generated session invoice",
            "question_payload" : {
                0 : "Select your preffered session type ",
                1 : "Enter M-pesa message for processing\nYou can edit and cut out your balance.",
                2 : "Confirm M-pesa message by repeating it\nYou can edt and cut out your balance"
            }
        },
        {
            "slot_code" : "C_SL_H",
            "slot_description" : "Update your location information",
            "question_payload" : {
                0 : "Enter location pin to update your search location"
            }
        },
        {
            "slot_code" : "V_UL_H",
            "slot_description" : "Update your location information",
            "question_payload" : {
                0 : "Enter your location pin to update your sale location"
            }
        },
        {
            "slot_code" : "V_UIS_H",
            "slot_description" : "Update your item of sale information",
            "question_payload" : {
                0 : "Enter item name",
                1 : "Enter item description",
                2 : "Enter item price",
                3 : "Do you accept live media prompting by customer",
                4 : "Should this item be public or private ?",
                5 : "Select which type of item you are selling",
                6 : "Upload item cover media image",
                7 : "Upload item order plate image",
                8 : "Upload item receipt plate image",
                9 : "Upload item instacard big plate image",
                10: "Upload item instacard small plate image"
            }
        }

    ]
    
    for data in slot_data:
        SlotQuestion.add_slot_question(
            db,
            slot_code=data['slot_code'],
            slot_description=data['slot_description'],
            question_payload=data['question_payload']
        )

    print("Slot quizzes loaded successfully")



# Example usage
if __name__ == '__main__':
    create_all_tables()
    db = SessionLocal()
    load_slotquizes(db)
    db.close()
