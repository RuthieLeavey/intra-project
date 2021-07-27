from flask_restful import Resource, reqparse
from models.dispenser import DispenserModel


class Dispenser(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('location_id',
		type=int,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('status_id',
		type=int,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('usage_count',
		type=int,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('detection_count',
		type=int,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('detection_id',
		type=int,
		required=True,
		help="This field can't be left blank!!"
	)
	# parser.add_argument('location_id',
	# 	type=int,
	# 	required=True,
	# 	help="Every dispenser needs a location id!!"
	# )

	def get(self, name):
		dispenser = DispenserModel.find_by_name(name)
		if dispenser:
			return dispenser.json()
		return {"message": "Dispenser not found"}, 404

	def get(self, id):
		dispenser = DispenserModel.find_by_id(id)
		if dispenser:
			return dispenser.json()
		return {"message": "Dispenser not found"}, 404

	def post(self, name):
		if DispenserModel.find_by_name(name):
			return {"message": "A dispenser named '{}' already exists".format(name)}, 400

		data = Dispenser.parser.parse_args()
		
		dispenser = DispenserModel(name, data['location_id'], data['status_id'], data['usage_count'], data['detection_count'], data['detection_id'])
		try:
			dispenser.save_to_db()
		except:
			return {"message": 'An error occurred while creating the location.'}, 500

		return dispenser.json(), 201

	def delete(self, name):
		dispenser = DispenserModel.find_by_name(name)
		if dispenser:
			dispenser.delete_from_db()

		return {'message': 'Dispenser deleted'}

class DispenserList(Resource):
	def get(self):
		return {'dispensers': [dispenser.json() for dispenser in DispenserModel.query.all()]}