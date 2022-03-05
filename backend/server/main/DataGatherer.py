import logging
import pandas as pd


def getData():

    # Loeme sisse
    data = pd.read_csv('server/main/finalData.csv')
    #data = pd.read_csv('backend/server/main/finalData.csv')
    logging.info("Data row count {}".format(len(data.index)))
    #print(data.head)
    #print(data)

    return data
