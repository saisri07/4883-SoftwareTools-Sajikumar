""" 
Description:
    This is an example gui that allows you to enter the appropriate parameters to get the weather from wunderground.
TODO:
    - You will need to change the text input boxes to drop down boxes and add the appropriate values to the drop down boxes.
    - For example the month drop down box should have the values 1-12.
    - The day drop down box should have the values 1-31.
    - The year drop down box should have the values ??-2023.
    - The filter drop down box should have the values 'daily', 'weekly', 'monthly'.
"""
import PySimpleGUI as sg      

def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    from datetime import datetime
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day':datetime.now().day,
        'month':datetime.now().month,
        'year':datetime.now().year
    }

def showWeatherTable(data):
    """ Display gui to show weather data
        Args:
            data: List of list containing table header and data
        Returns:
            None
    """
    layout = [
        [sg.Table(values=data[1:], headings=data[0],
                alternating_row_color='#8c8c8c', num_rows=20, expand_x=True, expand_y=True,justification='center')]
        ]

    window = sg.Window('Weather Data', layout)
    event, values = window.read()
    window.close()
    
def showErrorPopUp(error_msg = "There was en error fetching the data or data not available for given values. Please try again!"):
    """ Display error popup
        Args:
            error_msg: message to show in popup as string
        Returns:
            None
    """
    sg.popup(error_msg)

def buildWeatherURL(month=None, day=None, year=None, airport=None, filter=None):
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month,current_day,current_year = currentDate('tuple')

    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year
    
    # read codes from csv file
    import csv
    codes = []
    with open('C:\\Drive_B\\Stuff\\Python Assignment Scapping\\4883-Software-Tools\\Assignments\\A07\\airport-codes.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            codes.append(row['ident'])

    # create lists for days, months and years
    days = [i for i in range(1,13)]
    months = [i for i in range(1,32)]
    years = [i for i in range(2023,1900,-1)]
    filters = ['daily', 'weekly', 'monthly']
    # Create the gui's layout using text boxes that allow for user input without checking for valid input
    layout = [
        [sg.Text('Month')],[sg.Combo(days, default_value=days[0], size=(10,1))],
        [sg.Text('Day')],[sg.Combo(months, default_value=months[0], size=(10,1))],
        [sg.Text('Year')],[sg.Combo(years, default_value=years[0], size=(10,1))],
        [sg.Text('Code')],[sg.Combo(codes, default_value='KCHO', size=(15,1))],
        [sg.Text('Daily / Weekly / Monthly')],[sg.Combo(filters, default_value=filters[0], size=(15,1), readonly=True)],
        [sg.Submit(), sg.Cancel()]
    ]      

    window = sg.Window('Get The Weather', layout)    

    event, values = window.read()
    window.close()
        
    month = values[0]
    day = values[1]
    year = values[2]
    airport = values[3]
    filter = values[4]

    if month == None or month not in months:
        month = current_month
    if day == None or day not in days:
        day = current_day
    if year == None or year not in years:
        year = current_year
    if airport == None or airport not in codes:
        airport = codes[0]

    # return the URL to pass to wunderground to get appropriate weather data
    base_url = base_url = "https://wunderground.com/history"
    return f"{base_url}/{filter}/{airport}/{year}-{month}-{day}"


if __name__=='__main__':
    buildWeatherURL()
