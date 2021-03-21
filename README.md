weather_app
===
Weather API filtered by city.  

External APIs:  
* [REST Countries](https://restcountries.eu/)
* [OpenWeather](https://openweathermap.org/current)

## Install
Set `.env` file with data for Open weather API key and random string for Flask app secret key:
```
API_KEY=<open weather API key>
SECRET=<random string>
```
Populate database with **Populate** command.

## Usage
Boot project with `docker-compose up` and go to `localhost:5000`.  
Optionally filter by city name: `localhost:5000/?city=<city>`

### Example
`curl -X GET "localhost:5000/?city=Madrid"`
```
{
  "city": "madrid", 
  "info": {
    "base": "stations", 
    "clouds": {
      "all": 0
    }, 
    "cod": 200, 
    "coord": {
      "lat": 40.4165, 
      "lon": -3.7026
    }, 
    "dt": 1616273243, 
    "id": 3117735, 
    "main": {
      "feels_like": 1.93, 
      "humidity": 31, 
      "pressure": 1019, 
      "temp": 7.4, 
      "temp_max": 9, 
      "temp_min": 6.11
    }, 
    "name": "Madrid", 
    "sys": {
      "country": "ES", 
      "id": 6443, 
      "sunrise": 1616221088, 
      "sunset": 1616264781, 
      "type": 1
    }, 
    "timezone": 3600, 
    "visibility": 10000, 
    "weather": [
      {
        "description": "clear sky", 
        "icon": "01n", 
        "id": 800, 
        "main": "Clear"
      }
    ], 
    "wind": {
      "deg": 50, 
      "speed": 3.6
    }
  }
}
```

### Populate
Manually populate database with weather information.
```
docker-compose run api python app.py [-p|--populate]
```

### Debug
```
docker-compose run -p 5000:5000 api flask run
```

### Execute Tests
```
docker-compose run api python -m unittest
```