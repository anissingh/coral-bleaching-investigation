"""CSC110 Fall 2020 Final Project: Reading CSV Data

Information
===============================
This Python module contains the functions that will be used to process the raw csv
data from the dataset I will be using so that I can compute on the data present
inside the dataset.

Copyright Information
===============================
This file is Copyright (c) 2020 Anis Singh.
"""

import csv
from typing import Dict, List
import pandas as pd


def read_csv_data_ssta(filepath: str) -> Dict[float, List[float]]:
    """Return a dictionary mapping the severity of a coral bleaching event
    (represented numerically) to a list of SSTAs (Sea Surface Temperature Anomalies)
    (in degrees Celsius) that were present when such a severe bleaching event occurred.

    Preconditions:
        - filepath refers to a csv file in the format of
          data/coral_bleaching_data.csv
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        bleaching_data = {}

        for row in reader:
            # Skip the row if there is no SSTA data for a coral bleaching event
            if row[22] == 'nd':
                continue
            key = float(row[14])
            if key not in bleaching_data:
                bleaching_data[key] = [float(row[22])]
            else:
                bleaching_data[key].append(float(row[22]))
    return bleaching_data


def read_csv_data_frequency(filepath: str) -> Dict[int, List[float]]:
    """Return a dictionary mapping each year to a list containing the severities of the
    coral bleaching events that occurred that year.

    Preconditions:
        - filepath refers to a csv file in the format of
          data/coral_bleaching_data.csv
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        bleaching_data = {}

        for row in reader:
            key = int(row[12][:4])
            if key not in bleaching_data:
                bleaching_data[key] = [float(row[14])]
            else:
                bleaching_data[key].append(float(row[14]))
    return bleaching_data


def csv_to_dataframe(filepath: str) -> pd.DataFrame:
    """Return a DataFrame object from the data in the csv file that filepath refers to.

    Preconditions:
        - filepath refers to a csv file in the format of
          data/coral_bleaching_data.csv
    """
    return pd.read_csv(filepath)


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['csv', 'python_ta.contracts', 'pandas'],
        'allowed-io': ['read_csv_data_ssta', 'read_csv_data_frequency'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import doctest
    doctest.testmod(verbose=True)
