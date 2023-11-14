import utils

def knmi1hrplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    avgspeedcol = config['avgspeedcol']
    stdspeedcol = config['stdspeedcol']
    data_path = config['path']

    # get header columns
    header_columns = utils.knmi1hrheaders(data_path)

    # create the filtered dataframe
    df = utils.knmi1hrdf(data_path, date_range, header_columns, stations)

    # get plot data
    plot_data = knmi1hrplotdata(df, stations, avgspeedcol, stdspeedcol, plot_data)

    return plot_data


def knmi1hrplotdata(df, stations, avgspeedcol, stdspeedcol, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
        
        avgspeed = df[avgspeedcol]
        avgspeed = avgspeed.dropna()
        avgspeed = avgspeed.to_numpy()* 0.1

        stdspeed = df[stdspeedcol]
        stdspeed = stdspeed.dropna()
        stdspeed = stdspeed.to_numpy()* 0.1

        # save fit parameters
        plot_data[station] = {
                'avgspeed': avgspeed,
                'stdspeed': stdspeed
                }
    return plot_data
