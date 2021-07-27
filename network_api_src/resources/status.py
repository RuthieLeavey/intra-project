from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.status import StatusModel

class Status(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('curr_status',
		type=str,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('date',
		type=str,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('time',
		type=str,
		required=True,
		help="This field can't be left blank!!"
	)
	parser.add_argument('dispenser_id',
		type=int,
		required=True,
		help="Every dispenser needs a location id!!"
	)

	@jwt_required()
	def get(self, name):
		status = StatusModel.find_by_name(name)
		if status:
			return status.json()
		return {'message': 'Status not found'}, 404

	def post(self, name):
		# if DispenserModel.find_by_name(name):
		# 	return {'message': "A dispenser with name '{}' already exiists".format(name)}, 400
		data = Status.parser.parse_args()
	
		status = StatusModel(name, data['curr_status'], data['date'], data['time'], data['dispenser_id'])
		#exception is what python runs when an error occurs 
		try:
			status.save_to_db()
		except:
			return {"message": "an error occured inserting the data"}, 500 #internal server erro, somethinf went wrong that not the users fault.

		return status.json(), 201

	def delete(self, name):
		status = StatusModel.find_by_name(name)
		if status:
			status.delete_from_db()

		return {'message': 'Status deleted'}

	def put(self, name):
		data = Status.parser.parse_args()

		status = StatusModel.find_by_name(name)		
		if status is None:
			status = StatusModel(name, data['curr_status'], data['date'], data['time'], data['dispenser_id'])

		else:
			status.curr_status = data['curr_status']
			status.date = data['date']
			status.time = data['time']
			status.dispenser_id = data['dispenser_id']

		status.save_to_db()
		return status.json()
	
class StatusList(Resource):
	def get(self):
		return {'statuses': [status.json() for status in StatusModel.query.all()]}