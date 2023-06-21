"""
Overview:
This program uses Selenium to render a web page and then uses BeautifulSoup to parse the HTML.
The program then prints the parsed HTML to the console.
"""

import time                                             # needed for the sleep function

from bs4 import BeautifulSoup                           # used to parse the HTML
from selenium import webdriver                          # used to render the web page
from seleniumwire import webdriver                      
from selenium.webdriver.chrome.service import Service   # Service is only needed for ChromeDriverManager


import functools                                        # used to create a print function that flushes the buffer
flushprint = functools.partial(print, flush=True)       # create a print function that flushes the buffer immediately

def asyncGetWeather(url):
        """Returns the page source HTML from a URL rendered by ChromeDriver.
        Args:
            url (str): The URL to get the page source HTML from.
        Returns:
            str: The page source HTML from the URL.
            
        Help:
        https://stackoverflow.com/questions/76444501/typeerror-init-got-multiple-values-for-argument-options/76444544
        """
        
        #change '/usr/local/bin/chromedriver' to the path of your chromedriver executable
        service = Service(executable_path='/usr/local/bin/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        
        driver = webdriver.Chrome(service=service,options=options)  # run ChromeDriver
        flushprint("Getting page...")
        driver.get(url)                                             # load the web page from the URL
        flushprint("waiting 6 seconds for dynamic data to load...")
        time.sleep(6)                                               # wait for the web page to load
        flushprint("Done ... returning page source HTML")
        render = driver.page_source                                 # get the page source HTML
        driver.quit()                                               # quit ChromeDriver
        
        # parse the HTML
        soup = BeautifulSoup(render, 'html.parser')
        # find the appropriate tag that contains the weather data
        history = soup.find('lib-city-history-observation')
        
        data = []

        # get filter from url
        filter = url.split('/')[-3]
        
        if filter == 'daily':
            header = history.find('thead')
            header = header.find_all('th')
            header_values = [ele.text.strip() for ele in header]
            data.append(header_values)

            body = history.find('tbody')
            rows = body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
        elif filter == 'weekly' or filter == 'monthly':
            header = history.find('thead')
            header = history.find('tr')
            header = header.find_all('td')
            header_values = [ele.text.strip() for ele in header]
            data.append(header_values)
            body_data = []
            body = history.find('tbody').find('tr')
            for td_row in body.findAll('td', recursive=False):
                temp_data = []
                tr_table = td_row.find('table')
                for data_tr in tr_table.findAll('tr'):
                    values = [ele.text.strip() for ele in data_tr]
                    temp_data.append([ele for ele in values if ele])
                body_data.append(temp_data)
            formatted_data = []
            for i in range(len(body_data[0])):
                formatted_data.append([body_data[j][i] for j in range(len(body_data)) ] )
            data += formatted_data
                                     
        # return the parsed HTML
        return data


    
if __name__=='__main__':

    # Could be a good idea to use the buildWeatherURL function from gui.py
    url = 'http://www.wunderground.com/history/daily/KCHO/date/2020-12-31'

    # get the page source HTML from the URL
    page = asyncGetWeather(url)

    # parse the HTML
    soup = BeautifulSoup(page, 'html.parser')
    
    # find the appropriate tag that contains the weather data
    history = soup.find('lib-city-history-observation')

    # return the parsed HTML
    print(history.prettify())