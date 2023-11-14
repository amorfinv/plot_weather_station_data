import os
import pathlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
