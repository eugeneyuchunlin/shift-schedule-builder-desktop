import yaml
with open("config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    MONGODB_URI = config["mongodb_uri"]