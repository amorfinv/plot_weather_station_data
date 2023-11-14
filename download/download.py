
import utils
from urllib.parse import urljoin
import sys
import os
from subprocess import Popen
from download.createparquet import create_parquet

def download_data(source_config_dict):
    
    if 'tudelft' in source_config_dict:
        tudelftdownload(source_config_dict['tudelft'])

    if 'knmi1hr' in source_config_dict:
        knmi1hrdownload(source_config_dict['knmi1hr'])

    if 'knmi10min' in source_config_dict:
        # call file separately
        knmi10mindownload(source_config_dict['knmi10min'])


def tudelftdownload(tudelftconfig):
    
    url = tudelftconfig['url']
    directory_path = tudelftconfig['path']
    file2down = utils.list_csv_files_at_url(url)

    # Index and download the files
    for myFile in file2down:
        utils.download_file(myFile, directory_path)

    # Download header
    myFile = url + '/fields.txt'
    utils.download_file(myFile, directory_path)


def knmi1hrdownload(knmi1hrconfig):
    
    url = knmi1hrconfig['url']
    directory_path = knmi1hrconfig['path']
    file2down = [urljoin(url,file) for file in knmi1hrconfig['files_to_download']]

    # Index and download the files
    for myFile in file2down:
        utils.download_file(myFile, directory_path)


def knmi10mindownload(knmi10minconfig):

    url = knmi10minconfig['url']
    directory_path = knmi10minconfig['path']
    api_key = knmi10minconfig['api_key']
    cut_off_year = knmi10minconfig['cut_off_year']

    # call file separately and wait
    args = [sys.executable, os.path.join(
        'download','knmi10minasyncdownload.py'),
        url,
        directory_path, 
        api_key,
        cut_off_year
    ]
    process = Popen(args)
    process.wait()

    # create parquet file for easier loading
    create_parquet(directory_path, 'knmi10min')

    
