#! python3
# deleteFilesDownloadFolder.py - This script is used for deleting all files in the download folder
# @author: Syed A.M. Shihab

import os, shutil # shell utilities; import modules

# Deleting all files from the download folder
downloadPath = 'C:\\Users\\Syed\\Downloads' # Path of the default download directory of chrome browser
listFilenames = os.listdir(downloadPath)
for filename in listFilenames:
    # permanently delete the recently downloaded zip file in the download directory
    if os.path.isfile(os.path.join(downloadPath,filename)):
        print('filename = ',filename)  ###
        os.unlink(os.path.join(downloadPath,filename))

    elif os.path.isdir(os.path.join(downloadPath,filename)):
        print('folder name = ',filename)  ###
        shutil.rmtree(os.path.join(downloadPath,filename))

    
    
        
    
