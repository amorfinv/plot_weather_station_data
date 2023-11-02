import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import matplotlib.pyplot as plt
#
# Function to download files from the weather repository
#
def download_file(url, local_filename):
    '''
        This function downloads all the files from the weather.tudelft.nl location
    INPUT
        url:            [string] Location of the file
        local_filename: [string] Name of the file where data is downloaded
    OUTPUT
        N/A
    '''
    with requests.get(url, stream=True) as response:
        # Check if the request was successful
        response.raise_for_status()
        
        # Open the local file in binary write mode
        with open(local_filename, 'wb') as file:
            # Iterate over the content of the response in chunks and save it to the local file
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                
    print(f"Downloaded {url} and saved as {local_filename}")
#
#   Lists all the available files/content at the given location
#
def list_csv_files_at_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all anchor tags (links) in the HTML content
    anchor_tags = soup.find_all('a')
    
    # Extract href attribute from anchor tags and join them with the base URL
    file_urls = [urljoin(url, anchor['href']) for anchor in anchor_tags if anchor.has_attr('href')]
    
    # Filter URLs that end with ".csv"
    csv_files = [file_url for file_url in file_urls if file_url.lower().endswith('.csv')]
    
    return csv_files
#
# Set default plotting size
#
def fixPlot(thickness=1.5, fontsize=20, markersize=8, labelsize=15, texuse=False, tickSize = 15):
    '''
        This plot sets the default plot parameters
    INPUT
        thickness:      [float] Default thickness of the axes lines
        fontsize:       [integer] Default fontsize of the axes labels
        markersize:     [integer] Default markersize
        labelsize:      [integer] Default label size
    OUTPUT
        None
    '''
    # Set the thickness of plot axes
    plt.rcParams['axes.linewidth'] = thickness    
    # Set the default fontsize
    plt.rcParams['font.size'] = fontsize    
    # Set the default markersize
    plt.rcParams['lines.markersize'] = markersize    
    # Set the axes label size
    plt.rcParams['axes.labelsize'] = labelsize
    # Enable LaTeX rendering
    plt.rcParams['text.usetex'] = texuse
    # Tick size
    plt.rcParams['xtick.major.size'] = tickSize
    plt.rcParams['ytick.major.size'] = tickSize
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'