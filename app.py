from flask import Flask
from api.models import db
from api.routes import api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Pablo180518@localhost:5432/agile_monkeys"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
db.init_app(app)

#Adding all endpoints from /api
app.register_blueprint(api)



if (__name__) == "__main__":
    app.run(debug=True)