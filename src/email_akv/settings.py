import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD')

