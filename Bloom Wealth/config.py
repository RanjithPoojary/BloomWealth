import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dummy-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mutual_fund.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RAPID_API_KEY = os.environ.get('RAPID_API_KEY')
    RAPID_API_HOST = os.environ.get('RAPID_API_HOST')

    FUNDS_PER_PAGE = 30