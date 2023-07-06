from fastapi import FastAPI
from fastapi.responses import FileResponse
import pandas as pd
import datetime

app = FastAPI()

# read data
data = pd.read_csv('data.csv')

@app.get("/",  response_class=FileResponse)
async def home():
    """
    This method will return documentation to use the API.
    - **Params:**
        None
    - **Returns:**
      - (string) : documentation for the API 

    #### Example:

    [http://localhost:8080/](http://localhost:8080/)

    #### Response:

        {
            "total": 1000000,
            "params": {
                "country": null,
                "year": null
            }
            "success": true,
        }

    """
    return 'README.md'

@app.get("/countries")
async def countries():
    """
    This method will return list of unique countries from the db
    - **Params:**
      None
    - **Returns:**
      - (list) : list of unique countries from the db

    #### Example:

    [http://localhost:8080/countries/](http://localhost:8080/countries/)

    #### Response:

        {"countries":["Afghanistan","Albania","Algeria","American Samoa"]}

    """

    countries = data["Country"].unique()
    return {"countries": countries.tolist(), "success": True}

@app.get("/regions/")
async def regions():
    """
    This method will return list of available WHO regions from the db
    - **Params:**
      None
    - **Returns:**
      - (list) : list of available WHO regions from the db

    #### Example:

    [http://localhost:8080/regions/](http://localhost:8080/regions/)

    #### Response:
        
        {
        "regions": [
            "EMRO",
            "EURO",
            "AFRO",
            "WPRO",
            "AMRO",
            "SEARO",
            "Other"
        ]
        }

    """

    countries = data["WHO_region"].unique()
    return {"regions": countries.tolist(), "success": True}

@app.get("/deaths/")
async def deaths(country:str = None, region:str = None, year:int = None):
    """
    This method will return a total death count or can be filtered by country, year and region.
    - **Params:**
      - country (str) : A country name
      - region (str) : A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/deaths/](http://localhost:8080/deaths/)

    #### Response 1:

        {
            "total": 6945714,
            "params": {
                "country": null,
                "region": null,
                "year": null
            },
            "success": true
        }

    #### Example 2:

    [http://localhost:8080/deaths/?country=Brazil&year=2023](http://localhost:8080/deaths/?country=Brazil&year=2023)

    #### Response 2:

       {
            "total": 9665,
            "params": {
                "country": "Brazil",
                "region": null,
                "year": 2023
            },
            "success": true
        }

    """

    temp_data = data.copy()
    try:
        if year:
            temp_data = temp_data.loc[(data["Date_reported"].str[:4] == str(year))]
        if country:
            temp_data = temp_data.loc[(data["Country"] == country)]
        if region:
            temp_data = temp_data.loc[(data["WHO_region"] == region)]  

        return {
                "total": int(temp_data["New_deaths"].sum()),
                "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": True
            }
    except:
        return {
                "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": False
            }
    
@app.get("/cases/")
async def cases(country:str = None, region:str = None, year:int = None):
    """
    This method will return a total cases count or can be filtered by country, year and region.
    - **Params:**
      - country (str) : A country name
      - region (str) : A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/cases/](http://localhost:8080/cases/)

    #### Response 1:

        {
            "total": 768187096,
            "params": {
                "country": null,
                "region": null,
                "year": null
            },
            "success": true
        }

    #### Example 2:

    [http://localhost:8080/deaths/?region=AMRO&year=2023](http://localhost:8080/deaths/?region=AMRO&year=2023)

    #### Response 2:

        {
            "total": 6795571,
            "params": {
                "country": null,
                "region": "AMRO",
                "year": 2023
            },
            "success": true
        }

    """

    temp_data = data.copy()
    try:
        if year:
            temp_data = temp_data.loc[(data["Date_reported"].str[:4] == str(year))]
        if country:
            temp_data = temp_data.loc[(data["Country"] == country)]
        if region:
            temp_data = temp_data.loc[(data["WHO_region"] == region)]  

        return {
                "total": int(temp_data["New_cases"].sum()),
                "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": True
            }
    except:
        return {
                "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": False
            }

@app.get("/max_deaths/")
async def max_deaths(min_date:str = None, max_date:str = None):
    """
    This method will return the country with the most deaths.
    - **Params:**
      - min_date (str) : lower range for filter by date
      - max_date (str) : upper range for filer by date
    - **Returns:**
      - (str) : country with the most deaths

    #### Example 1:

    [http://localhost:8080/max_deaths/](http://localhost:8080/max_deaths/)

    #### Response 1:
        {
            "country": "United States of America",
            "params": {
                "min_date": null,
                "max_date": null
            },
            "success": true
        }   

    #### Example 2:

    [http://localhost:8080/max_deaths/?min_date=2021-06-01&max_date=2021-12-31](http://localhost:8080/max_deaths/?min_date=2021-06-01&max_date=2021-12-31)

    #### Response 2:

        {
            "country": "United States of America",
            "params": {
                "min_date": "2021-06-01",
                "max_date": "2021-12-31"
            },
            "success": true
        }

    """

    temp_data = data.copy()
    try:
        temp_data['Date_reported'] = pd.to_datetime(data['Date_reported']).dt.date

        if not min_date and max_date:
            raise ValueError("min date not provied")
        if not max_date and min_date:
            raise ValueError("max date not provied")

        if min_date and max_date:
            min_year, min_month, min_day = map(int, min_date.split('-'))
            max_year, max_month, max_day = map(int, max_date.split('-'))
            min_date_filter = datetime.date(min_year, min_month, min_day)
            max_day_filter = datetime.date(max_year, max_month, max_day)

            temp_data = temp_data[(temp_data["Date_reported"] >= min_date_filter) & (temp_data["Date_reported"] <= max_day_filter)]

        country = temp_data.groupby("Country")["New_deaths"].sum().idxmax()

        return {
                "country": country,
                "params": {
                    "min_date": min_date,
                    "max_date": max_date,
                },
                "success": True
            }
    except :
        return {
                "params": {
                    "min_date": min_date,
                    "max_date": max_date,
                },
                "success": False
            }

@app.get("/min_deaths/")
async def min_deaths(min_date:str = None, max_date:str = None):
    """
    This method will return the country with the least deaths.
    - **Params:**
      - min_date (str) : lower range for filter by date
      - max_date (str) : upper range for filer by date
    - **Returns:**
      - (str) : country with the least deaths

    #### Example 1:

    [http://localhost:8080/min_deaths/](http://localhost:8080/min_deaths/)

    #### Response 1:
        {
            "country": "Democratic People's Republic of Korea",
            "params": {
                "min_date": null,
                "max_date": null
            },
            "success": true
        }

    #### Example 2:

    [http://localhost:8080/min_deaths/?min_date=2021-06-01&max_date=2021-12-31](http://localhost:8080/min_deaths/?min_date=2021-06-01&max_date=2021-12-31)

    #### Response 2:

        {
            "country": "American Samoa",
            "params": {
                "min_date": "2021-06-01",
                "max_date": "2021-12-31"
            },
            "success": true
        }

    """

    temp_data = data.copy()
    try:
        temp_data['Date_reported'] = pd.to_datetime(data['Date_reported']).dt.date

        if not min_date and max_date:
            raise ValueError("min date not provied")
        if not max_date and min_date:
            raise ValueError("max date not provied")

        if min_date and max_date:
            min_year, min_month, min_day = map(int, min_date.split('-'))
            max_year, max_month, max_day = map(int, max_date.split('-'))
            min_date_filter = datetime.date(min_year, min_month, min_day)
            max_day_filter = datetime.date(max_year, max_month, max_day)

            temp_data = temp_data[(temp_data["Date_reported"] >= min_date_filter) & (temp_data["Date_reported"] <= max_day_filter)]

        country = temp_data.groupby("Country")["New_deaths"].sum().idxmin()

        return {
                "country": country,
                "params": {
                    "min_date": min_date,
                    "max_date": max_date,
                },
                "success": True
            }
    except :
        return {
                "params": {
                    "min_date": min_date,
                    "max_date": max_date,
                },
                "success": False
            }

@app.get("/avg_deaths/")
async def avg_deaths():
    """
    This method will return average number of deaths between all countries
    - **Params:**
      None
    - **Returns:**
      - (list) : list of coutires with average number of deaths

    #### Example:

    [http://localhost:8080/avg_deaths/](http://localhost:8080/avg_deaths/)

    #### Response:
        
        {
            "avg_deaths": 23.149139120523127,
            "success": true
        }
    """
    try:
        average_deaths = data["New_deaths"].mean()
        return {"avg_deaths": float(average_deaths), "success": True}
    except:
        return {"success": False}