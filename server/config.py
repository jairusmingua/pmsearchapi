import os 
from dotenv import load_dotenv

load_dotenv()

class Config():
    def __init__(self) -> None:
        self.environment = os.environ['ENVIRONMENT']
        self.debug = bool(os.environ['DEBUG'])
        self.postgres_url = str(os.getenv('DATABASE_URL')) or None
        self.allowed_hosts = str(os.environ['ALLOWED_HOSTS']).strip().split(',')

config = Config()