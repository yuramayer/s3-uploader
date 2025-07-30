"""App keys for the python script"""

import os
from dotenv import load_dotenv

load_dotenv()


CLOUD_S3_ID_KEY = str(os.getenv('CLOUD_S3_ID_KEY'))
CLOUD_S3_SECRET_KEY = str(os.getenv('CLOUD_S3_SECRET_KEY'))
BUCKET_NAME = str(os.getenv('BUCKET_NAME'))
ADMIN_LOGIN = str(os.getenv("ADMIN_LOGIN"))
ADMIN_PASSWORD = str(os.getenv("ADMIN_PASSWORD"))
