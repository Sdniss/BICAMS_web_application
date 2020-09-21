import numpy as np


def normalization_pipeline(data_vector, raw_score, test, conversion_table, z_cutoff):
    """ Entire normalization pipeline

    :param data_vector: 1-D vector consisting in following order: [age, age^2, sex, education]
    :param raw_score: int, raw score on the test of interest
    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :param conversion_table: pd dataframe, being the conversion table for the test of interest
    :param z_cutoff: float, the value where you want to declare impairment on the cognitive domain
    :returns: z_score: z-score for the test of interest -- impaired_bool: 1 if impaired, 0 if preserved
    """

    expected_score = get_expected_score(data_vector, test)
    scaled_score = raw_to_scaled(raw_score, conversion_table)
    z_score = to_z_score(scaled_score, expected_score, test)
    impaired_bool = impaired_or_not(z_score, z_cutoff)

    return z_score, impaired_bool


def get_expected_score(data_vector, test):
    """ Get the expected score on a subtest of the BICAMS

    :param data_vector: 1-D vector consisting in following order: [age, age^2, sex, education]
    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :return: the expected score on the respective test
    """
    weight_dict = {'sdmt': [10.648, -0.289, 0.002, -0.05, 0.479],
                   'cvlt': [9.052, -0.230, 0.002, -2.182, 0.323],
                   'bvmt': [16.902, -0.473, 0.005, -1.427, 0.341]}

    weight_vector = weight_dict.get(test)
    data_vector = [1] + list(data_vector)  # Add 1 to multiply with bias term in regression equation
    expected_score = np.dot(weight_vector, data_vector)

    return expected_score


def raw_to_scaled(raw_score, conversion_table):
    """ Convert raw score to a categorical, scaled value

    :param raw_score: int, raw score on the test of interest
    :param conversion_table: pd dataframe, being the conversion table for the test of interest
    :return: categorical, scaled score
    """

    scaled_scores = conversion_table.iloc[:,0]
    lower_values = conversion_table.iloc[:,1]
    upper_values = conversion_table.iloc[:,2]

    for scaled_score, lower_value, upper_value in zip(scaled_scores, lower_values, upper_values):
        if lower_value <= raw_score <= upper_value:
            return scaled_score


def to_z_score(scaled_score, expected_score, test):
    """ Turn scaled and expected score to a z score

    :param scaled_score: scaled score, result from raw_to_scaled function
    :param expected_score: expected score, result from get_expected_score function
    :param test: test of interest
    :return: z-score for the test of interest
    """
    denominator_dict = {'sdmt': 2.790,
                        'bvmt': 2.793,
                        'cvlt': 2.801}

    denominator = denominator_dict.get(test)

    z_score = (scaled_score - expected_score)/denominator

    return z_score

def impaired_or_not(z_score, cutoff):
    """ Dichotimize z-score by applying a cutoff

    :param z_score: the z-score, i.e. performance relative to a reference population
    :param cutoff: the cut-off to decide impaired (<=) or preserved (>) on the cognitive domain
    :return: 1 if impaired, 0 if preserved
    """
    if z_score <= cutoff:
        return 1
    else:
        return 0
