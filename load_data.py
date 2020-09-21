import pandas as pd
import numpy as np


class ConversionTable:
    def __init__(self):

        # Read relevant files
        data_sdmt = pd.read_csv('data/sdmt_conversion_table.csv')
        data_bvmt = pd.read_csv('data/bvmt_conversion_table.csv')
        data_cvlt = pd.read_csv('data/cvlt_conversion_table.csv')
        description = open('data_descriptions/conversion_table_description.txt')

        # Create the attributes
        self.sdmt = data_sdmt
        self.bvmt = data_bvmt
        self.cvlt = data_cvlt
        self.description = description.read()


class ReferenceData:

    def __init__(self):

        # read data
        z_data = np.load('./data/z_score_array.npy')

        self.data = z_data
        self.description = 'Numpy array with 100.000 samples from a normal distribution with mean 0 and std 1'
