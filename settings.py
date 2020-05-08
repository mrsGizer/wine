import os
from dotenv import load_dotenv
from environs import Env

load_dotenv()

env = Env()
env.read_env()

DATA_FILE = os.getenv('DATA_FILE')
