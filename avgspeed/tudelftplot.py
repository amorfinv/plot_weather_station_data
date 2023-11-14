import numpy as np
from scipy import stats
import utils

def tudelftplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    column_to_plot = config['column']
    data_path = config['path']

    # get header columns
    header_columns = utils.tudelftheaders(data_path)

    # create the filtered dataframe
    df = utils.tudelftdf(data_path, date_range, header_columns, stations)

    # get plot data
    plot_data = tudelftplotdata(df, stations, column_to_plot, plot_data)

    return plot_data

def tudelftplotdata(df, stations, column_to_plot, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
    
        # get station data and the column to plot and remove NaNs 
        station_df = df.loc[df['Name'] == station]
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
