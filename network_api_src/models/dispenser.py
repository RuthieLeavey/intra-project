from db import db

class DispenserModel(db.Model):
	__tablename__ = 'dispensers'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	location_id = db.Column(db.String())
	status_id = db.Column(db.String())
	usage_count = db.Column(db.Integer())
	detection_count = db.Column(db.Integer())
	detection_id = db.Column(db.String())

	locations = db.relationship('LocationModel', lazy='dynamic')
	statuses = db.relationship('StatusModel', lazy='dynamic')
	detections = db.relationship('DetectionModel', lazy='dynamic')

	def __init__(self, name, location_id, status_id, usage_count, detection_count, detection_id):
		self.name = name
		self.location_id = location_id
		self.status_id = status_id
		self.usage_count = usage_count
		self.detection_count = detection_count		
		self.detection_id = detection_id
		# self.location_id = location_id

	def json(self):
		return {'id': self.id, 'disp': self.name, 'locations': [location.json() for location in self.locations.all()], 'statuses': [status.json() for status in self.statuses.all()], 'usage_count': self.usage_count, 'detection_count': self.detection_count, 'detections': [detection.json() for detection in self.detections.all()]}
	
	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name
	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()