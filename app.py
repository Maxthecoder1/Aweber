from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

# Initializing our database

# creating an instance of the flask app
app = Flask(__name__)

# Configure our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Widget(db.Model):
    __tablename__ = 'widgets'  # creating a table name
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)  # this is the primary key
    name = db.Column('name', db.String(64), nullable=False)# nullable is false so the column can't be empty
    number_of_parts = db.Column('number_of_parts', db.Integer, )
    created_date = db.Column('created_date', db.DateTime, default=datetime.datetime.utcnow())
    updated_date = db.Column('updated_date', db.DateTime, default=datetime.datetime.utcnow())

    def json(self):
        return {'id': self.id, 'name': self.name,
                'number_of_parts': self.number_of_parts, 'created_date': self.created_date,
                'updated_date': self.updated_date}

    def add_widget(name, number_of_parts):
        '''function to add widget to database using id, name,
        number_of_parts, created_date, and updated_date as parameters'''
        new_widget = Widget(name=name, number_of_parts=number_of_parts)
        db.session.add(new_widget)  # add new widget to database session
        db.session.commit()

    def get_all_widgets():
        '''function to get all widgets in our database'''
        return [Widget.json(widget) for widget in Widget.query.all()]

    def get_widget(id):
        '''function to get widget using the id of the widget as parameter'''
        return [Widget.json(Widget.query.filter_by(id=id).first())]


    def update_widget(id, name, number_of_parts):
        '''function to update the details of a widget using the id, name,
        number_of_parts, created_date, and updated_date as parameters'''
        widget_to_update = Widget.query.filter_by(id=id).first()
        widget_to_update.name = name
        widget_to_update.number_of_parts = number_of_parts
        widget_to_update.updated_date = datetime.datetime.utcnow()
        db.session.commit()

    def delete_widget(id):
        '''function to delete a widget from our database using
           the id of the widget as a parameter'''
        Widget.query.filter_by(id=id).delete()
        db.session.commit()


# route to get widget by id
@app.route('/widgets/<int:id>', methods=['GET'])
def get_widget_by_id(id):
    return_value = Widget.get_widget(id)
    return jsonify(return_value)

# route to list widgets
@app.route('/widgets', methods=['GET'])
def list_widgets():
    return jsonify({'Widgets': Widget.get_all_widgets()})

# route to create widget
@app.route('/widgets', methods=['POST'])
def create_widget():
    request_data = request.get_json()
    Widget.add_widget(request_data['name'], request_data['number_of_parts'])
    response = Response("Widget Created", status=201, mimetype='application/json')
    return response

# route to update widget by id
@app.route('/widgets/<int:id>', methods=['PUT'])
def update_widget(id):
    request_data = request.get_json()
    Widget.update_widget(id, request_data['name'], request_data['number_of_parts'])
    response = Response("Widget Updated", status=200, mimetype='application/json')
    return response

# route to delete widget by id
@app.route('/widgets/<int:id>', methods=['DELETE'])
def delete_widget(id):
    Widget.delete_widget(id)
    response = Response("Widget Deleted", status=200, mimetype='application/json')
    return response

if __name__ == "__main__":
    app.debug = True
    app.run(port=1234, debug=True)