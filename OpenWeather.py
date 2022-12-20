#OpenWeather API
#You will need to install prettytable with the below command
#python -m pip install -U prettytable
import requests, json, sys
from prettytable import PrettyTable

fiveDay = PrettyTable()
airpol = PrettyTable()

#GLOBALS
#Default location is Plano, TX
lat = 33.019675
lon = -96.699241
apiKey = "8012016a2a5b58b63168873805ecc018"
spacer = "-----------------------------------------"
format = 0 
cho = 0

#function for getting current weather conditions
def CurrentWeather():
    api_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid={}".format(lat, lon, apiKey)
    response = requests.get(api_url)
    resp_dict = response.json()

    #Print Info
    print(spacer)
    print(resp_dict["name"])
    print(spacer)
    print("{}: {}".format(resp_dict["weather"][0]["main"],resp_dict["weather"][0]["description"]))
    print("{} F".format(resp_dict["main"]["temp"]))
    print("High({}F) Low({}F)".format(resp_dict["main"]["temp_min"],resp_dict["main"]["temp_max"]))
    
def FiveDay():
    api_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=imperial&appid={}".format(lat, lon, apiKey)
    response = requests.get(api_url)
    resp_dict = response.json()
    
    #Declare Variables
    days = []
    prev_date = ""
    temp = 0
    highTemp = 0
    lowTemp = 0
    medianTemp = []
    weather = []
    highs = []
    lows = []
    count = 1
    prev_date = ""
    
    #Loo[ through all of the returned date/time values in the API call
    for x in range(0,(len(resp_dict["list"]))-1):
        date = ((resp_dict["list"][x]["dt_txt"]).split(' '))[0]
        time = ((resp_dict["list"][x]["dt_txt"]).split(' '))[1]
        
        #We only want to display one instance of each day, as this api is broken apart by 3 hour intervals
        #We gather data until the date changes to the next day
        if date != prev_date and count != 1:
            #Append the rows that will eventually be added to the table
            days.append(date)
            weather.append(resp_dict["list"][x-1]["weather"][0]["main"])
            highs.append("High: " + str(int(highTemp)) +"F")
            lows.append("Low: " + str(int(lowTemp))+"F")
            #Reset counters and values
            temp = 0
            count = 1
        else:
            #Convert temp to float in case median formulas need to be applied
            temp =(float(resp_dict["list"][x]["main"]["temp"]))
            if count == 1:
                #Initial High and Low assignment
                highTemp = temp
                lowTemp = temp
            else:
                #Adjusts high and low based on 3 hour interval reported
                if temp > highTemp:
                    highTemp = temp
                if temp < lowTemp:
                    lowTemp = temp
            count += 1
        prev_date = date
    
    #Create table and merge together
    fiveDay.field_names = days
    merged = [weather, highs, lows]
    fiveDay.add_rows(merged)
    
    print(fiveDay)

    
def AirPoll():
    api_url = "http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&units=imperial&appid={}".format(lat, lon, apiKey)
    response = requests.get(api_url)
    resp_dict = response.json()
    comp = resp_dict["list"][0]["components"]
    
    #Create and print table
    airpol.field_names = ["CO", "NO", "NO2", "O3", "SO2", "PM2_5", "PM10", "NH3"]
    airpol.add_row([comp["co"], comp["no"], comp["no2"], comp["o3"], comp["so2"], comp["pm2_5"], comp["pm10"], comp["nh3"]])
        
    print("Air Pollution")
    print(airpol)
    
def ChangeLoc():
    zip = input("Please enter your zip code: ")
    api_url = "http://api.openweathermap.org/geo/1.0/zip?zip={},US&appid={}".format(zip, apiKey)
    response = requests.get(api_url)
    resp_dict = response.json()
    
    #Replace global values with lat and lon from zip api
    lat = resp_dict["lat"]
    lon = resp_dict["lon"]
    
    print("Location changed to: {}".format(resp_dict["name"]))
    return lat, lon
    
#Main Function will continue to loop until user exits
while cho != 5:
    print("\nPlease choose a Weather Forecast Option\n{}\n1: Current Forecast\n2: 5 Day Forecast\n3: Air Pollution Forecast\n4: Change Location\n5: Quit".format(spacer))
    print(spacer)
    cho = input("\nSelection: ")
    
    #Runs function based on user input
    match cho:
        case '1':
            CurrentWeather()
        case '2':
            FiveDay()
        case '3':
            AirPoll()
        case '4':
            lat, lon = ChangeLoc()
        case '5':
            sys.exit()
