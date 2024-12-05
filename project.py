
import pandas as pd
from configparser import ConfigParser
# import seaborn as sns
# import numpy as np


# config file

def read_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    return config


config = read_config("config.ini")
# mulecules_file = config['FILES']['molecules']
data_path = config['FILES']['data']


def load_data():
    return pd.read_csv(data_path)


def main():
    data = load_data()


if __name__ == '__main__'():
    main()
