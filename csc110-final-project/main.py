"""CSC110 Fall 2020 Final Project: The Main Module

Information
===============================
This Python module is the main module. It contains a function that can be called to produce
the results of my project in a visual way.

Copyright Information
===============================
This file is Copyright (c) 2020 Anis Singh.
"""
import read_data
import compute_on_data
import visualize_results


def display_results(result: str) -> None:
    """Display the results of this project. Which results are displayed
    depends on result.

    Preconditions:
        - result == 'c' or result == 'fs' or result == 'm'
    """
    if result == 'c':
        raw_data = read_data.read_csv_data_ssta('data/coral_bleaching_data.csv')
        refined_data = compute_on_data.determine_average_sstas(raw_data)
        points = compute_on_data.convert_to_points(refined_data)

        visualize_results.show_correlation(points[0], points[1])

    elif result == 'fs':
        raw_data = read_data.read_csv_data_frequency('data/coral_bleaching_data.csv')
        refined_data = compute_on_data.get_freq_and_severity(raw_data)

        visualize_results.show_freq_and_severity(refined_data)

    else:
        raw_dataframe = read_data.csv_to_dataframe('data/coral_bleaching_data.csv')
        refined_dataframe = compute_on_data.convert_dates(raw_dataframe)

        visualize_results.generate_map(refined_dataframe)


if __name__ == '__main__':
    # Visualize the correlation between the severity of a coral bleaching event
    # and the average of the sea surface temperature anomalies of the ocean at that
    # time.
    display_results('c')

    # Visualize the frequency and average severity of coral bleaching events
    # per year.
    display_results('fs')

    # Display an interactive map of the world that demonstrates the coral bleaching
    # at specific locations for each year between 2003-2017 inclusive.
    display_results('m')
