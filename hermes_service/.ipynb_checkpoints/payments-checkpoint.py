from config.database import hermes_bot_db
from models import PaymentTransaction, SessionLocal


import re
import string
import secrets


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(secrets.choice(letters) for i in range(stringLength))


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


def update_hermes_invoice(telegram_id, invoice_id):
    hermes_bot_db.hset(f"client:{telegram_id}:invoice:{invoice_id}", "status", 1)
    return hermes_bot_db.srem(f"client:{telegram_id}:unsettled_invoices", invoice_id)


def activate_hermes_session(telegram_id):
    hermes_bot_db.smove("client:inactive:sessions", "client:active:sessions", telegram_id)
    hermes_bot_db.set(f"client:{telegram_id}:session", 1)
    if menu_type(telegram_id) == "vendor":
        hermes_bot_db.expire(f"client:{telegram_id}:session", 60*60*72)
    else:
        hermes_bot_db.expire(f"client:{telegram_id}:session", 60*60*24)

def menu_type(telegram_id):
    return hermes_bot_db.get(f"client:{telegram_id}:menu").decode("utf-8")

def master_mpesa_hermes_log(mpesa_string):
    res = process_mpesa_string(mpesa_string)
    payment = {"mpesa_code":res[1], "amount":float(res[3]), 
               "name":res[4]['first_name']+' '+res[4]['second_name'], 
               "mpesa_number":str(res[0]), "date":res[5], 
                "time":res[6]['time']+' '+res[6]['meridien']}
    hermes_bot_db.hmset("payments:master:mpesa_log:{}".format(res[1]),payment)
    
    if hermes_bot_db.sismember("payments:client:unprocessed_payments", res[1]):
        log = hermes_bot_db.hgetall(f"payments:client:mpesa_log:{res[1]}")
        print(log[b'telegram_id'].decode("utf-8"))
        print(update_hermes_invoice(log[b'telegram_id'].decode("utf-8"), log[b'invoice_id'].decode('utf-8')))
        hermes_bot_db.set("client:{}:payment_status".format(log[b'telegram_id'].decode("utf-8")) , 1)
        activate_hermes_session(log[b'telegram_id'].decode("utf-8"))
        record_hermes_transaction(log[b'invoice_id'].decode('utf-8'), payment['mpesa_number'], payment['amount'], payment['name'], payment['date'], payment['time'])
        remove_hermes_client_unprocessed_payments(res[1])
        return 0
    else:
        set_hermes_master_unprocessed_mpesa_payments(res[1])
        return 1

def set_hermes_master_unprocessed_mpesa_payments(code):
    return hermes_bot_db.sadd("payments:master:unprocessed_payments", code)


def remove_hermes_client_unprocessed_payments(code):
    return hermes_bot_db.srem("payments:client:unprocessed_payments", code)


def record_hermes_transaction(transaction_id, invoice_id, client_service_number, amount_received, name, date):
    db = SessionLocal()  # Create a new database session
    try:
        # Prepare the data for export
        data = {
            'transaction_id': transaction_id,
            'invoice_id': invoice_id,
            'client_service_number': client_service_number,
            'amount_received': amount_received,
            'name': name,
            'date': date
        }
        
        # Call the export_transaction function
        export_transaction(data, db)
    finally:
        db.close()  # Ensure the session is closed

def export_transaction(data, db):
    # Create a new PaymentTransaction instance
    transaction = PaymentTransaction(
        transaction_id=data['transaction_id'],
        invoice_id=data['invoice_id'],
        client_service_number=data['client_service_number'],
        amount_received=data['amount_received'],
        name=data['name'],
        date=data['date']  # Assuming date is already a timestamp
    )
    
    # Add the transaction to the session and commit
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    print(f"Transaction exported: {transaction}")