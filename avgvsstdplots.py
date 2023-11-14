
import utils
from avgvsstd import avgvsstd

def main():

    plot_config = {
        'parent_dir': 'data',
        'plot_title': 'Average speed vs standard deviation',
        'date_range': ['2022-01-01','2022-12-31']
    }
    

    source_config_dict = {
        'tudelft': {
            'stations': ['SpaansePolder', 'Delfshaven'],
            'avgspeedcol': 'WindSpd_{Avg}',
            'stdspeedcol': 'WindSpd_{Std}'
        },
        'knmi10min': {
            'stations': ['Rotterdam Geulhaven', 'Rotterdam locatie 06t'],
            'avgspeedcol': 'FF_10M_10',
            'stdspeedcol': 'FF_10M_STD_10'
        }
    }
    

    # STEP 1 prep data directories
    data_directories = utils.prep_directories(
        parent_dir=plot_config['parent_dir'], 
        data_sources=source_config_dict.keys()
        )
    
    for idx, source_config in enumerate(source_config_dict):        
        source_config_dict[source_config]['path'] = data_directories[idx]

    
    # STEP 2:
    avgvsstd.make_avgvsstd_plots(source_config_dict, plot_config)


if __name__ == '__main__':
    main()