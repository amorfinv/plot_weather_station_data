import pandas as pd
import utils

def knmi10minplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    column_to_plot = config['column']
    data_path = config['path']

    # create the filtered dataframe
    df = utils.knmi10mindf(data_path, column_to_plot, date_range, stations)

    # get plot data
    plot_data = knmi10minplotdata(df, stations, column_to_plot, plot_data)

    return plot_data


def knmi10minplotdata(df, stations, column_to_plot, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
        
        # get station data and the column to plot and remove NaNs 
        station_df = df.loc[df['NAME'] == station]
        data_to_fit = station_df[column_to_plot]
        data_to_fit = data_to_fit.dropna()
        data_to_fit = data_to_fit.to_numpy()

        # save fit parameters
        plot_data[station] = {
                'data': data_to_fit,
                }

    return plot_data
