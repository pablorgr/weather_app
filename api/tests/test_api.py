import app
from copy import deepcopy
from unittest import TestCase


class TestAPI(TestCase):
    def setUp(self):
        self.data = [
            {
                "city": "fakecity",
                "info": {
                    "weather": [
                        {
                            "id": 100,
                            "main": "Clear",
                            "description": "clear sky",
                        }
                    ]
                },
            },
            {
                "city": "fakecity2",
                "info": {
                    "weather": [
                        {
                            "id": 200,
                            "main": "Cloud",
                            "description": "cloudy sky",
                        }
                    ]
                },
            },
        ]
        app.mongo.db.weather.insert_many(self.data)

    def test_index(self):
        with app.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200
            assert response.is_json
            json_result = response.get_json()
            for data in self.data:
                assert {"city": data["city"], "info": data["info"]} in json_result

    def test_filter(self):
        city_data = self.data[0]
        with app.app.test_client() as client:
            response = client.get(f"/?city={city_data['city']}")
            assert response.status_code == 200
            assert response.is_json
            json_result = response.get_json()
            assert json_result["city"] == city_data["city"]
            assert json_result["info"] == city_data["info"]

    def tearDown(self):
        object_cities = [obj["city"] for obj in self.data]
        app.mongo.db.weather.delete_many({"city": {"$in": object_cities}})