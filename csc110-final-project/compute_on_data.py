"""CSC110 Fall 2020 Final Project: Computing on Data

Information
===============================
This Python module contains the functions that will be used to compute on the
data that was extracted from the dataset. Some of the purposes of this
module include, but are not limited to: transforming the data about the
severity of a coral bleaching event and the SSTAs that were present at the
times of such severe bleaching events into a bunch of points so that a correlation
can be established; determining the frequency and average severity of the
coral bleaching events per year; and changing the dates in a dataframe
to a more favourable format.

Copyright Information
===============================
This file is Copyright (c) 2020 Anis Singh.
"""

from typing import List, Dict, Tuple
import pandas as pd


# Functions to process the data about the severity of a coral bleaching event and the SSTAs
# that were present at the times of those bleaching events.

def determine_average_sstas(data: Dict[float, List[float]]) -> Dict[float, float]:
    """Return a dictionary mapping the severity of the coral bleaching events (each key
    in data) to the average of all the SSTAs that were present when such an event occurred (the
    average of each value in data), rounded to 3 decimal places.

    Preconditions:
        - data is the return value of the function read_csv_data_ssta from the read_data
          module
    """
    data_containing_averages = {}
    for key in data:
        assert key not in data_containing_averages

        avg = round(calculate_average(data[key]), 3)
        data_containing_averages[key] = avg
    return data_containing_averages


def convert_to_points(data: Dict[float, float]) -> Tuple[List[float], List[float]]:
    """Convert the values and the keys in data into x and y coordinates
    respectively. Return a tuple of two lists, where the first list contains the x
    coordinates, and the second list contains the y coordinates.

    Preconditions:
        - the keys of data are the dependent variables, and the values of data
          are the independent variables

    >>> convert_to_points({1.0: 12.0, 2.0: 15.0, 3.0: 18.0})
    ([12.0, 15.0, 18.0], [1.0, 2.0, 3.0])
    >>> convert_to_points({100.4: 52.4, 23.0: 11.0})
    ([52.4, 11.0], [100.4, 23.0])
    """
    return (list(data.values()), list(data.keys()))


def calculate_average(collection: list) -> float:
    """Return the mean value of the collection of numbers stored in collection.

    Preconditions:
        - all(isinstance(x, int) or isinstance(x, float) for x in collection)

    >>> calculate_average([2.0, 4.0, 6.0, 8.0])
    5.0
    >>> calculate_average([105.0, 55.0, 17.0])
    59.0
    """
    return sum(collection) / len(collection)


# Functions to determine the frequency and average severity of all the coral bleaching events
# per year.

def get_freq_and_severity(data: Dict[int, List[float]]) -> Dict[int, Tuple[int, float]]:
    """Return a dictionary mapping each year (each key in data) to a Tuple containing the frequency
    of coral bleaching events that year at index 0, and the average severity of all the bleaching
    events that happened that year at index 1. The values for the frequency and average severity
    are obtained by performing operations on the values of data.

    Implementation Notes:
        - This function filters out any years where little data (<= 70 data entries) was recorded to
          reduce outliers.
        - A coral bleaching event is said to have occurred if the bleaching severity rating is
          strictly greater than 0.

    Preconditions:
        - data is the return value of the function read_csv_data_frequency from the
          read_data module
    """
    filtered_data = {key: data[key] for key in data if len(data[key]) > 70}
    return {year: (_count_occurrences(filtered_data[year], 0),
                   _get_average_severity(filtered_data[year], 0.0)) for year in filtered_data}


def _count_occurrences(collection: List[float], n: int) -> int:
    """Return the number of items in collection that are strictly greater than n.

    Preconditions:
        - This function is only meant to be called by get_freq_and_severity as a helper
          function. It is not intended to be used in other situations, even though it may work.

    >>> _count_occurrences([1.0, 2.5, 3.7, 4.1], 4)
    1
    >>> _count_occurrences([12.0, 25.0, 89.4], 12)
    2
    """
    return len([item for item in collection if item > n])


def _get_average_severity(collection: List[float], n: float) -> float:
    """Return the average severity of all the items in collection that are greater than n.

    Preconditions:
        - This function is only meant to be called by get_freq_and_severity as a helper
          function. It is not intended to be used in other situations, even though it
          may work.

    >>> _get_average_severity([1.0, 0.0, 0.0, 12.0, 11.0], 0.0)
    8.0
    >>> _get_average_severity([6.0, 7.2, 4.8, 3.8], 4.3)
    6.0
    """
    severities = [num for num in collection if num > n]
    return sum(severities) / len(severities)


# Function to convert the date of a bleaching event that is in the form of yyyymmdd
# into a date that is in the form of yyyy in a DataFrame.

def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame that contains dates in the form of yyyy instead of
    in the form of yyyymmdd.

    Preconditions:
        - df is a DataFrame returned by the function csv_to_dataframe from
          the read_data module
    """
    # Note: The Date2 column has dates in the form of yyyymmdd. Thus, by dividing each
    # integer by 10000 and flooring the result, only the year remains.
    df['Date2'] = df['Date2'].floordiv(10000).astype(int)
    return df


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'pandas'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import doctest
    doctest.testmod(verbose=True)
