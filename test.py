import pandas as pd
# import seaborn as sns
# import numpy as np


def load_data():
    return pd.read_csv('/homes/ieineke/Documents/kwartaal_6/datadashboards/Dataset/betere_namen/Lifelines_Public_Health_dataset_2024.csv')


def main():
    data = load_data()


if __name__ == '__main__'():
    main()
