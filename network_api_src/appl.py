from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db 

from security import authenticate, identity
from resources.user import UserRegister
from resources.dispenser import Dispenser, DispenserList
from resources.location import Location, LocationList
from resources.status import Status, StatusList
from resources.detection import Detection, DetectionList
from models.location import LocationModel
from models.status import StatusModel
from models.detection import DetectionModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLAlLCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'group18'
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Location, '/location/<string:name>', '/location/<int:id>')
api.add_resource(Status, '/status/<string:name>')
api.add_resource(Detection, '/detection/<string:name>')
api.add_resource(Dispenser, '/dispenser/<string:name>', '/dispenser/<int:id>')
api.add_resource(DispenserList, '/dispensers')
api.add_resource(LocationList, '/locations')
api.add_resource(StatusList, '/statuses')
api.add_resource(DetectionList, '/detections')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
	db.init_app(app)
	app.run(port=5000, debug=True)