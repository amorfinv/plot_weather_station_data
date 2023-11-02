import os
from functions import download_file, list_csv_files_at_url
# INPUT DATA
url='https://weather.tudelft.nl/csv/'           # Base location of the data source
outputfilelocation = 'data/'                    # Where do you want to store the data
# Ensure that the base location exists
if os.path.exists(outputfilelocation) and os.path.isdir(outputfilelocation):
    print("Starting the download.....") 
else:
    print("Creating data/ folder....")
    os.makedirs(outputfilelocation)
# Fetch the files available for download
file2down = list_csv_files_at_url(url)
# Index and download the files
for myFile in file2down:
    downfilename=outputfilelocation+myFile.rsplit('/', 1)[-1]
    download_file(myFile,downfilename)
# Get the header files containing the database keys
myKey = url+'/fields.txt'
download_file(myKey,'data/fields.txt')



