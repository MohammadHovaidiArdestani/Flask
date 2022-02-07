from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
import random
import requests
from copy import copy
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import flasgger


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
Swagger(app)


class FlightModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False) 
    departing_time = db.Column(db.String(20), nullable=False)   
    arrival_time = db.Column(db.String(20), nullable=False)  
    departing_airport = db.Column(db.String(20), nullable=False) 
    base_ticket_prices = db.Column(db.Float, nullable=False)
    arrival_airport = db.Column(db.String(20), nullable=False) 
    number_passengers = db.Column(db.Integer, nullable=False)   


db.create_all()


flight_model_field = {
    'id': fields.Integer,
    'number': fields.String,
    'origin': fields.String,
    'destination': fields.String,
    'departing_time': fields.String,
    'arrival_time': fields.String,
    'departing_airport': fields.String,
    'arrival_airport': fields.String,
    'base_ticket_prices': fields.Float,
    'number_passengers': fields.Integer,
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

flight_req_patch = reqparse.RequestParser()
flight_req_patch.add_argument('number', type=str)
flight_req_patch.add_argument('number_passengers', type=int)
flight_req_patch.add_argument('origin', type=str)
flight_req_patch.add_argument('destination', type=str)
flight_req_patch.add_argument('departing_time', type=str)
flight_req_patch.add_argument('arrival_time', type=str)
flight_req_patch.add_argument('departing_airport', type=str)
flight_req_patch.add_argument('arrival_airport', type=str)
flight_req_patch.add_argument('base_ticket_prices', type=float)


def abort_if_flight_missing(flight_id):
    flight  = FlightModel.query.get(flight_id)

    if not flight:
        abort(404, message='No flight found with this id')


class FlightsList(Resource):

    @marshal_with(flight_model_field)
    def get(self):
        """
        returns all flights
        ---
        responses:
            200:
                description : list of flights
        """
        result = FlightModel.query.all()

        return result
    
    @marshal_with(flight_model_field)
    def post(self):
        new_flight_data = flight_req.parse_args()

        new_flight = FlightModel(
            number = new_flight_data['number'],
            origin = new_flight_data['origin'],
            destination = new_flight_data['destination'],
            departing_time = new_flight_data['departing_time'],
            arrival_time = new_flight_data['arrival_time'],
            departing_airport = new_flight_data['departing_airport'],
            arrival_airport = new_flight_data['arrival_airport'],
            base_ticket_prices = new_flight_data['base_ticket_prices'],
            number_passengers = new_flight_data['number_passengers']
        )

        db.session.add(new_flight)
        db.session.commit()

        return new_flight, 201
        
    

class Flight(Resource):
    @marshal_with(flight_model_field)
    def get(self, flight_id):
        """returns a flight
        ---
        parameters:
            - name: flight_id
              in: path
              type: integer
              required: true
        responses:
            200:
                description: Get data related to one particular flight
        """
        abort_if_flight_missing(flight_id)
        flight = FlightModel.query.get(flight_id)

        return flight
    
    @marshal_with(flight_model_field)
    def put(self, flight_id):
        abort_if_flight_missing(flight_id)

        data = flight_req.parse_args()

        flight = FlightModel.query.get(flight_id)
        
        flight.number = data['number']
        flight.origin = data['origin']
        flight.destination = data['destination']
        flight.departing_time = data['departing_time']
        flight.arrival_time = data['arrival_time']
        flight.departing_airport = data['departing_airport']
        flight.arrival_airport = data['arrival_airport']
        flight.base_ticket_prices = data['base_ticket_prices']
        flight.number_passengers = data['number_passengers']

        db.session.commit()

        return flight
    
    @marshal_with(flight_model_field)
    def patch(self, flight_id):
        abort_if_flight_missing(flight_id)
        
        data = flight_req_patch.parse_args()

        flight = FlightModel.query.get(flight_id)
        
        if data['number']:
            flight.number = data['number']
        
        if data['origin']:
            flight.origin = data['origin']
        
        if data['destination']:
            flight.destination = data['destination']
        
        if data['departing_time']:
            flight.departing_time = data['departing_time']

        if data['arrival_time']:
            flight.arrival_time = data['arrival_time']

        if data['departing_airport']:
            flight.departing_airport = data['departing_airport']

        if data['base_ticket_prices']:
            flight.base_ticket_prices = data['base_ticket_prices']

        if data['arrival_airport']:
            flight.arrival_airport = data['arrival_airport']

        if data['number_passengers']:
            flight.number_passengers = data['number_passengers']


        db.session.commit()

        return flight
    
    def delete(self, flight_id):
        abort_if_flight_missing(flight_id)

        flight = FlightModel.query.get(flight_id)

        db.session.delete(flight)
        db.session.commit()

        return '', 204


def predict_late_flight(flight): # 98% of flights do not get late

    if flight.destination == 'Ukraine': # 100% of flights will be late
        return True

    prediction = random.choice([True, False])

    return prediction

class FlightPredictor(Resource):
    def get(self, flight_id):
        abort_if_flight_missing(flight_id)
        flight = FlightModel.query.get(flight_id)

        prediction = predict_late_flight(flight)

        return {'prediction': prediction}


class FlightUSD(Resource):
    @marshal_with(flight_model_field)
    def get(self, flight_id):
        abort_if_flight_missing(flight_id)

        resp = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur.json')
        currency_rates = resp.json()
        eur_usd = currency_rates['eur']['usd']

        flight = FlightModel.query.get(flight_id)

        flight_usd = copy(flight)

        flight_usd.base_ticket_prices = flight_usd.base_ticket_prices * eur_usd

        return flight_usd
    


api.add_resource(FlightsList, '/flights/')
api.add_resource(FlightUSD, '/flights/usd/<int:flight_id>')
api.add_resource(Flight, '/flights/<int:flight_id>')
api.add_resource(FlightPredictor, '/flights/late_flight/<int:flight_id>')


if __name__ == '__main__':
    app.run(debug=True)