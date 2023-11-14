import utils

def knmi1hrplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    column_to_plot = config['column']
    data_path = config['path']

    # get header columns
    header_columns = utils.knmi1hrheaders(data_path)

    # create the filtered dataframe
    df = utils.knmi1hrdf(data_path, column_to_plot, date_range, header_columns, stations)

    # get plot data
    plot_data = knmi1hrplotdata(df, stations, column_to_plot, plot_data)

    return plot_data


def knmi1hrplotdata(df, stations, column_to_plot, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
        
        # get station data and the column to plot and remove NaNs 
        data_to_fit = df[column_to_plot]
        data_to_fit = data_to_fit.dropna()
        data_to_fit = data_to_fit.to_numpy()

        # save fit parameters
        plot_data[station] = {
                'data': data_to_fit,
                }

    return plot_data
