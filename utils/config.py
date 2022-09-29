from json import loads

def load_config() -> dict:
    """
    Loads config file
    """
    with open('./config/config.json', 'r', encoding='utf-8') as config_file:
        config_dict = loads(config_file.read())
    return config_dict
