from flask import Flask

from file.SQLalchemy import db

from file.Models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
app.app_context().push()
db.create_all()



@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/users', method='GET')
def get_user():
        users_list = []
        for user in User.query.all():
            users_list.append(user.get_dict())

if __name__ == '__main__':
    app.run()