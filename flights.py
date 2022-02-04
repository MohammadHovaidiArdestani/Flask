from locale import currency
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort 
import random
import requests
from copy import deepcopy

# run the app properly
app = Flask(__name__)
api = Api(app)

flights_data = {
    1: {
        "id": 1,
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
    2: {
        "id": 2,
        "number": "LH700",
        "neumber_passengers": 550,
        "origin": "TFS",
        "destination": "LPA",
        "departing_time": "2022/05/09 18:10",
        "arrival_time": "2022/05/09 19:00",
        "departing_airport": "TFS_Airport",
        "arrival_airport": "LPA_Airport",
        "base_ticket_prices" : {
            "economy": 300,
            "business": 200
        }
    },
}

def abort_if_id_missing(flight_id):
    if flight_id not in flights_data:
        abort(404, message= "No flight fount with this id")
class FlightsList(Resource):
    def get(self):
        
        #return flights_data
        return flights_data
        #return flights_data[0]["number"]
        #return flights_data[1]["base_ticket_prices"]["economy"]
    def post(self):
        new_flight = request.json
        flight_id = random.randint(4,1000000)
        new_flight["id"] = flight_id

        flights_data[flight_id] = new_flight
        #return {"message": "new flight added"}
        return new_flight, 201

class Flight(Resource):
    def get(self, flight_id):
        abort_if_id_missing(flight_id)

        flight = flights_data[flight_id]

        return flight
    
    def put(self, flight_id):
        data = request.json
        flights_data[flight_id] = data

        return data
class FlightUSD(Resource):
    def get(self, flight_id):
        abort_if_id_missing(flight_id)

        resp = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur.json')
        currency_rates = resp.json()
        eur_usd = currency_rates['eur']['usd']

        flight = flights_data[flight_id]

        flight_usd = deepcopy(flight)

        flight_usd['base_ticket_prices']['economy'] = flight_usd['base_ticket_prices']['economy'] * eur_usd
        flight_usd['base_ticket_prices']['busines'] = flight_usd['base_ticket_prices']['business'] * eur_usd
           

        return flight_usd


api.add_resource(FlightsList, "/flights/")
api.add_resource(FlightUSD, "/flights/usd/<int:flight_id>")
api.add_resource(Flight, "/flights/<int:flight_id>")

if __name__ == "__main__":
    app.run(debug=True)