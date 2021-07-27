from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.location import LocationModel


class Location(Resource):
	parser = reqparse.RequestParser() #NEW
	parser.add_argument('building',
		type=str,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('room',
		type=str,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('start_date',
		type=int,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('dispenser_id',
		type=int,
		required=True,
		help="Every location needs a dispenser id!!"
	)

	@jwt_required()
	def get(self, name):
		location = LocationModel.find_by_name(name)
		if location:
			return location.json()
		return {'message': 'Location not found'}, 404

	def post(self, name):
		# if DispenserModel.find_by_name(name):
		# 	return {'message': "A dispenser with name '{}' already exiists".format(name)}, 400
		# data = Dispenser.parser.parse_args()
		data = Location.parser.parse_args()
	
		location = LocationModel(name, data['building'], data['room'], data['start_date'], data['dispenser_id'])
		#exception is what python runs when an error occurs 
		try:
			location.save_to_db()
		except:
			return {"message": "an error occured inserting the data"}, 500 #internal server erro, somethinf went wrong that not the users fault.

		return location.json(), 201

	def delete(self, name):
		location = LocationModel.find_by_name(name)
		if location:
			location.delete_from_db()

		return {'message': 'Location deleted'}

	def put(self, name):
		data = Location.parser.parse_args()

		location = LocationModel.find_by_name(name)		
		if location is None:
			location = LocationModel(name, data['building'], data['room'], data['start_date'], data['dispenser_id'])

		else:
			location.building = data['building']
			location.room = data['room']
			location.start_date = data['start_date']
			location.dispenser_id = data['dispenser_id']

		location.save_to_db()
		return location.json()
	
	
class LocationList(Resource):
	def get(self):
		return {'locations': [location.json() for location in LocationModel.query.all()]}