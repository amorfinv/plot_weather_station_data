# plot_weather_station_data

Steps to create probability density functions for TU Delft weather stations of wind speed

1. run ```downloader.py``` to download data. Note that you need KNMI API key for 10 minute dara. Place in root directory with file called ```api_key```.
2. Create a folder named ```images```.
3. run ```avspeedplot.py``` to create histograms.
4. run ```avgdirplots.py``` to create windroses.
5. run ```avgvsstdplots.py``` to create a plot of average speed vs standard deviation.


Note: log-normal fitting only makes sense for speed. It does not really fit for the wind directions. Code should be modified for wind direction plots.

## Python requirements
1. pandas
2. scipy
4. numpy
5. matplotlib
