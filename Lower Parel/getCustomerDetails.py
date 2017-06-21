import math
import random
import string
import time
import traceback

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from pymongo import MongoClient

import settings

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


def unique_id_gen(prefix='', more_entropy=False):
    m = time.time()
    unique_id = '%8x%05x' % (math.floor(m), (m - math.floor(m)) * 1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0, 10, 1):
            entropy_string += random.choice(valid_chars)
        unique_id = unique_id + entropy_string
    unique_id = prefix + unique_id
    return unique_id


BEST_db = MongoClient('mongodb://localhost:27017')['BEST']
account_numbers = BEST_db['account_numbers_1']
account_details = BEST_db['account_details']

account_url = settings.BEST_BASE_URL + '/QuickPayment.aspx'


def get_view_state(soup_state):
    try:
        view_state = soup_state.findAll(attrs={"name": "__VIEWSTATE"})[0]['value']
    except IndexError:
        view_state = None
    return view_state


def unique_id_gen(prefix='', more_entropy=False):
    m = time.time()
    unique_id = '%8x%05x' % (math.floor(m), (m - math.floor(m)) * 1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0, 10, 1):
            entropy_string += random.choice(valid_chars)
        unique_id = unique_id + entropy_string
    unique_id = prefix + unique_id
    return unique_id


bill_table_mapping = {
    0: 'bill_no',
    1: 'payment_date',
    2: 'payment_received_on',
    3: 'paid_amount',
    4: 'payment_mode',
    5: 'payment_id',
    6: 'transaction_id',
    7: 'receipt_no',
    8: 'pmt_type'
}

get_page = requests.get(account_url, headers=headers)

settings.logger.info("Added 5secs sleep before each request. Don't crash their servers!")
soup = bs(get_page.text, 'html.parser')
view_state = get_view_state(soup)
detail_dict = settings.CUSTOMER_DETAIL_REQUEST
if view_state:
    detail_dict['__VIEWSTATE'] = view_state
settings.logger.info('Fetching User data..')


def extract_node_value(attr_name):
    try:
        node_text = soup2.findAll(attrs={"id": attr_name})[0].text
    except Exception as e:
        node_text = None
    return node_text

cursor = account_numbers.find({'extracted': {'$exists': False}}, no_cursor_timeout=True)

for account_info in cursor:
    account_num = account_info['account_no']
    settings.logger.info(account_num)
    settings.logger.info('XXXXXXXXXXXXXXXXXX')
    detail_dict['ctl00$Contentplaceholder2$ctl02$txtAccno'] = account_num
    account_request = requests.post(account_url, data=detail_dict, headers=headers)
    soup2 = bs(account_request.text, 'html.parser')
    user_details = {}
    try:
        user_details['account_number'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_LblAccountNumber")
        user_details['customer_name'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_LblCustName")
        user_details['mobile_number'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_lblMobileNumber1")
        print(user_details['mobile_number'])
        user_details['customer_address'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_LblAddress")

        user_details['division'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_LblDivision")
        user_details['ward'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_LblWard")
        user_details['cycle'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_LblCycle")
        user_details['current_bill_details'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_lblMsg")
        user_details['current_bill_date'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_lblBillDate")
        user_details['current_bill_due_date'] = extract_node_value("ctl00_Contentplaceholder2_ctl04_lblDueDate")
        table = soup2.findAll('table', {'id': 'ctl00_Contentplaceholder2_ctl04_gvRecentPayments'})[0].findAll('tr')
        paid_bills_array = []
        for tr in table:
            column_values = tr.findAll('td')
            bill_details = {}
            if column_values:
                for i, value in enumerate(column_values):
                    bill_details[bill_table_mapping[i]] = value.text
                paid_bills_array.append(bill_details)
        user_details['paid_bills'] = paid_bills_array
        settings.logger.info('Inserting user data in DB..')
        try:
            account_details.insert_one(user_details)
        except Exception as e:
            user_details['_id'] = unique_id_gen()
            inserted_data = account_details.insert_one(user_details)
        account_info['extracted'] = True
        account_numbers.save(account_info)
    except Exception as e:
        traceback.print_exc()
    settings.logger.info('Sleeping 5secs')
    time.sleep(10)
cursor.close()
