This scripts fetches information from the website and stores it in the .xls file.

PREREQUISITES

1. Make sure the geckodriver executable directory is in PATH.
       
       cp geckodriver /usr/local/bin

2. Make sure all the necessary dependencies are installed.
        
        pip install selenium scrapy xlwt

3. Make sure the Python interpreter is version 3.0+
       
        python --version
        Python 3.8.1

USAGE

1. Execute the script.
        
        python scarletblue_scraper.py

2. Solve CAPTCHA in the pop-up window.

3. Wait until the script finishes collecting data. 
Explicit message "Data written to scarletblue.xls will appear.
