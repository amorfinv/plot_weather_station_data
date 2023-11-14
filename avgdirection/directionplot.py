import os
import matplotlib.pyplot as plt

from avgdirection.tudelftplot import tudelftplot
from avgdirection.knmi1hrplot import knmi1hrplot
from avgdirection.knmi10minplot import knmi10minplot
import utils

def make_direction_plots(source_config_dict, plot_config):

    plot_title = plot_config['plot_title']
    date_range = plot_config['date_range']

    # gather plotting data here
    plot_data = {}
    
    if 'tudelft' in source_config_dict:
        plot_data = tudelftplot(source_config_dict['tudelft'], date_range, plot_data)

    if 'knmi1hr' in source_config_dict:
        plot_data = knmi1hrplot(source_config_dict['knmi1hr'], date_range, plot_data)

    if 'knmi10min' in source_config_dict:
        plot_data = knmi10minplot(source_config_dict['knmi10min'], date_range, plot_data)

    make_images(plot_data, date_range, plot_title)


def make_images(plot_data, date_range, plot_title):

    utils.fixPlot(thickness=1.5, fontsize=25, markersize=8, labelsize=20, texuse=True, tickSize = 15)

    # create individual plots for each weather_station comparing it to
    for weather_station, fit_dict in plot_data.items():
        
        # get the plot title from configuration
        plot_title = plot_title

        # get filename
        filename = '_'.join([weather_station, plot_title, *date_range]) + '.png'
        filename = filename.replace(" ", "").lower()
        
        # get the x axis name depending on what is being plotted    
        x_axis_label = 'Wind Speed (m/s)' if 'speed' in filename else 'Wind Direction (degrees)'

        # start plot
        plt.figure()
        plt.hist(fit_dict['data'], bins='auto', density=True, label='Weather station data')


        plt.xlabel(x_axis_label)
        plt.ylabel('Probability density function')
        plt.legend()    
        plt.title(f'PDF of {plot_title} for {weather_station} weather station \n from {date_range[0]} to {date_range[1]}')
        plt.savefig(os.path.join('images', filename))
        plt.close()

    # crete combined plots

    plt.figure()

    # get the plot title from configuration and xlabel
    plot_title = plot_title
    x_axis_label = 'Wind Speed (m/s)' if 'speed' in plot_title else 'Wind Direction (degrees)'

    filename = '_'.join(['stationcomparison', plot_title, *date_range]) + '.png'
    filename = filename.replace(" ", "").lower()

    for weather_station, fit_dict in plot_data.items():

        if weather_station == 'Rotterdam locatie 24t':
            continue
        plt.plot(fit_dict['x_plot'], fit_dict['y_plot'], label=weather_station)

    plt.xlabel(x_axis_label)
    plt.ylabel('Probability density function')
    plt.legend()    
    plt.title(f'Log-normal comparisions of {plot_title} \n from {date_range[0]} to {date_range[1]}')
    plt.savefig(os.path.join('images', filename))
    plt.close()
