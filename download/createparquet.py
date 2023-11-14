import pandas as pd
import gzip
from pathlib import Path
from itertools import islice
import os

def create_parquet(zip_directory, filename):

    file_path  = os.path.join(zip_directory,filename + '.parquet')

    if os.path.exists(file_path):
        print(f'{file_path} exists! Delete to recreate.')
        return
    else:
        print('Creating parquet file for easier loading')
    
    # Get a list of all zip files in the directory
    gz_files = list(Path(zip_directory).glob('*.gz'))


    # Initialize an empty list to store DataFrames
    dfs = []

    # get the 23rd line of the first file to use as a delimeter
    def get_column_info(file_path, line_number=23):

        # read the line with headers
        with gzip.open(file_path, 'rt') as file:
            specific_line = next(islice(file, line_number - 1, line_number)).strip()

        # replace # with ##
        search_line = specific_line.replace('# ', '##')

        # get the space 
        inter_column_width = []
        counter = 0

        # Iterate through the characters in the text
        for char in search_line:
            if char == ' ':
                counter += 1
            else:
                if counter > 0:
                    inter_column_width.append(counter)
                    counter = 0

        # Add the count for the last word (if any)
        if counter > 0:
            inter_column_width.append(counter)

        # now create the column list by adding it back to the columns
        columns = search_line.split()
        column_text_lengths = [len(col) for col in columns]

        # now add the inter_column widths
        column_widths  = []
        for idx, inter_width in enumerate(inter_column_width):

            width = inter_width + column_text_lengths[idx]
            column_widths.append(width)

        # add the last column width
        column_widths.append(column_text_lengths[-1])

        # now remove the ## from search line
        columns = specific_line.replace('# ', '')

        columns = columns.split()

        return columns, column_widths

    # get column names and column widths
    columns, column_widths = get_column_info(gz_files[0])


    fwf_args = { 
        'on_bad_lines': 'skip',
        'names': columns,
        'na_values': ['NaN'],
        'comment': "#",
        'widths': column_widths

    }
    # Loop through each gzipped file
    for gz_file in gz_files:
        # Read the gzipped CSV file into a Pandas DataFrame
        with gzip.open(gz_file, 'rt') as f:
            
            # get the header in line 23
            df = pd.read_fwf(f, **fwf_args)

            df['DTG'] = pd.to_datetime(df['DTG'], errors='coerce')

            print(f'Parsing {gz_file}')
            
            # Append the DataFrame to the list
            dfs.append(df)


    # Concatenate the DataFrames in the list along the rows
    combined_df = pd.concat(dfs, ignore_index=True)

    # Write the combined DataFrame to a Parquet file
    combined_df.to_parquet(file_path, index=False)

    print(f"Combined DataFrame saved to {file_path}")
