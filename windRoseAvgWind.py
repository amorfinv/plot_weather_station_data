# Mostly copied from Andres' script #
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from functions import fixPlot

num_bins = int(360/5)
figx, figy = 10,10
range_to_plot = ['2022-01-01','2022-12-31']

# read in the column names,  remove new line characters, and empty spaces
with open('data/fields.txt', 'r') as file:
   columns = file.readlines()
columns = [column.rstrip('\n') for column in columns]
columns = [column.split(" ")[-1] for column in columns]

# csv read configurations
csv_args = { 
    'on_bad_lines': 'skip',
    'names': columns, 
    'na_values': ['NAN'],
    'dtype': {'Albedo': float},
    'comment': '^'
}
# Read the database
#stations = ['Oost', 'Ommoord', 'Bolnes', 'SpaansePolder', 'Ridderkerk', 'Heijplaat', 'Delfshaven']
stations = ['Delfshaven']  # Uncomment to debug
fixPlot(thickness=1.5, fontsize=25, markersize=8, labelsize=20, texuse=True, tickSize = 15)
for iternum in range(len(stations)):
    filein='data/'+stations[iternum]+'.csv'
    df = pd.read_csv(filein,**csv_args)
    # convert datetime to datetime object
    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
    # Define the desired time range
    start_date = pd.to_datetime(range_to_plot[0])
    end_date = pd.to_datetime(range_to_plot[1])
    # Filter the data
    df_filtered = df[(df['DateTime'] >= start_date) & (df['DateTime'] <= end_date)]

    # PLOTTING

    # Calculate bin edges and centers for wind directions
    bin_edges = np.linspace(0, 360, num_bins + 1, endpoint=True)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    print(bin_edges)
    # Compute the histogram
    windHist, _ = np.histogram(df_filtered['WindDir_{Avg}'],bins=bin_edges)
    fig = plt.figure(iternum+1,figsize=(figx,figy))
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
    
    ax.set_title(stations[iternum], va='bottom')
plt.show()

