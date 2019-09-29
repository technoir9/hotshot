# pylint: disable=no-member
import re
import os
import time
from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

SCRIPT_ENV = os.environ['SCRIPT_ENV']
if SCRIPT_ENV == 'production':
    WEBHOOK_URL = os.environ['HOTSHOT_WEBHOOK']
else:
    WEBHOOK_URL = os.environ['TEMP_WEBHOOK']
INPUT_URL = os.environ['INPUT_URL']
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

def get_discount_percentage(old_price_str, new_price_str):
    old_price = float(re.sub(r"\D", '', old_price_str))
    new_price = float(re.sub(r"\D", '', new_price_str))
    percentage = (old_price - new_price) / old_price * 100
    return round(percentage, 2)

def run(post_url = WEBHOOK_URL):
    headers = {
        "accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    for x in range(0, 5):
        page_content = simple_get(INPUT_URL, headers=headers)
        if page_content is None:
            raise Exception('Error - couldn\'t fetch the page')
        html = BeautifulSoup(page_content, 'html.parser')
        product_name = html.select('#hotShot .product-name')[0].text
        try:
            items_left = html.select('#hotShot .pull-left > span')[0].text
            print('New product')
            break
        except IndexError:
            print('Product hasn\'t changed')
            items_left = html.select('#hotShot .sold-info')[0].text
            time.sleep(WAITING_TIME[x])
        # recent_product_name = file_utils.get_last_product()
        # if recent_product_name == product_name:
        #     print('Product hasn\'t changed')
        #     time.sleep(WAITING_TIME[x])
        # else:
        #     print('New product')
        #     file_utils.write_last_product(product_name)
        #     break
    try:
        hotshot_script = html.select('#hotShot + script')[0].text
        product_url = INPUT_URL + re.search(r"(goracy.+?)\"", hotshot_script)[1]
    except IndexError:
        # image url
        product_url = html.select('#hotShot .product-impression > img')[0].get('src')
    old_price = html.select('#hotShot .old-price')[0].text
    new_price = html.select('#hotShot .new-price')[0].text

    discount_percent = get_discount_percentage(old_price, new_price)

    message = (
        f"Produkt: {product_name}, stara cena: {old_price}, nowa cena: {new_price}, pozostało sztuk: {items_left}\n"
        f"Obniżka: {discount_percent}%\n"
        f"{product_url}")
    post(post_url, data={'content': message})
