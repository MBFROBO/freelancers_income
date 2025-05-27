import yaml
from yaml import load
from pathlib import Path

confs = {}
with open(Path(__file__).parent.absolute() / Path("config.yaml"), 'r') as f:
    confs = load(f, yaml.Loader)

VERSION = confs['version']
MODEL_NAME = confs['LLM_model']['model']
MODEL_URL = confs['LLM_model']['url']
MODEL_API_KEY = confs['LLM_model']['api_key']

DB_HOST = confs['database']['host']
DB_PORT = confs['database']['port']
DB_USER = confs['database']['user']
DB_PASSWORD = confs['database']['password']
DB_NAME = confs['database']['database']