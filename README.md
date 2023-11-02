# plot_weather_station_data

Steps to create probability density functions for TU Delft weather stations of wind speed

1. Download data from TU Delft [weather stations](https://weather.tudelft.nl/csv/) and place in a folder named ```data```.
2. Create a folder named ```images```.
3. Set desired stations in line 8, for example: ```weather_stations = ['Oost', 'Delfshaven']```
4. Set field to plot in line 9, for example: ```column_to_plot = 'WindSpd_{Avg}'```. See ```fields.txt``` for list of wind speed fields.
5. Set the desired range to plot in line 10, for example: ```range_to_plot = ['2022-01-01','2022-12-31']```
6. Add the desired plot title to the ```plot_titles``` dictionary if it is not already there.
7. Run ```python create_plots.py```

Note: log-normal fitting only makes sense for speed. It does not really fir for the wind directions. Code should be modified for wind direction plots.

## Python requirements
1. pandas
2. scipy
4. numpy
5. matplotlib
