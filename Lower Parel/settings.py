import logging


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

BEST_BASE_URL = 'https://www.bestundertaking.net'

# Only one request header required. But it works

PINCODE_RQUEST_DICT = {

}

BUILDING_REQUEST_DICT = {

}

CUSTOMER_REQUEST_DICT = {

}

CUSTOMER_INITIAL_REQUEST = {
}

CUSTOMER_DETAIL_REQUEST = {
}
