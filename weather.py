import requests
import datetime as dt
class Weather:

    def __init__(self):
        self.data = 0
    



    lines = []
    with open('env.txt') as env_file:
        for line in env_file:
            lines.append(line)

    global env_key

    env_key =  str(lines[3]);

    global base 
    base = "https://api.openweathermap.org/data/2.5/weather?"


    def to_farenheit(self,kelvin):
        self.kelvin = kelvin
        celcius  = kelvin - 273.15
        farenheit = celcius * (9/5) + 32
        return farenheit
    def to_celcius(self,kelvin):
        self.kelvin = kelvin
        celcius = kelvin - 273.15
        return celcius



    def weatherreport(self,city,option):
        option = str(option)
        url = base + "appid=" + env_key + "&q=" + str(city)
        response = requests.get(url).json()
        temp = 0  
        template = " "
        feel_like = 0
        if(option.lower() == 'celcius'):
            temp = self.to_celcius(self,response["main"]["temp"])
            feel_like = self.to_celcius(self,response["main"]["feels_like"])
            template = " celcius"
        elif(option.lower() == 'farenheit'):
            temp = self.to_farenheit(self,response["main"]["temp"])
            feel_like = self.to_farenheit(self,response["main"]["feels_like"])
            template = " farenheit"
        else:
            print("Not a valid option, please pick between Celcius and Farenheit")
        
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

        print(f"Temperature in {city}: {temp:.2f}{template} ")
        print(f"Feels Like {feel_like:.2f}{template}")
        print(f"Humidity {humidity}%")
        print(f"Wind Speed {wind_speed}m/s")
        print(f"General Weather Description {description}")
        print(f"Sunrise Time : {sunrise_time} local time")
        print(f"Sunset Time : {sunset_time} local time")

