from configparser import ConfigParser
import pandas as pd


def read_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    return config


config = read_config("config.ini")
metadata = config['FILES']['metadata']

df = pd.read_csv(metadata, sep=';', header=None)

print(df)