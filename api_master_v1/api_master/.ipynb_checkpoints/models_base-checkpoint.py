from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float, Integer, Text, Boolean, Date, Time, JSON, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

import uuid
import time
import json
import random, string 

# SQLite database connection
DATABASE_URL = "sqlite:///db.sqlite3"

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


class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)  # Updated to accept JSON data
    created_at = Column(Float, default=lambda: time.time())
    updated_at = Column(Float, default=lambda: time.time())

    def __repr__(self):
        return f"id : {self.id}, name : {self.name}"

    # CRUD Operations for Card

    @staticmethod
    def create_card(session, data):
        card = Card(**data)
        session.add(card)
        session.commit()
        return card

    @staticmethod
    def get_all_cards(session):
        return session.query(Card).all()

    @staticmethod
    def get_single_card(session, card_id):
        return session.query(Card).filter(Card.id == card_id).first()

    @staticmethod
    def update_card(session, card_id, data):
        card = session.query(Card).filter(Card.id == card_id).first()
        if card:
            for key, value in data.items():
                setattr(card, key, value)
            session.commit()
            return card
        return None

    @staticmethod
    def delete_card(session, card_id):
        card = session.query(Card).filter(Card.id == card_id).first()
        if card:
            session.delete(card)
            session.commit()
            return card
        return None


    

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)

    location_type = Column(String, nullable=False)
    location_description = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    created_at = Column(Float, default=lambda: time.time())
    updated_at = Column(Float, default=lambda: time.time())

    def __repr__(self):
        return f"id : {self.id}, description : {self.location_description}"

    # CRUD Operations for Location

    @staticmethod
    def create_location(session, data):
        location = Location(**data)
        session.add(location)
        session.commit()
        return location

    @staticmethod
    def get_all_locations(session):
        return session.query(Location).all()

    @staticmethod
    def get_single_location(session, location_id):
        return session.query(Location).filter(Location.id == location_id).first()

    @staticmethod
    def update_location(session, location_id, data):
        location = session.query(Location).filter(Location.id == location_id).first()
        if location:
            for key, value in data.items():
                setattr(location, key, value)
            session.commit()
            return location
        return None

    @staticmethod
    def delete_location(session, location_id):
        location = session.query(Location).filter(Location.id == location_id).first()
        if location:
            session.delete(location)
            session.commit()
            return location
        return None




class Item(Base):
    __tablename__ = 'item'

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

    # CRUD Operations for Item

    @staticmethod
    def create_item(session, data):
        item = Item(**data)
        session.add(item)
        session.commit()
        return item

    @staticmethod
    def get_all_items(session):
        return session.query(Item).all()

    @staticmethod
    def get_single_item(session, item_id):
        return session.query(Item).filter(Item.id == item_id).first()

    @staticmethod
    def update_item(session, item_id, data):
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            session.commit()
            return item
        return None

    @staticmethod
    def delete_item(session, item_id):
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            session.delete(item)
            session.commit()
            return item
        return None
 



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

    # CRUD Operations for Delivery

    @staticmethod
    def create_delivery(session, data):
        delivery = Delivery(**data)
        session.add(delivery)
        session.commit()
        return delivery

    @staticmethod
    def get_all_deliveries(session):
        return session.query(Delivery).all()

    @staticmethod
    def get_single_delivery(session, delivery_id):
        return session.query(Delivery).filter(Delivery.id == delivery_id).first()

    @staticmethod
    def update_delivery(session, delivery_id, data):
        delivery = session.query(Delivery).filter(Delivery.id == delivery_id).first()
        if delivery:
            for key, value in data.items():
                setattr(delivery, key, value)
            session.commit()
            return delivery
        return None

    @staticmethod
    def delete_delivery(session, delivery_id):
        delivery = session.query(Delivery).filter(Delivery.id == delivery_id).first()
        if delivery:
            session.delete(delivery)
            session.commit()
            return delivery
        return None




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

    # CRUD Operations for Invoice

    @staticmethod
    def create_invoice(session, data):
        invoice = Invoice(**data)
        session.add(invoice)
        session.commit()
        return invoice

    @staticmethod
    def get_all_invoices(session):
        return session.query(Invoice).all()

    @staticmethod
    def get_single_invoice(session, invoice_id):
        return session.query(Invoice).filter(Invoice.id == invoice_id).first()

    @staticmethod
    def update_invoice(session, invoice_id, data):
        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            for key, value in data.items():
                setattr(invoice, key, value)
            session.commit()
            return invoice
        return None

    @staticmethod
    def delete_invoice(session, invoice_id):
        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            session.delete(invoice)
            session.commit()
            return invoice
        return None



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

    # CRUD Operations for Payment

    @staticmethod
    def create_payment(session, data):
        payment = Payment(**data)
        session.add(payment)
        session.commit()
        return payment

    @staticmethod
    def get_all_payments(session):
        return session.query(Payment).all()

    @staticmethod
    def get_single_payment(session, payment_id):
        return session.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def update_payment(session, payment_id, data):
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            for key, value in data.items():
                setattr(payment, key, value)
            session.commit()
            return payment
        return None

    @staticmethod
    def delete_payment(session, payment_id):
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            session.delete(payment)
            session.commit()
            return payment
        return None




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

    # CRUD Operations for PaymentTransaction

    @staticmethod
    def create_payment_transaction(session, data):
        payment_transaction = PaymentTransaction(**data)
        session.add(payment_transaction)
        session.commit()
        return payment_transaction

    @staticmethod
    def get_all_payment_transactions(session):
        return session.query(PaymentTransaction).all()

    @staticmethod
    def get_single_payment_transaction(session, transaction_id):
        return session.query(PaymentTransaction).filter(PaymentTransaction.transaction_id == transaction_id).first()

    @staticmethod
    def update_payment_transaction(session, transaction_id, data):
        payment_transaction = session.query(PaymentTransaction).filter(PaymentTransaction.transaction_id == transaction_id).first()
        if payment_transaction:
            for key, value in data.items():
                setattr(payment_transaction, key, value)
            session.commit()
            return payment_transaction
        return None

    @staticmethod
    def delete_payment_transaction(session, transaction_id):
        payment_transaction = session.query(PaymentTransaction).filter(PaymentTransaction.transaction_id == transaction_id).first()
        if payment_transaction:
            session.delete(payment_transaction)
            session.commit()
            return payment_transaction
        return None

    

# Enum for ReferralAction type
class ActionType(str, Enum):
    SIGNUP = "signup"
    PURCHASE = "purchase"
    SHARE = "share"

    
# Referral Model
class Referral(Base):
    __tablename__ = 'referral'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)
    description = Column(String, nullable=True)

    referrer_id = Column(Integer, nullable=False)  # ID of the referrer (user who initiated the referral)
    referred_id = Column(Integer, nullable=True)  # ID of the referred user (optional, until they sign up)

    created_at = Column(Float, default=lambda: time.time())
    updated_at = Column(Float, default=lambda: time.time())

    # Relationships
    actions = relationship('ReferralAction', back_populates='referral')
    rewards = relationship('ReferralReward', back_populates='referral')

    def __repr__(self):
        return f"Referral(id={self.id}, referrer_id={self.referrer_id}, referred_id={self.referred_id})"

    @staticmethod
    def create_referral(session, data):
        referral = Referral(**data)
        session.add(referral)
        session.commit()
        return referral

    @staticmethod
    def get_all_referrals(session):
        return session.query(Referral).all()

    @staticmethod
    def get_single_referral(session, referral_id):
        return session.query(Referral).filter(Referral.id == referral_id).first()

    @staticmethod
    def update_referral(session, referral_id, data):
        referral = session.query(Referral).filter(Referral.id == referral_id).first()
        if referral:
            for key, value in data.items():
                setattr(referral, key, value)
            session.commit()
            return referral
        return None

    @staticmethod
    def delete_referral(session, referral_id):
        referral = session.query(Referral).filter(Referral.id == referral_id).first()
        if referral:
            session.delete(referral)
            session.commit()
            return referral
        return None


    
# Referral Action Model
class ReferralAction(Base):
    __tablename__ = 'referral_action'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)

    referral_id = Column(Integer, ForeignKey('referral.id'), nullable=False)
    action_type = Column(String, nullable=False)  # Type of action (e.g., SIGNUP, PURCHASE)
    description = Column(String, nullable=True)  # Optional details about the action

    created_at = Column(Float, default=lambda: time.time())
    updated_at = Column(Float, default=lambda: time.time())

    # Relationships
    referral = relationship('Referral', back_populates='actions')

    def __repr__(self):
        return f"ReferralAction(id={self.id}, referral_id={self.referral_id}, action_type={self.action_type})"

    @staticmethod
    def create_referral_action(session, data):
        referral_action = ReferralAction(**data)
        session.add(referral_action)
        session.commit()
        return referral_action

    @staticmethod
    def get_all_referral_actions(session):
        return session.query(ReferralAction).all()

    @staticmethod
    def get_single_referral_action(session, action_id):
        return session.query(ReferralAction).filter(ReferralAction.id == action_id).first()

    @staticmethod
    def update_referral_action(session, action_id, data):
        referral_action = session.query(ReferralAction).filter(ReferralAction.id == action_id).first()
        if referral_action:
            for key, value in data.items():
                setattr(referral_action, key, value)
            session.commit()
            return referral_action
        return None

    @staticmethod
    def delete_referral_action(session, action_id):
        referral_action = session.query(ReferralAction).filter(ReferralAction.id == action_id).first()
        if referral_action:
            session.delete(referral_action)
            session.commit()
            return referral_action
        return None


    
# Referral Reward Model
class ReferralReward(Base):
    __tablename__ = 'referral_reward'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, unique=True, index=True, default=generate_uid)

    referral_id = Column(Integer, ForeignKey('referral.id'), nullable=False)
    reward_type = Column(String, nullable=False)  # E.g., "discount", "cashback", "points"
    amount = Column(Float, nullable=False)  # Value of the reward
    issued_at = Column(Float, default=lambda: time.time())  # When the reward was issued
    is_redeemed = Column(Integer, default=0)  # Boolean: 0 = not redeemed, 1 = redeemed

    created_at = Column(Float, default=lambda: time.time())
    updated_at = Column(Float, default=lambda: time.time())

    # Relationships
    referral = relationship('Referral', back_populates='rewards')

    def __repr__(self):
        return f"ReferralReward(id={self.id}, referral_id={self.referral_id}, reward_type={self.reward_type})"

    @staticmethod
    def create_referral_reward(session, data):
        referral_reward = ReferralReward(**data)
        session.add(referral_reward)
        session.commit()
        return referral_reward

    @staticmethod
    def get_all_referral_rewards(session):
        return session.query(ReferralReward).all()

    @staticmethod
    def get_single_referral_reward(session, reward_id):
        return session.query(ReferralReward).filter(ReferralReward.id == reward_id).first()

    @staticmethod
    def update_referral_reward(session, reward_id, data):
        referral_reward = session.query(ReferralReward).filter(ReferralReward.id == reward_id).first()
        if referral_reward:
            for key, value in data.items():
                setattr(referral_reward, key, value)
            session.commit()
            return referral_reward
        return None

    @staticmethod
    def delete_referral_reward(session, reward_id):
        referral_reward = session.query(ReferralReward).filter(ReferralReward.id == reward_id).first()
        if referral_reward:
            session.delete(referral_reward)
            session.commit()
            return referral_reward
        return None









