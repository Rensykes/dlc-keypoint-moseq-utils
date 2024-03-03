import os
import configparser

def load_settings():
    """
    Load settings from the configuration file.
    """
    settings_file = "settings.ini"
    settings = {}
    if os.path.exists(settings_file):
        config = configparser.ConfigParser()
        config.read(settings_file)
        if "Settings" in config:
            settings = dict(config["Settings"])
    return settings

def save_settings(**kwargs):
    """
    Save settings to the configuration file.
    """
    settings_file = "settings.ini"
    config = configparser.ConfigParser()
    config["Settings"] = kwargs
    with open(settings_file, "w") as config_file:
        config.write(config_file)