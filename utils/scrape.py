# pylint: disable=no-member
import re
import os
import time
from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from utils.config import SCRIPT_ENV, WEBHOOK_URL, INPUT_URL

WAITING_TIME = [1, 5, 30, 90, 300]

def simple_get(url, headers=None):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_discount_percentage(old_price, new_price):
    percentage = (old_price - new_price) / old_price * 100
    return round(percentage, 2)

def run(post_url=WEBHOOK_URL):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "time-zone": "UTC",
        "x-api-key": "sJSgnQXySmp6pqNV"
    }
    response = get(INPUT_URL, headers=headers)
    json_response = response.json()
    product_name = json_response['PromotionName']
    old_price = json_response['OldPrice']
    new_price = json_response['Price']
    items_all = json_response['PromotionTotalCount']
    items_left = json_response['MaxBuyCount']
    discount_percent = get_discount_percentage(old_price, new_price)
    product_url = json_response['PromotionPhoto']['Url']
    message = (
        f"Produkt: {product_name}, stara cena: {old_price}, nowa cena: {new_price}, pozostało sztuk: {items_left}/{items_all}\n"
        f"Obniżka: {discount_percent}%\n"
        f"{product_url}")

    post(post_url, data={'content': message})
