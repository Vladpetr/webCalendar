from flask import Flask, abort, request
import sys
from flask_restful import Api, Resource
from flask_restful import reqparse, inputs, fields, marshal_with
from datetime import date
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.secret_key = "super secret"
db = SQLAlchemy(app)


class Event(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()

api = Api(app)
parser = reqparse.RequestParser()


parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}


class EventTodayResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Event.query.filter(Event.date == date.today()).all()


class EventResource(Resource):
    def post(self):
        args = parser.parse_args()
        event = args['event']
        date = args['date'].date()

        new_event = Event(event=event, date=date)
        db.session.add(new_event)
        db.session.commit()

        ans = {
            "message": "The event has been added!",
            "event": event,
            "date": date.strftime('%Y-%m-%d')
        }
        return ans

    @marshal_with(resource_fields)
    def get(self):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        if start_time and end_time:
            events = Event.query.filter(Event.date >= start_time). \
                filter(Event.date <= end_time).all()
            if len(events) < 1:
                abort(404, {"message": "The event doesn't exist!"})
            return events
        return Event.query.all()


class EventByID(Resource):

    @marshal_with(resource_fields)
    def get(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    def delete(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {
            "message": "The event has been deleted!"
        }


api.add_resource(EventTodayResource, '/event/today')
api.add_resource(EventResource, '/event')
api.add_resource(EventByID, '/event/<int:event_id>')


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
