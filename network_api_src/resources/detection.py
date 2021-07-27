from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.detection import DetectionModel

class Detection(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('used',
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
		detection = DetectionModel.find_by_name(name)
		if detection:
			return detection.json()
		return {'message': 'Status not found'}, 404

	def post(self, name):
		# if DispenserModel.find_by_name(name):
		# 	return {'message': "A dispenser with name '{}' already exiists".format(name)}, 400
		data = Detection.parser.parse_args()
	
		detection = DetectionModel(name, data['used'], data['date'], data['time'], data['dispenser_id'])
		#exception is what python runs when an error occurs 
		try:
			detection.save_to_db()
		except:
			return {"message": "an error occured inserting the data"}, 500 #internal server erro, somethinf went wrong that not the users fault.

		return detection.json(), 201

	def delete(self, name):
		detection = DetectionModel.find_by_name(name)
		if detection:
			detection.delete_from_db()

		return {'message': 'Detection deleted'}

	def put(self, name):
		data = Detection.parser.parse_args()

		detection = DetectionModel.find_by_name(name)		
		if detection is None:
			detection = DetectionModel(name, data['used'], data['date'], data['time'], data['dispenser_id'])

		else:
			detection.used = data['used']
			detection.date = data['date']
			detection.time = data['time']
			detection.dispenser_id = data['dispenser_id']

		detection.save_to_db()
		return detection.json()
	
class DetectionList(Resource):
	def get(self):
		return {'detections': [detection.json() for detection in DetectionModel.query.all()]}