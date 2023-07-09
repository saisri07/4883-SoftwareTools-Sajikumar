# A08 - Fast Api with Covid Data
## ATHUL SAJIKUMAR
## Description:

This project will create a RESTful API using FastAPI that provides access to COVID-19 data. The API will fetch the data from data.csv (covid data) and expose endpoints to retrieve various statistics related to COVID-19 cases. 





### End Points

- /  : return documentation to use the API. 

- /countries : return list of unique countries from the db

     Example:

        [http://localhost:8080/countries/](http://localhost:8080/countries/)

     Response:

        {"countries":["Afghanistan","Albania","Algeria","American Samoa"]}
        
- /regions : return list of available WHO regions from the db

     Example:

        [http://localhost:8080/regions/](http://localhost:8080/regions/)

     Response:
        
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
        
- /deaths : return a total death count or can be filtered by country, year and region.

     - **Params:**
      - country (str) : A country name
      - region (str) : A region name
      - year (int) : A 4 digit year
     - **Returns:**
      - (int) : The total sum based on filters (if any)

     Example 1:

        [http://localhost:8080/deaths/](http://localhost:8080/deaths/)

     Response 1:

        {
            "total": 6945714,
            "params": {
                "country": null,
                "region": null,
                "year": null
            },
            "success": true
        }

     Example 2:

        [http://localhost:8080/deaths/?country=Brazil&year=2023](http://localhost:8080/deaths/?country=Brazil&year=2023)

     Response 2:

       {
            "total": 9665,
            "params": {
                "country": "Brazil",
                "region": null,
                "year": 2023
            },
            "success": true
        }
        
- /cases :  return a total cases count or can be filtered by country, year and region.

    - **Params:**
      - country (str) : A country name
      - region (str) : A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    Example 1:

        [http://localhost:8080/cases/](http://localhost:8080/cases/)

     Response 1:

        {
            "total": 768187096,
            "params": {
                "country": null,
                "region": null,
                "year": null
            },
            "success": true
        }

    Example 2:

        [http://localhost:8080/deaths/?region=AMRO&year=2023](http://localhost:8080/deaths/?region=AMRO&year=2023)

    Response 2:
    
        {
            "total": 6795571,
            "params": {
                "country": null,
                "region": "AMRO",
                "year": 2023
            },
            "success": true
        }

- /max_deaths: return the country with the most deaths.
    
    - **Params:**
      - min_date (str) : lower range for filter by date
      - max_date (str) : upper range for filer by date
    - **Returns:**
      - (str) : country with the most deaths

    Example 1:

        [http://localhost:8080/max_deaths/](http://localhost:8080/max_deaths/)

    Response 1:
        {
            "country": "United States of America",
            "params": {
                "min_date": null,
                "max_date": null
            },
            "success": true
        }   

    Example 2:

        [http://localhost:8080/max_deaths/?min_date=2021-06-01&max_date=2021-12-31](http://localhost:8080/max_deaths/?min_date=2021-06-01&max_date=2021-12-31)

    Response 2:

        {
            "country": "United States of America",
            "params": {
                "min_date": "2021-06-01",
                "max_date": "2021-12-31"
            },
            "success": true
        }

- /min_deaths: return the country with the least deaths.

    - **Params:**
      - min_date (str) : lower range for filter by date
      - max_date (str) : upper range for filer by date
    - **Returns:**
      - (str) : country with the least deaths

    Example 1:

        [http://localhost:8080/min_deaths/](http://localhost:8080/min_deaths/)

    Response 1:
    
        {
            "country": "Democratic People's Republic of Korea",
            "params": {
                "min_date": null,
                "max_date": null
            },
            "success": true
        }

    Example 2:

        [http://localhost:8080/min_deaths/?min_date=2021-06-01&max_date=2021-12-31](http://localhost:8080/min_deaths/?min_date=2021-06-01&max_date=2021-12-31)

    Response 2:

        {
            "country": "American Samoa",
            "params": {
                "min_date": "2021-06-01",
                "max_date": "2021-12-31"
            },
            "success": true
        }

- /avg_deaths: average number of deaths between all countries.

    Example:

        [http://localhost:8080/avg_deaths/](http://localhost:8080/avg_deaths/)

    Response:
        
        {
            "avg_deaths": 23.149139120523127,
            "success": true
        }


        ## Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   |   [data.csv](https://github.com/ATHUL107/4883-SoftwareTools-Sajikumar/blob/main/Assignments/A08/data.csv)    | file that holds covid data    |
|   2  |    [api.py](https://github.com/ATHUL107/4883-SoftwareTools-Sajikumar/blob/main/Assignments/A08/api.py)       | file that holds python code for api routes    |


        
### How to run the code

- Install uvicorn if it is not already installed using the following command

    ```pip3 install uvicorn(standard)```
 

- Start the server using the following command:

    ``` uvicorn api:app –-reload ```
