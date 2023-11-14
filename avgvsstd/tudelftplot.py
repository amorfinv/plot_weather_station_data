import utils

def tudelftplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    avgspeedcol = config['avgspeedcol']
    stdspeedcol = config['stdspeedcol']
    data_path = config['path']

    # get header columns
    header_columns = utils.tudelftheaders(data_path)

    # create the filtered dataframe
    df = utils.tudelftdf(data_path, date_range, header_columns, stations)

    # get plot data
    plot_data = tudelftplotdata(df, stations, avgspeedcol, stdspeedcol, plot_data)

    return plot_data

def tudelftplotdata(df, stations, avgspeedcol, stdspeedcol, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
    
        # get station data and the column to plot and remove NaNs 
        station_df = df.loc[df['Name'] == station]
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
