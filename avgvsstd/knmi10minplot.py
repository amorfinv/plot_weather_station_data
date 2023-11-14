import utils

def knmi10minplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    avgspeedcol = config['avgspeedcol']
    stdspeedcol = config['stdspeedcol']
    data_path = config['path']

    # create the filtered dataframe
    df = utils.knmi10mindf(data_path, date_range, stations)

    # get plot data
    plot_data = knmi10minplotdata(df, stations, avgspeedcol, stdspeedcol, plot_data)

    return plot_data


def knmi10minplotdata(df, stations, avgspeedcol, stdspeedcol, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
        
        # get station data and the column to plot and remove NaNs 
        station_df = df.loc[df['NAME'] == station]
        
        avgspeed = station_df[avgspeedcol]
        avgspeed = avgspeed.dropna()
        avgspeed = avgspeed.to_numpy()

        stdspeed = station_df[stdspeedcol]
        stdspeed = stdspeed.dropna()
        stdspeed = stdspeed.to_numpy()

        # save fit parameters
        plot_data[station] = {
                'avgspeed': avgspeed,
                'stdspeed': stdspeed
                }

    return plot_data
