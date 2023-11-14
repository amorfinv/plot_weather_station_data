
import utils
from avgdirection import directionplot

def main():

    plot_config = {
        'parent_dir': 'data',
        'plot_title': 'Average wind direction',
        'date_range': ['2022-01-01','2022-12-31']
    }
    

    source_config_dict = {
        'tudelft': {
            'stations': ['SpaansePolder', 'Delfshaven'],
            'column': 'WindDir_{Avg}'
        },
        'knmi1hr': {
            'stations': ['Rotterdam locatie 24t'],
            'column': 'DD'
        },
        'knmi10min': {
            'stations': ['Rotterdam Geulhaven', 'Rotterdam locatie 06t'],
            'column': 'DD_10'
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
    directionplot.make_direction_plots(source_config_dict, plot_config)


if __name__ == '__main__':
    main()