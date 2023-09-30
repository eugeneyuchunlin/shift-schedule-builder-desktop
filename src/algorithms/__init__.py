import yaml
import sys
with open("config.yml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader) 
    dau_url = config['dau_url']
    dma_url = config['dma_url']
    api_key = config['dau_api_key']
    dma_api_key = config['dma_api_key']
    MONGODB_URI = config['mongodb_uri']