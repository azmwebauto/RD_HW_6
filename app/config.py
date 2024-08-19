import logging
import os

from pathlib import Path

from dotenv import load_dotenv

# Root folder path
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Env path
load_dotenv(ROOT_DIR / '.env')

# Db config
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

DB_URI = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/app'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
