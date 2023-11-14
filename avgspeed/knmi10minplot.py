import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def knmi10minplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    column_to_plot = config['column']
    data_path = config['path']

    # create the filtered dataframe
    df = knmi10mindf(data_path, column_to_plot, date_range, stations)

    # get plot data
    plot_data = knmi10minplotdata(df, stations, column_to_plot, plot_data)

    return plot_data

def knmi10mindf(data_path, column_to_plot, date_range, stations):

    # read parquet
    dataframe_path = os.path.join(data_path, 'knmi10min.parquet')
    wind_df = pd.read_parquet(dataframe_path)

    # STEP 2: Only select the columns with relevant weather stations
    station_wind_df = wind_df[wind_df['NAME'].isin(stations)]


    # Define the desired time range for the year 2022
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the wind_data DataFrame to include only dates within the year 2022
    filtered_wind_df = station_wind_df[(station_wind_df['DTG'] >= start_date) & (station_wind_df['DTG'] <= end_date)]


    return filtered_wind_df

def knmi10minplotdata(df, stations, column_to_plot, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
        
        # get station data and the column to plot and remove NaNs 
        station_df = df.loc[df['NAME'] == station]
        data_to_fit = station_df[column_to_plot]
        data_to_fit = data_to_fit.dropna()
        data_to_fit = data_to_fit.to_numpy()

        # fit to log normal plot
        shape, loc, scale = stats.lognorm.fit(data_to_fit)
        
        # perform statistical test
        res = stats.kstest(data_to_fit, 'lognorm', args=(shape, loc, scale))

        # create arrays with fit to plot later
        x = np.linspace(data_to_fit.min(), data_to_fit.max(), 100)
        fitted_lognormal = stats.lognorm.pdf(x, shape, loc, scale)

        # save fit parameters
        plot_data[station] = {
                'shape': shape, 
                'loc': loc, 
                'scale': scale, 
                'p': res.pvalue,
                'stat': res.statistic,
                'data': data_to_fit,
                'x_plot': x,
                'y_plot': fitted_lognormal
                }

    return plot_data
