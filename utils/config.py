import os
from dotenv import load_dotenv
load_dotenv()

SCRIPT_ENV = os.environ['SCRIPT_ENV']
if SCRIPT_ENV == 'production':
    WEBHOOK_URL = os.environ['HOTSHOT_WEBHOOK']
else:
    WEBHOOK_URL = os.environ['TEMP_WEBHOOK']
INPUT_URL = os.environ['INPUT_URL']
PROXY_URL = os.environ['FIXIE_URL']
