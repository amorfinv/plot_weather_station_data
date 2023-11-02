from functions import download_file, list_csv_files_at_url
# Test to download the data
url='https://weather.tudelft.nl/csv/'
myfile='test.dat'
# Test to list the files at the url
res = list_csv_files_at_url(url)
print("Files available at the given URL:")
for file_url in res:
    print(file_url)
# Test to download the data
#url='https://weather.tudelft.nl/csv/Centrum.csv'
#download_file(url, myfile)