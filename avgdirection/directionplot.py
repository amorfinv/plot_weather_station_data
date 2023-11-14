import os
import matplotlib.pyplot as plt
import numpy as np

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
    num_bins = 64
    figx, figy = 10,10

    for weather_station, fit_dict in plot_data.items():

        data_to_plot = fit_dict['data']
        
        # get the plot title from configuratio
        # get filename
        filename = '_'.join([weather_station, plot_title, *date_range]) + '.png'
        filename = filename.replace(" ", "").lower()
        
        # Calculate bin edges and centers for wind directions
        bin_edges = np.linspace(0, 360, num_bins + 1, endpoint=True)
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        # Compute the histogram
        windHist, _ = np.histogram(data_to_plot,bins=bin_edges)
        
        plt.figure(figsize=(figx,figy))
        
        ax = plt.subplot(1,1,1,polar=True)
        # Plot windrose histogram
        ax.bar(np.radians(bin_centers), windHist, width=np.radians(360 / num_bins),  
            align="center", color="red", edgecolor="black")
        
        # Customize the windrose plot
        ax.tick_params(axis='both', pad=20)
        ax.set_theta_offset(np.radians(90))  
        ax.set_theta_direction(-1)  
        ax.set_rlabel_position(0)  
        ax.set_rticks([])  
        
        ax.set_title(weather_station, va='bottom')


        plt.savefig(os.path.join('images', filename))
        plt.close()

