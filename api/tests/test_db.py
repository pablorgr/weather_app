import app
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

    def test_insert_many(self):
        result = app.mongo.db.weather.insert_many(self.data)
        assert result.acknowledged
        assert set([data_obj["_id"] for data_obj in self.data]) == set(
            result.inserted_ids
        )

    def test_insert_one_and_retrieve(self):
        first_city = self.data[0]
        result = app.mongo.db.weather.insert_one(first_city)
        assert result.acknowledged
        assert first_city["_id"] == result.inserted_id
        retrieved = app.mongo.db.weather.find({"_id": first_city["_id"]})
        assert retrieved[0] == first_city

    def tearDown(self):
        for data in self.data:
            app.mongo.db.weather.delete_one(data)
