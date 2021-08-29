from flask import Flask
from api.models import db
from api.routes import api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pablo180518@localhost:5432/agile_monkeys"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


migrate = Migrate(app, db)
db.init_app(app)

#Adding JWT
app.config["JWT_SECRET_KEY"] = "agile_monkeys"
jwt = JWTManager(app)

#Adding all endpoints from /api
app.register_blueprint(api)



if (__name__) == "__main__":
    app.run(debug=True)