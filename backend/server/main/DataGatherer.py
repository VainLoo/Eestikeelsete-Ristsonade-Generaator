import logging
import pandas as pd


def getData():

    # Loeme sisse
    mainData = pd.read_csv('server/main/finalData.csv')
    fillerData = pd.read_csv('server/main/finalInflections.csv')
    #mainData = pd.read_csv('backend/server/main/finalData.csv')
    #fillerData = pd.read_csv('backend/server/main/finalInflections.csv')
    logging.info("Main data row count {}".format(len(mainData.index)))
    logging.info("Filler data row count {}".format(len(fillerData.index)))

    return mainData, fillerData


