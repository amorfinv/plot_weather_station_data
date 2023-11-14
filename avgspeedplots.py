
import utils
from avgspeed import speedplot

def main():

    plot_lognormal = True
    
    parent_dir = 'data'

    plot_title = 'Average wind speeds'
      

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
    
    date_range = ['2022-01-01','2022-12-31']

    # STEP 1 prep data directories
    data_directories = utils.prep_directories(
        parent_dir=parent_dir, 
        data_sources=source_config_dict.keys()
        )
    
    for idx, source_config in enumerate(source_config_dict):        
        source_config_dict[source_config]['path'] = data_directories[idx]

    
    # STEP 2:
    speedplot.make_speed_plots(source_config_dict, date_range, plot_title)


if __name__ == '__main__':
    main()