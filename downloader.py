
import utils
from download import download

def main():

    parent_dir = 'data'

    source_config_dict = {
        'tudelft': {
            'url': 'https://weather.tudelft.nl/csv/'
        },
        'knmi1hr': {
            'url': 'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/uurgegevens/',
            'files_to_download': [
                'uurgeg_344_2011-2020.zip',
                'uurgeg_344_2021-2030.zip',
                ]
        },
        'knmi10min': {
            'url': 'https://api.dataplatform.knmi.nl/open-data/v1',
            'api_key': open('api_key', 'r').read().strip(),
            'cut_off_year': '2020'
        }
    }

    # STEP 1 prep data directories
    data_directories = utils.prep_directories(
        parent_dir=parent_dir, 
        data_sources=source_config_dict.keys()
        )
    
    # add the full directories to config
    for idx, source_config in enumerate(source_config_dict):        
        source_config_dict[source_config]['path'] = data_directories[idx]

    # STEP 2 download data
    download.download_data(source_config_dict)


if __name__ == '__main__':
    main()