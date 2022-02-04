from flask import Flask, request, jsonify
from flask_restful import Api, Resource 

# run the app properly
app = Flask(__name__)
api = Api(app)

flights_data = [
    {
        "number": "LH1234",
        "neumber_passengers": 55,
        "origin": "Hamburg",
        "destination": "Stuttgart",
        "departing_time": "2022/02/04 18:00",
        "arrival_time": "2022/02/04 19:00",
        "departing_airport": "HH_Airport",
        "arrival_airport": "BL_Airport",
        "base_ticket_prices" : {
            "economy": 100,
            "business": 200
        }
    },
        {
        "number": "LH700",
        "neumber_passengers": 550,
        "origin": "TFS",
        "destination": "LPA",
        "departing_time": "2022/02/09 18:10",
        "arrival_time": "2022/02/09 19:00",
        "departing_airport": "TFS_Airport",
        "arrival_airport": "LPA_Airport",
        "base_ticket_prices" : {
            "economy": 300,
            "business": 200
        }
    },
]

class FlightsList(Resource):
    def get(self):
        
        #return flights_data
        return flights_data[1]
        #return flights_data[0]["number"]
        #return flights_data[1]["base_ticket_prices"]["economy"]

api.add_resource(FlightsList, "/flights/")

if __name__ == "__main__":
    app.run(debug=True)