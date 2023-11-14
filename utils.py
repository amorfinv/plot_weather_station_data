import os
import pathlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import matplotlib.pyplot as plt
import pandas as pd

def prep_directories(parent_dir, data_sources):

    # STEP 1 create parent directories
    check_directories(parent_dir)

    data_directories = []
    # STEP 2 create child data directories
    for data_source in data_sources:
        # check child directorues
        child_dir = os.path.join(parent_dir, data_source)
        check_directories(child_dir)

        data_directories.append(pathlib.Path(child_dir).resolve())

    return data_directories

def check_directories(directory):
    # Ensure that data directories exist
    if os.path.exists(directory) and os.path.isdir(directory):
        pass
    else:
        print(f"Creating {directory} directory....")
        os.makedirs(directory)


def download_file(url, directory_path):
    '''
        This function downloads files given a url and a director.
    INPUT
        url:            [string] Location of the file
        directory_path: [string] Name of the directory.
    OUTPUT
        N/A
    '''

    local_filename = directory_path / url.rsplit('/', 1)[-1]


    if local_filename.exists():
        print(f'{local_filename} exists. Delete to redownload.')
        return
    
    with requests.get(url, stream=True) as response:
        # Check if the request was successful
        response.raise_for_status()
        
        # Open the local file in binary write mode
        with open(local_filename, 'wb') as file:
            # Iterate over the content of the response in chunks and save it to the local file
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                
    print(f"Downloaded {url} and saved as {local_filename}")


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
    # plt.rcParams['text.usetex'] = texuse
    # Tick size
    plt.rcParams['xtick.major.size'] = tickSize
    plt.rcParams['ytick.major.size'] = tickSize
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'


def tudelftdf(data_path, date_range, header_columns, stations):

    # generic arguments for reading csv data
    csv_args = { 
        'on_bad_lines': 'skip',
        'names': header_columns, 
        'na_values': ['NAN'],
        'dtype': {'Albedo': float},
        'comment': '^'
    }

    # create map that combines all dataframes and combine dataframes
    station_paths = [os.path.join(data_path, weather_station + '.csv') for weather_station in stations]
    csv_map = map(lambda file_path: pd.read_csv(file_path, **csv_args), station_paths)
    wind_df = pd.concat(csv_map)

    # Filter data based on date_range
    # convert datetime to datetime object
    wind_df['DateTime'] = pd.to_datetime(wind_df['DateTime'], errors='coerce')

    # Define the desired time range for the year 2022
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the wind_data DataFrame to include only dates within the year 2022
    #filtered_wind_df = wind_df.loc['DateTime', start_date:end_date]
    filtered_wind_df = wind_df[(wind_df['DateTime'] >= start_date) & (wind_df['DateTime'] <= end_date)]

    return filtered_wind_df


def tudelftheaders(data_path):

    header_path = os.path.join(data_path, 'fields.txt')
    # read in the column names,  remove new line characters, and empty spaces
    with open(header_path, 'r') as file:
        columns = file.readlines()
    columns = [column.rstrip('\n') for column in columns]
    columns = [column.split(" ")[-1] for column in columns]

    return columns


def knmi1hrheaders(data_path):

    column_string = 'STN,YYYYMMDD,   HH,   DD,   FH,   FF,   FX,    T, T10N,   TD,   SQ,    Q,   DR,   RH,    P,   VV,    N,    U,   WW,   IX,    M,    R,    S,    O,    Y'
    columns = column_string.replace(" ", "")
    columns = columns.split(',')

    return columns

def knmi1hrdf(data_path, date_range, header_columns, stations):

    # generic arguments for reading csv data
    csv_args = { 
        'on_bad_lines': 'skip',
        'na_values': ['NaN'],
        'skiprows': 32,
        'names': header_columns
    }

    # create map that combines all dataframes and combine dataframes
    list_files = os.listdir(data_path)    
    station_paths = [os.path.join(data_path, file) for file in list_files if '.zip' in file]
    csv_map = map(lambda file_path: pd.read_csv(file_path, **csv_args), station_paths)
    wind_df = pd.concat(csv_map)

    # STEP 3: Filter data based on date_range
    # convert datetime to datetime object
    wind_df['HH'] = wind_df['HH'].astype(str)
    wind_df['YYYYMMDD'] = wind_df['YYYYMMDD'].astype(str)
    wind_df['DateTime'] = pd.to_datetime(wind_df['YYYYMMDD'] + wind_df['HH'], format='%Y%m%d%H', errors='coerce')

    # Define the desired time range for the year 2022
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the wind_data DataFrame to include only dates within the year 2022
    #filtered_wind_df = wind_df.loc['DateTime', start_date:end_date]
    filtered_wind_df = wind_df[(wind_df['DateTime'] >= start_date) & (wind_df['DateTime'] <= end_date)]

    return filtered_wind_df

def knmi10mindf(data_path, date_range, stations):

    # read parquet
    dataframe_path = os.path.join(data_path, 'knmi10min.parquet')
    wind_df = pd.read_parquet(dataframe_path)

    # STEP 2: Only select the columns with relevant weather stations
    station_wind_df = wind_df[wind_df['NAME'].isin(stations)]


    # Define the desired time range for the year 2022
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the wind_data DataFrame to include only dates within the year 2022
    filtered_wind_df = station_wind_df[(station_wind_df['DTG'] >= start_date) & (station_wind_df['DTG'] <= end_date)]

    return filtered_wind_df