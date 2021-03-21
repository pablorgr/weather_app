weather_app
===
Weather API filtered by city.  

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


### Populate
Manually populate database with weather information.
```
docker-compose run api python app.py [-p|--populate]
```

### Execute Tests
```
docker-compose run api python -m unittest
```
