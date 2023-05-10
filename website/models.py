from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

## sqlalchemy migrate_engine
## https://stackoverflow.com/questions/14032066/cant-import-sqlalchemy-migrate-engine

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    public_key = db.Column(db.String(500))
    private_key = db.Column(db.String(500))
    subscription_status = db.Column(db.String(500))

class Virus(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    virus_type = db.Column(db.String(150))
    name = db.Column(db.String(500))
    heartbeat_rate = db.Column(db.String(500))
    subscription_status = db.Column(db.String(500))
    user_id = db.Column(db.Integer(150))

class Hosts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pc_name = db.Column(db.String(150), unique=True)
    country = db.Column(db.String(150))
    host_notes = db.Column(db.String(500))
    settings = db.Column(db.String(500))
    last_heartbeat = db.Column(db.String(500))
    user_id = db.Column(db.Integer(150))
    virus_id = db.Column(db.Integer(150))

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image_name = db.Column(db.String(150))
#     imageset_id = db.Column(db.String(150))


# class ImageSet(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String(150))

# class RenderedModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     model_name = db.Column(db.String(150))
#     user_id = db.Column(db.String(150))
#     imageset_id = db.Column(db.String(150))
#     job_id = db.Column(db.String(150))

# class Job(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String(150))
#     user_id = db.Column(db.String(150))
#     imageset_id = db.Column(db.String(150))
   

  
    #notes = db.relationship('Note')
    


