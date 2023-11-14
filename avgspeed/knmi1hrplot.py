import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def knmi1hrplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    column_to_plot = config['column']
    data_path = config['path']

    # get header columns
    header_columns = knmi1hrheaders(data_path)

    # create the filtered dataframe
    df = knmi1hrdf(data_path, column_to_plot, date_range, header_columns, stations)

    # get plot data
    plot_data = knmi1hrplotdata(df, stations, column_to_plot, plot_data)

    return plot_data


def knmi1hrheaders(data_path):

    column_string = 'STN,YYYYMMDD,   HH,   DD,   FH,   FF,   FX,    T, T10N,   TD,   SQ,    Q,   DR,   RH,    P,   VV,    N,    U,   WW,   IX,    M,    R,    S,    O,    Y'
    columns = column_string.replace(" ", "")
    columns = columns.split(',')

    return columns

def knmi1hrdf(data_path, column_to_plot, date_range, header_columns, stations):

    # generic arguments for reading csv data
    csv_args = { 
        'on_bad_lines': 'skip',
        'na_values': ['NaN'],
        'skiprows': 32,
        'names': header_columns
    }

    # create map that combines all dataframes and combine dataframes
    list_files = os.listdir(data_path)    
    station_paths = [os.path.join(data_path, file) for file in list_files if '.zip' in file]
    csv_map = map(lambda file_path: pd.read_csv(file_path, **csv_args), station_paths)
    wind_df = pd.concat(csv_map)

    # STEP 3: Filter data based on date_range
    # convert datetime to datetime object
    wind_df['HH'] = wind_df['HH'].astype(str)
    wind_df['YYYYMMDD'] = wind_df['YYYYMMDD'].astype(str)
    wind_df['DateTime'] = pd.to_datetime(wind_df['YYYYMMDD'] + wind_df['HH'], format='%Y%m%d%H', errors='coerce')

    # Define the desired time range for the year 2022
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the wind_data DataFrame to include only dates within the year 2022
    #filtered_wind_df = wind_df.loc['DateTime', start_date:end_date]
    filtered_wind_df = wind_df[(wind_df['DateTime'] >= start_date) & (wind_df['DateTime'] <= end_date)]

    return filtered_wind_df

def knmi1hrplotdata(df, stations, column_to_plot, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
        
        # get station data and the column to plot and remove NaNs 
        data_to_fit = df[column_to_plot]
        data_to_fit = data_to_fit.dropna()
        data_to_fit = data_to_fit.to_numpy() * 0.1

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
