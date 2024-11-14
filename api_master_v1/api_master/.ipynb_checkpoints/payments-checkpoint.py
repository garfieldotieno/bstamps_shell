from api_master.db import hermes_bot_db, mk40_bot_db, blu_bot_db

from api_master import Mk40Markup

import re
from api_master import string
import secrets

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('api_master/My First Project-6656111849f6.json', scope)

gc = gspread.authorize(credentials)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(secrets.choice(letters) for i in range(stringLength))


def process_mpesa_string(mpesa_string):
    phone = re.search(r'\d{10}', mpesa_string).group()
    code = re.search(r'^\w*', mpesa_string).group()
    payment_type = "Recieved" if re.search(r'Confirmed', mpesa_string).group() == "Confirmed" else "Reversal"
    amount = float(re.search(r'Ksh\d*.\d*', mpesa_string).group().replace(",", "")[3:])
    person_names = {"first_name":re.search(r'from.\w*\s\w*', mpesa_string).group().split(" ")[1], "second_name":re.search(r'from.\w*\s\w*', mpesa_string).group().split(" ")[2]}
    pay_date = re.search(r'\son\s\w.*\sat', mpesa_string).group().split(" ")[2]
    pay_time = {"time":re.search(r'at\s[0-9]+:[0-9][0-9]\s\w*', mpesa_string).group().split(" ")[1], "meridien":re.search(r'at\s[0-9]+:[0-9][0-9]\s\w*', mpesa_string).group().split(" ")[2]}
    return [phone, code, payment_type, amount, person_names, pay_date, pay_time]


def update_hermes_invoice(telegram_id, invoice_id):
    hermes_bot_db.hset(f"client:{telegram_id}:invoice:{invoice_id}", "status", 1)
    return hermes_bot_db.srem(f"client:{telegram_id}:unsettled_invoices", invoice_id)

def update_blue_invoice(telegram_id, invoice_id):
    blu_bot_db.hset(f"client:{telegram_id}:invoice:{invoice_id}", "status", 1)
    return blu_bot_db.srem(f"client:{telegram_id}:unsettled_invoices", invoice_id)


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

def master_mpesa_blue_log(mpesa_string):
    print("executing master_mpesa_blue_log")
    res = process_mpesa_string(mpesa_string)
    payment = {"mpesa_code":res[1], "amount":float(res[3]), 
               "name":res[4]['first_name']+' '+res[4]['second_name'], 
               "mpesa_number":str(res[0]), "date":res[5], 
                "time":res[6]['time']+' '+res[6]['meridien']}
    print("payment details are:")
    blu_bot_db.hmset("payments:master:mpesa_log:{}".format(res[1]),payment)
    if blu_bot_db.sismember("payments:client:unprocessed_payments", res[1]):
        log = blu_bot_db.hgetall(f"payments:client:mpesa_log:{res[1]}")
        print("the log fetched is:\n")
        print(log)
        # print(log[b'telegram_id'].decode("utf-8"))

        update_blue_invoice(log[b'telegram_id'].decode("utf-8"), log[b'invoice_id'].decode('utf-8'))
        blu_bot_db.set("client:{}:payment_status".format(log[b'telegram_id'].decode("utf-8")) , 1)
        record_blue_transaction(log[b'invoice_id'].decode('utf-8'), payment['mpesa_number'], payment['amount'], payment['name'], payment['date'], payment['time'])
        remove_blue_client_unprocessed_payments(res[1])
        return 0
    else:
        set_blue_master_unprocessed_mpesa_payments(res[1])
        return 1

def set_hermes_master_unprocessed_mpesa_payments(code):
    return hermes_bot_db.sadd("payments:master:unprocessed_payments", code)

def set_blue_master_unprocessed_mpesa_payments(code):
    return blu_bot_db.sadd("payments:master:unprocessed_payments", code)

def remove_hermes_client_unprocessed_payments(code):
    return hermes_bot_db.srem("payments:client:unprocessed_payments", code)

def remove_blue_client_unprocessed_payments(code):
    return blu_bot_db.srem("payments:client:unprocessed_payments", code)


def record_hermes_transaction(invoice_id, client_service_number, amount_recieved, name, date, time):
    transaction_id = mk40_bot_db.incr("payments:transaction:count")
    record = {"transaction_id":transaction_id, "invoice_id":invoice_id, 
              "client_service_number":client_service_number, "amount":amount_recieved,
              "name":name, 
              "date":date, "time":time
             }
    export_data = [transaction_id, invoice_id, client_service_number, amount_recieved, name, date, time]
    export_transaction(export_data)
    return hermes_bot_db.hmset("payment:transaction:{}".format(transaction_id), record)

def record_blue_transaction(invoice_id, client_service_number, amount_recieved, name, date, time):
    transaction_id = mk40_bot_db.incr("payments:transaction:count")
    record = {"transaction_id":transaction_id, "invoice_id":invoice_id, 
              "client_service_number":client_service_number, "amount":amount_recieved,
              "name":name, 
              "date":date, "time":time
             }
    export_data = [transaction_id, invoice_id, client_service_number, amount_recieved, name, date, time]
    export_transaction(export_data)
    return blu_bot_db.hmset("payment:transaction:{}".format(transaction_id), record)

def export_transaction(data):
    work_sheet = gc.open('mk40').sheet1
    work_sheet.append_row(data)

