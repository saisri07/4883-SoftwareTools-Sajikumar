import gui
import get_weather

from bs4 import BeautifulSoup

# url = 'http://www.wunderground.com/history/daily/KCHO/date/2020-12-31'

def getDataForTalbe(tableHTML):
    table = BeautifulSoup(tableHTML, 'html.parser')
    data = []
    print('&' * 10)
    print(table)
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')  
        cols = [ele.text.strip() for ele in cols]
        # data.append([ele for ele in cols if ele]) # Get rid of empty values

    return data

if __name__=='__main__':
    # get url to fetch data from
    url = gui.buildWeatherURL()

    # use try-except to handle any error
    try:
        # get table data from the url
        tableData = get_weather.asyncGetWeather(url)
        # show table windows
        gui.showWeatherTable(tableData)
    
    except:
        gui.showErrorPopUp()
