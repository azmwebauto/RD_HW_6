import os

from pathlib import Path

from dotenv import load_dotenv

# Root folder path
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Env path
load_dotenv(ROOT_DIR / '.env')

# Db config
DB_URI = os.environ.get('DB_URI')
