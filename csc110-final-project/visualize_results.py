"""CSC110 Fall 2020 Final Project: Visualizing the Results of the Computations

Information
===============================
This Python module contains the functions that will be used to visually display the results
of the computations that have been performed on the data.

Copyright Information
===============================
This file is Copyright (c) 2020 Anis Singh.
"""
from typing import List, Dict, Tuple
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Function to visualize the correlation between the severity of a coral bleaching event
# and the average sea surface temperature anomaly at that time.

def show_correlation(x_coords: List[float], y_coords: List[float]) -> None:
    """Plot the given x and y coordinates and plot a line of best fit for the points.

    Preconditions:
        - x_coords and y_coords are the return values of convert_to_points from the
          compute_on_data module
    """
    fig = px.scatter(x=x_coords,
                     y=y_coords,
                     trendline='ols',
                     trendline_color_override='darkblue')
    fig.update_layout(
        title=dict(
            text='Relationship Between Change in Sea Surface Temperature and Coral Bleaching',
            x=0.5,
            font=dict(
                family='Gravitas One',
                size=28,
                color='black'
            )
        ),
        xaxis_title='Average Sea Surface Temperature Anomalies (' + u'\N{DEGREE SIGN}' + 'C)',
        yaxis_title='Severity of Coral Bleaching (%)',
        font_size=14
    )
    fig.show()


# Function to visualize the frequency and average severity of the coral bleaching events
# per year.

def show_freq_and_severity(data: Dict[int, Tuple[int, float]]) -> None:
    """Plot the values that correspond to each key in data as two bar charts.

    Preconditions:
        - data is the return value of get_freq_and_severity from the compute_on_data
          module
    """
    x_values = [str(key) for key in data]
    y1_values = [data[key][0] for key in data]
    y2_values = [data[key][1] for key in data]

    assert len(x_values) == len(y1_values) == len(y2_values)

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'bar'}]],
                        subplot_titles=('Frequency', 'Average Severity'))

    fig.add_trace(go.Bar(name='Frequency', x=x_values, y=y1_values), row=1, col=1)
    fig.add_trace(go.Bar(name='Average Severity', x=x_values, y=y2_values), row=1, col=2)

    fig.update_layout(title=dict(
        text='Frequency and Average Severity of Coral Bleaching Per Year',
        x=0.5,
        font=dict(
            family='Gravitas One',
            size=28,
            color='black'
        )
    ))
    fig.show()


# Function to generate an interactive map of the world that plots coral bleaching
# events for every year and allows the user to choose which year they wish to view.

def generate_map(df: pd.DataFrame) -> None:
    """Generate an interactive map based on the data contained in the DataFrame
    object df.

    Preconditions:
        - df is the DataFrame returned by the function convert_dates in the
          compute_on_data module
    """
    pd.set_option('mode.chained_assignment', None)

    data_slider = []
    years = sorted(df.Date2.unique())

    # Remove the years with insufficient data
    for i in range(1998, 2003):
        # There was no data recorded in 1999, and so attempting to remove 1999 from years would
        # throw an error because 1999 would not be in the list
        if i == 1999:
            continue
        years.remove(i)

    start_year = min(years)

    # Iterate through each year in years to get the necessary data
    for year in years:
        # Select the year
        # Uses '&' and not 'and' because bitwise operator is required
        df_specific_year = df[(df['Date2'] == year) & (df['Average_Bleaching'] > 0.0)]

        # Convert every column object type to a string
        for col in df_specific_year.columns:
            df_specific_year[col] = df_specific_year[col].astype('string')

        # Note: This line of code is very subtle but powerful and necessary. If you read
        # a little further down this file, you will notice that the opacity of a specific
        # marker is determined by its average bleaching percentage. However, this presents
        # a small bug if left unhandled, because multiple bleaching events can be recorded
        # in the same year with the exact same longitude and latitude, and so the point
        # that is added LAST will be the only point that shows up in that location on the
        # map for that year. This will cause some points to appear much darker than they
        # should be, because there is a point behind it that is more opaque, but it
        # isn't showing up because it is in the exact same latitude and longitude position
        # as the point with a lower opacity. This line of code ensures that the darkest
        # opacity point is the one that will show up on the map by sorting df_specific_year in
        # ascending order based on its Average_Bleaching column. As a side comment, points
        # that are stacked on top of each other will always appear darker (since there are
        # more of them), but you will only be able to see one point on the map. This WILL
        # make some points appear darker than others that have the same (or slightly higher)
        # bleaching values when a user hovers over the point, but this is fair because that
        # area did experience more bleaching.
        df_specific_year = df_specific_year.sort_values(['Average_Bleaching'])

        # Create a new column for mouse-hovering text
        df_specific_year['text'] = 'Bleaching %: ' + df_specific_year['Average_Bleaching']

        # Create a new column for the opacity of the markers
        # Note: 10 is an arbitrary choice that was made to ensure the visibility of each
        # marker, while still accurately reflecting the severity of each bleaching
        # event
        df_specific_year['opac'] = df_specific_year['Average_Bleaching'].astype(float) / 10

        # Ensure the maximum value for each opacity is less than or equal to 1.0
        df_specific_year['opac'] = df_specific_year['opac'].where(
            df_specific_year['opac'] <= 1.0, 1.0)

        # Ensure every point is somewhat visible. It should be noted that 0.3 is an arbitrary
        # choice.
        df_specific_year['opac'] = df_specific_year['opac'].where(
            df_specific_year['opac'] > 0.3, 0.3)

        # Create the data for this year
        data_this_year = go.Scattergeo(
            lon=df_specific_year['Longitude_Degrees'],
            lat=df_specific_year['Latitude_Degrees'],
            mode='markers',
            marker=dict(
                size=7.5,
                opacity=df_specific_year['opac'],
                line=dict(
                    color='red',
                    width=2
                )
            ),
            text=df_specific_year['text'],
            hoverinfo='text'
        )

        # Add this data to data slider
        data_slider.append(data_this_year)

    # Make only the 2003 data visible when the map is first displayed
    data_slider[0].visible = True
    for i in range(1, len(data_slider)):
        data_slider[i].visible = False

    # Create the steps for the slider
    steps = []
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label='Year ' + str(i + start_year))

        # For a certain year, make only the data from that year visible
        step['args'][1][i] = True

        steps.append(step)

    # Create the sliders from the steps
    # Note: The active slider is set to 0 (Year 2003) because only the data from 2003 is
    # visible when the map is first displayed
    sliders = [dict(active=0, pad={'t': 1}, steps=steps)]

    # Create the layout of the figure object that will be created
    layout = dict(geo=dict(scope='world', showcoastlines=True, coastlinecolor='black',
                           showland=True, landcolor='LightGreen',
                           showocean=True, oceancolor='LightBlue',
                           showlakes=True, lakecolor='Blue',
                           showrivers=True, rivercolor='Blue',
                           projection=dict(
                               type='orthographic'
                           )),
                  sliders=sliders)

    # Create the figure object
    fig = go.Figure(data=data_slider, layout=layout)

    # Add a title
    fig.update_layout(title=dict(
        text='Map of Coral Bleaching Events and their Severity',
        x=0.5,
        font=dict(
            size=28,
            color='black',
            family='Gravitas One'
        )
    ))

    # Show the figure object
    fig.show()


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'plotly.express', 'pandas',
                          'plotly.graph_objects', 'plotly.subplots'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import doctest
    doctest.testmod(verbose=True)
