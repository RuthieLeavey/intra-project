from db import db

class StatusModel(db.Model):
	__tablename__ = 'statuses'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	curr_status = db.Column(db.String)
	date = db.Column(db.String())
	time = db.Column(db.String())


	dispenser_id = db.Column(db.Integer, db.ForeignKey('dispensers.id'))
	dispensser = db.relationship('DispenserModel')

	def __init__(self, name, curr_status, date, time, dispenser_id):
		self.name = name
		self.curr_status = curr_status
		self.date = date
		self.time = time
		self.dispenser_id = dispenser_id				

	# def json(self):
	# 	return {'name': self.name, 'price': self.price}
	def json(self):
		return {'status id': self.name, 'curr_status': self.curr_status, 'date': self.date, 'time': self.time, 'dispenser_id': self.dispenser_id}

	# @classmethod
	# def find_by_name(cls, name):
	# 	return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name
	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()
	@classmethod
	def find_by_location_id(cls, dispenser_id):
		return cls.query.filter_by(dispenser_id=dispenser_id).first() #SELECT * FROM items WHERE name=name

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()