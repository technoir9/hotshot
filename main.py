# pylint: disable=no-member
from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import os

INPUT_URL = os.environ['INPUT_URL']

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
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

page_content = simple_get(INPUT_URL)
if page_content is None:
    raise Exception('Error - couldn\'t fetch the page')
html = BeautifulSoup(page_content, 'html.parser')
product_name = html.select('#hotShot .product-name')[0].text
image_url = html.select('#hotShot .product-impression > img')[0].get('src')
old_price = html.select('#hotShot .old-price')[0].text
new_price = html.select('#hotShot .new-price')[0].text
