import os
import matplotlib.pyplot as plt

from avgvsstd.tudelftplot import tudelftplot
from avgvsstd.knmi1hrplot import knmi1hrplot
from avgvsstd.knmi10minplot import knmi10minplot


def make_avgvsstd_plots(source_config_dict, plot_config):

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

    # create individual plots for each weather_station comparing it to
    for weather_station, fit_dict in plot_data.items():

        # get filename
        filename = '_'.join([weather_station, plot_title, *date_range]) + '.png'
        filename = filename.replace(" ", "").lower()
        # start plot
        plt.figure()
        plt.scatter(fit_dict['stdspeed'], fit_dict['avgspeed'], label='Weather station data')
        plt.xlabel('Standard deviation (m/s)')
        plt.ylabel('Average speed (m/s)')

        #plt.legend()    
        plt.title(f'{weather_station} weather station \n from {date_range[0]} to {date_range[1]}')
        plt.savefig(os.path.join('images', filename))
        plt.close()

 