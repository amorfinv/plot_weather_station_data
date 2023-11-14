
import utils
from avgspeed import speedplot

def main():

    plot_config = {
        'parent_dir': 'data',
        'plot_lognormal': True,
        'plot_title': 'Average wind speeds',
        'date_range': ['2022-01-01','2022-12-31']
    }
    

    source_config_dict = {
        'tudelft': {
            'stations': ['SpaansePolder', 'Delfshaven'],
            'column': 'WindSpd_{Avg}'
        },
        'knmi1hr': {
            'stations': ['Rotterdam locatie 24t'],
            'column': 'FH'
        },
        'knmi10min': {
            'stations': ['Rotterdam Geulhaven', 'Rotterdam locatie 06t'],
            'column': 'FF_SENSOR_10'
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
    speedplot.make_speed_plots(source_config_dict, plot_config)


if __name__ == '__main__':
    main()