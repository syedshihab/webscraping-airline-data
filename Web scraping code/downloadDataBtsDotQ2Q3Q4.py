#! python3
# downloadDataBtsDot3.py - Download DB1B Origin-Destination market survey dataset from BTS DOT website
# @author: Syed A.M. Shihab

# ********* The download folder must be empty *************

import time, os, shutil, zipfile # shell utilities; import modules
from selenium import webdriver
from selenium.webdriver.support.ui import Select

browser = webdriver.Chrome() # Launch Chrome

# browser.get('https://www.transtats.bts.gov/DL_SelectFields.asp') # Cannot open this webpage directly
# navigate to the "Database Name: Airline Origin and Destination Survey (DB1B)" webpage instead and then click on the 'Download' button for DB1BMarket Table webpage
browser.get('https://www.transtats.bts.gov/Tables.asp?DB_ID=125&DB_Name=Airline')

# click on the download button for DB1BMarket table webpage
txt = 'Download'
webElem = browser.find_elements_by_link_text(txt)
webElem[1].click() # click on the download button for DB1BMarket table webpage

# Select geography, year and quarter
select1 = Select(browser.find_element_by_id('GEOGRAPHY'))
select2 = Select(browser.find_element_by_id('XYEAR'))
select3 = Select(browser.find_element_by_id('FREQUENCY'))
# print (select.options)
# print ([o.text for o in select.options]) # these are string-s

# List of East coast states 
state = ['Maine', 'New Hampshire', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York', 'New Jersey', 'Delaware', 'Maryland', 'Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida']
# year = ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017'] # year list flipped
# Create year list
year = []
yr = 1993
while yr<2018:
    year = year + [str(yr)]
    yr = yr + 1

# year = ['1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',...
# '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']   
quarter = ['Q 2','Q 3','Q 4'] # Quarter list
quarter2 = ['Q2','Q3','Q4'] # This list will be used for naming folders containing quarterly data

# Select the checkboxes for OriginCityMarketID, DestCityMarketID, Passengers and uncheck the rest
checkboxElem1 = browser.find_element_by_css_selector('input[value="ORIGIN_AIRPORT_ID"]') # Uncheck
checkboxElem2 = browser.find_element_by_css_selector('input[value="ORIGIN_AIRPORT_SEQ_ID"]') # Uncheck
##checkboxElem3 = browser.find_element_by_css_selector('input[value="ORIGIN_CITY_MARKET_ID"]')
checkboxElem4 = browser.find_element_by_css_selector('input[value="DEST_AIRPORT_ID"]') # Uncheck
checkboxElem5 = browser.find_element_by_css_selector('input[value="DEST_AIRPORT_SEQ_ID"]') # Uncheck
##checkboxElem6 = browser.find_element_by_css_selector('input[value="DEST_CITY_MARKET_ID"]')
checkboxElem7 = browser.find_element_by_css_selector('input[value="PASSENGERS"]') # Check it
# Uncheck unnecessary attributes
checkboxElem1.click()
checkboxElem2.click()
checkboxElem4.click()
checkboxElem5.click()
checkboxElem7.click()

# Click Download button to download the data file for the selected state, year and quarter
name1 = 'Download'
webElem2 = browser.find_element_by_name(name1)
browser.execute_script("window.scrollBy(0, -1000);") # scroll all the way to the top of the webpage;
# this is necessary to scroll the "Download-button" element into view; try to place the elements in the center of viewport to avoid the problem of
# "element is not clickable at the point (x,y)"

downloadPath = 'C:\\Users\\Syed\\Downloads' # Path of the default download directory of chrome browser
qq = 0 # qq will be used for indexing quarter2 list            

for q in quarter:
    select3.select_by_visible_text(q)
    # os.getcwd() = 'C:\\Users\\Syed\\AppData\\Local\\Programs\\Python\\Python36-32'
    os.makedirs(os.path.join('C:\\Users\\Syed\\AppData\\Local\\Programs\\Python\\Python36-32\\btsDataset',quarter2[qq])) # make a new folder for each quarter: Q1, Q2, Q3 and Q4
    
    # browser.execute_script("return arguments[0].scrollIntoView();", webElem2) # Does not work
    for y in year:
        select2.select_by_visible_text(y)
        os.makedirs(os.path.join('C:\\Users\\Syed\\AppData\\Local\\Programs\\Python\\Python36-32\\btsDataset',quarter2[qq],y))
        folderPath = os.path.join('C:\\Users\\Syed\\AppData\\Local\\Programs\\Python\\Python36-32\\btsDataset',quarter2[qq],y)
        for s in state:
            select1.select_by_visible_text(s)
            # browser.execute_script("return arguments[0].scrollIntoView();", webElem2) # Does not work
            webElem2.click() # click on the download button to download the csv file
            stateYrQrFilename = s + '_' + y + '_' + quarter2[qq] + '.csv' # s -> state, y -> year, quarter2[qq] -> quarter
            print('Downloading',stateYrQrFilename,'file') ###
            # time delay of 5 seconds to let download complete 
            # time.sleep(5)
            
            downloadStatus = 0
            while downloadStatus==0:
                time.sleep(7) # downloadStatus is still equal to 0 # Wait an additional 5 seconds to allow the completion of the download 
                listFilenames = os.listdir(downloadPath) # list of filenames in downloadPath directory: ['864172104_T_DB1B_MARKET.zip', 'desktop.ini']
                print('downloadPathFilenames = ',listFilenames)  ###
                for filename in listFilenames:
                    if filename.endswith('.zip'): # identify the zip file; 
                        zipFilename = filename
                        downloadStatus = 1
                        print('zipFilename = ',zipFilename)  ###
                        print('downloadStatus = ',downloadStatus)  ###
        
        
            zipObject = zipfile.ZipFile(os.path.join(downloadPath,zipFilename)) # Creates a zip file object
            zipObject.extractall(folderPath) # extract/unzip the downloaded file to the folderPath directory
            csvFilename = zipObject.namelist()
            zipObject.close()
            # Rename the name of the file to filename = NY_Y20**_Q* (e.g MA_2017_Q2)
            # stateYrQrFilename = s + '_' + y + '_' + quarter2[qq] + '.csv' # s -> state, y -> year, quarter2[qq] -> quarter
            os.rename(os.path.join(folderPath,csvFilename[0]),os.path.join(folderPath,stateYrQrFilename))
            folderPathFilenames = os.listdir(folderPath) ### list of filenames in downloadPath directory: ['864172104_T_DB1B_MARKET.zip', 'desktop.ini']
            print('folderPathFilenames = ',folderPathFilenames)  ###
            #  permanently delete the recently downloaded zip file in the download directory
            os.unlink(os.path.join(downloadPath,zipFilename))
            listFilenames = os.listdir(downloadPath) ### list of filenames in downloadPath directory: ['864172104_T_DB1B_MARKET.zip', 'desktop.ini']
            print('downloadPathFilenames = ',listFilenames)  ###
             
            
        
    qq = qq + 1 # increment qq

    # Each state will have 40 files worth of data (10 years * 4 quarters = 40). For each quarter, there will be 14 files inside each 'year' folder
    # corresponding to the 14 states of the Eastcoast
