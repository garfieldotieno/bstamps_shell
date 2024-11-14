from api_master import datetime, timedelta, secrets, string, token_urlsafe, time, philate

import requests

import json

import os

import sys

import yaml

from api_master.models import Transaction, UserSessionProfile

from api_master.db import base_bot_db

import uuid

import hashlib

import re

import unittest

# test for dev reset card generation and code

dev_reset_card = {}
dev_reset_card['session_data'] = {}
dev_reset_card['print_data'] = {}
dev_reset_card['verity_data'] = {}


dev_reset_card['session_data']['card_type'] = "Auth_Reset_Card"
dev_reset_card['session_data']['level'] = 0
dev_reset_card['session_data']['session_type']= "Developer"
dev_reset_card['session_data']['redeem_code']= True
dev_reset_card['session_data']['redeem_code_value']= ''
dev_reset_card['session_data']['duration_in_seconds'] = 60*60
dev_reset_card['session_data']['active_days'] = 7

# auth_reset_card['print_data']['item_id'] = 28
dev_reset_card['print_data']['item_media_plate_url'] = 'static/media_store/session_plates/plate_session_full_centerd.jpg'
dev_reset_card['print_data']['heading'] = 'Auth'
dev_reset_card['print_data']['sub_heading'] = 'Sub_heading'
dev_reset_card['print_data']['indicator'] = 'Re'



dev_reset_card['created_at'] = time.asctime(time.localtime(time.time()))

local_url = "http://localhost:5009/request_auth_reset_card"

dev_reset_card_req_res = requests.post(local_url, json=dev_reset_card)

dev_reset_card_req_res_dict = dev_reset_card_req_res.json()

print(f" Dict value =>  {dev_reset_card_req_res_dict} \n\n Keys => {dev_reset_card_req_res_dict.keys()}")

