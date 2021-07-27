from db import db

class LocationModel(db.Model):
	__tablename__ = 'locations'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	building = db.Column(db.String(80))
	room = db.Column(db.String(80))
	start_date = db.Column(db.Integer())

	dispenser_id = db.Column(db.Integer, db.ForeignKey('dispensers.id'))
	dispenser = db.relationship('DispenserModel')

	def __init__(self, name, building, room, start_date, dispenser_id):
		self.name = name
		self.building = building
		self.room = room
		self.start_date = start_date
		self.dispenser_id = dispenser_id

	def json(self):
		return return {'id': self.id, 'dispenser_name': self.name, 'building': self.building, 'room': self.room, 'start_date': self.start_date, 'dispenser_id': self.dispenser_id}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()