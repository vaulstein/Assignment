import math
import random
import string
import time

import argparse
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from pymongo import MongoClient

import settings

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


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

#switchIP()

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pincode",
                    help="crawl required pincode")
args = parser.parse_args()

if args.pincode:
    pincode_array = [args.pincode]
    collection = 'account_numbers_' + args.pincode
else:
    collection = 'account_numbers'
    pincode_array = []

account_collection = MongoClient('mongodb://localhost:27017')['BEST'][collection]

account_url = settings.BEST_BASE_URL + '/BuildingWiseConsumerDetails.aspx?ReturnURL=quickpayment.aspx'
settings.logger.info('Initial request. Fetching Pin-codes.')
get_pincode_list = requests.get(account_url, headers=headers)

settings.logger.info("Added 5secs sleep before each request. Don't crash their servers!")
soup = bs(get_pincode_list.text, 'html.parser')

view_state = get_view_state(soup)

if not pincode_array:
    for pincode in soup.find_all('option'):
       pin = pincode.text.strip()
       if pin:
           pincode_array.append(pin)


for pin in pincode_array:
    pin_code_dict = settings.PINCODE_RQUEST_DICT
    pin_code_dict['ctl00$Contentplaceholder2$ddlPin'] = pin
    if view_state:
        pin_code_dict['__VIEWSTATE'] = view_state
    settings.logger.info('Fetching Road Names..')
    road_request = requests.post(account_url, data=pin_code_dict, headers=headers)
    settings.logger.info('Sleeping 5 secs..')
    time.sleep(5)
    soup2 = bs(road_request.text, 'html.parser')
    view_state = get_view_state(soup2)
    for road_name in soup2.findAll('select', {'name': 'ctl00$Contentplaceholder2$ddlRoadName'})[0].findAll('option'):
        road = road_name.text.strip()
        if road:
            pin_code_dict = settings.BUILDING_REQUEST_DICT
            if view_state:
                pin_code_dict['__VIEWSTATE'] = view_state
            pin_code_dict['ctl00$Contentplaceholder2$ddlPin'] = pin
            pin_code_dict['ctl00$Contentplaceholder2$ddlRoadName'] = road
            settings.logger.info('Fetching Building data..')
            building_request = requests.post(account_url, data=pin_code_dict, headers=headers)
            settings.logger.info('Sleeping 5 secs..')
            time.sleep(5)
            #switchIP()
            soup3 = bs(building_request.text, 'html.parser')
            view_state = get_view_state(soup3)
            for building_name in soup3.findAll('select', {'name': 'ctl00$Contentplaceholder2$ddlBuildingName'})[
                0].findAll('option'):
                building = building_name.text.strip()
                if building:
                    pin_code_dict = settings.CUSTOMER_REQUEST_DICT
                    if view_state:
                        pin_code_dict['__VIEWSTATE'] = view_state
                    pin_code_dict['ctl00$Contentplaceholder2$ddlPin'] = pin
                    pin_code_dict['ctl00$Contentplaceholder2$ddlRoadName'] = road
                    pin_code_dict['ctl00$Contentplaceholder2$ddlBuildingName'] = building
                    settings.logger.info('Fetching User info..')
                    account_request = requests.post(account_url, data=pin_code_dict, headers=headers)
                    settings.logger.info('Sleeping 5 secs..')
                    time.sleep(10)
                    soup4 = bs(account_request.text, 'html.parser')
                    for account_detail in soup4.findAll('table', {'id': 'ctl00_Contentplaceholder2_gvConsumerDetails'})[
                        0].findAll('tr'):
                        try:
                            account_number, user_name = [i.text for i in account_detail.findAll('td')]
                            user_dict = {'account_no': account_number, 'user_name': user_name, 'pin-code': pin,
                                         'building': building, 'street_name': road}
                            settings.logger.info('Inserting user data in DB..')
                            try:
                                account_collection.insert_one(user_dict)
                            except Exception as e:
                                user_dict['_id'] = unique_id_gen()
                                inserted_data = account_collection.insert_one(user_dict)
                        except ValueError:
                            settings.logger.warn('Empty td')
                            settings.logger.warn({'pin-code': pin,
                                   'building': building, 'street_name': road})
