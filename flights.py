from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse
import random
import requests
from copy import copy

app = Flask(__name__)
api = Api(app)



flights_data = {

    1 : {
        'id': 1,
        'number': 'LH123',
        'number_passengers': 55,
        'origin': 'Tallinn',
        'destination': 'Berlin',
        'departing_time': '2022/02/04 18:00',
        'arrival_time': '2022/02/04 22:00',
        'departing_airport': 'TTL airport',
        'arrival_airport': 'Berlin airport',
        'base_ticket_prices': 123
    },
    2: {
        'id': 2,
        'number': 'LH123',
        'number_passengers': 55,
        'origin': 'Tallinn',
        'destination': 'Berlin',
        'departing_time': '2022/03/04 18:00',
        'arrival_time': '2022/03/04 22:00',
        'departing_airport': 'TTL airport',
        'arrival_airport': 'Berlin airport',
        'base_ticket_prices': 435
    },
    3: {
        'id': 3,
        'number': 'TY323',
        'number_passengers': 65,
        'origin': 'Rio de Janeiro',
        'destination': 'Paris',
        'departing_time': '2022/05/07 18:00',
        'arrival_time': '2022/02/04 22:00',
        'departing_airport': 'TTL airport',
        'arrival_airport': 'Berlin airport',
        'base_ticket_prices': 545.645
    }

}


flight_req = reqparse.RequestParser()
flight_req.add_argument('number', type=str, required=True)
flight_req.add_argument('number_passengers', type=int, required=True)
flight_req.add_argument('origin', type=str, required=True)
flight_req.add_argument('destination', type=str, required=True, help='Destination is required')
flight_req.add_argument('departing_time', type=str, required=True)
flight_req.add_argument('arrival_time', type=str, required=True)
flight_req.add_argument('departing_airport', type=str, required=True)
flight_req.add_argument('arrival_airport', type=str, required=True)
flight_req.add_argument('base_ticket_prices', type=float, required=True)


def abort_if_flight_missing(flight_id):
    if flight_id not in flights_data:
        abort(404, message='No flight found with this id')


class FlightsList(Resource):
    def get(self):
        return flights_data
    
    def post(self):
        new_flight = flight_req.parse_args()
        flight_id = random.randint(4, 100000000) # this can generate repeated ids!!!!!
        new_flight['id'] = flight_id

        flights_data[flight_id] = new_flight

        return new_flight, 201
        
    

class Flight(Resource):
    def get(self, flight_id):
        abort_if_flight_missing(flight_id)

        flight = flights_data[flight_id]

        return flight
    
    def put(self, flight_id):
        data = flight_req.parse_args()
        flight = flights_data[flight_id]

        for field in data:
            flight[field] = data[field]

        return flight
    
    def delete(self, flight_id):
        abort_if_flight_missing(flight_id)
        del flights_data[flight_id]

        return '', 204



class FlightUSD(Resource):
    def get(self, flight_id):
        abort_if_flight_missing(flight_id)

        resp = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur.json')
        currency_rates = resp.json()
        eur_usd = currency_rates['eur']['usd']

        flight = flights_data[flight_id]

        flight_usd = copy(flight)

        flight_usd['base_ticket_prices'] = flight_usd['base_ticket_prices'] * eur_usd
           

        return flight_usd
    


api.add_resource(FlightsList, '/flights/')
api.add_resource(FlightUSD, '/flights/usd/<int:flight_id>')
api.add_resource(Flight, '/flights/<int:flight_id>')


if __name__ == '__main__':
    app.run(debug=True)