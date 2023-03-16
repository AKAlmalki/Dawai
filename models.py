from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, PrimaryKeyConstraint

# initialize 'db' variable as database instance
db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Medication(db.Model):
    __tablename__ =  'medication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    commercial_names = db.Column(db.String(255))
    concentration_APD = db.Column(db.Float)
    concentration_TOB = db.Column(db.Float)
    emergency_case = db.Column(db.String(2000))
    side_effect = db.Column(db.String(500))
    side_effect_MP = db.Column(db.String(255))
    a_ping = db.Column(db.String(255))
    dosage_form = db.Column(db.String(255))
    indications = db.Column(db.String(2000))
    image_url = db.Column(db.String(1000))
    treat_for = db.Column(db.String(500))
    status = db.Column(db.Integer, default=0)
    # backref 
    med_logs = db.relationship('MedLog', backref= db.backref('medication', lazy= True))
    med_videos = db.relationship('MedVid', backref= db.backref('medication', lazy= True))
    med_resources = db.relationship('MedRes', backref= db.backref('medication', lazy= True))
    

    def __repr__(self):
      return f'<Medication_id: {self.id}, name: {self.name}>'

    def __init__(self, name, commercial_names, concentration_APD, concentration_TOB, emergency_case, side_effect, side_effect_MP, a_ping, dosage_form, indications, image_url, treat_for, status):
        self.name = name
        self.commercial_names = commercial_names
        self.concentration_APD = concentration_APD
        self.concentration_TOB = concentration_TOB
        self.emergency_case = emergency_case
        self.side_effect = side_effect
        self.side_effect_MP = side_effect_MP
        self.a_ping = a_ping
        self.dosage_form = dosage_form
        self.indications = indications
        self.image_url = image_url
        self.treat_for = treat_for
        self.status = status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "commercial_names": self.commercial_names,
            "concentration_APD": self.concentration_APD,
            "concentration_TOB": self.concentration_TOB,
            "emergency_case": self.emergency_case,
            "side_effect": self.side_effect,
            "side_effect_MP": self.side_effect_MP,
            "a_ping": self.a_ping,
            "dosage_form" : self.dosage_form,
            "indications": self.indications,
            "image_url": self.image_url,
            "treat_for": self.treat_for,
            "status": self.status
        }


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    address = db.Column(db.String(120))
    profile_picture = db.Column(db.String(1000))
    date_of_birth = db.Column(db.String(120))
    status = db.Column(db.Integer, default=0)
    # backref
    user_logs = db.relationship('MedLog', backref= db.backref('user', lazy= True))

    def __repr__(self):
      return f'<User_id: {self.id}, name: {self.name}>'

    def __init__(self, name, user_name, password, email, role, phone_number, genres, address, profile_picture, date_of_birth, status):
        self.name = name
        self.user_name = user_name
        self.password = password
        self.email = email
        self.role = role
        self.phone_number = phone_number
        self.genres = genres
        self.address = address
        self.profile_picture = profile_picture
        self.date_of_birth = date_of_birth
        self.status = status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "password": self.password,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
            "genres": self.genres,
            "address": self.address,
            "profile_picture": self.profile_picture,
            "date_of_birth": self.date_of_birth,
            "status": self.status
        }

class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    website_link = db.Column(db.String(500))
    additional_info = db.Column(db.String(500))
    status = db.Column(db.Integer, default=0)
    # backref
    med_resources = db.relationship('MedRes', backref= db.backref('resource', lazy= True))

    def __repr__(self):
      return f'<Resource_id: {self.id}, name: {self.name}>'

    def __init__(self, name, website_link, additional_info, status):
        self.name = name
        self.website_link = website_link
        self.additional_info = additional_info
        self.status = status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "website_link": self.website_link,
            "additional_info": self.additional_info,
            "status": self.status
        }

class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    classification = db.Column(db.String(500))
    creation_date = db.Column(db.String(500))
    last_modification_date = db.Column(db.String(500))
    url = db.Column(db.String(2000))
    status = db.Column(db.Integer, default=0)
    # backref
    med_vids = db.relationship('MedVid', backref= db.backref('video', lazy= True))

    def __repr__(self):
      return f'<Video_id: {self.id}, title: {self.title}>'

    def __init__(self, title, classification, creation_date, last_modification_date, url, status):
        self.title = title
        self.classification = classification
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.url = url
        self.status = status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "classification": self.classification,
            "creation_date": self.creation_date,
            "last_modification_date": self.last_modification_date,
            "url": self.url,
            "status": self.status
        }

#=========================================================
# Many-to-many relationship Models
#=========================================================

class MedLog(db.Model):
    __tablename__ = 'MedLog'

    # NOTE: no need to declare an id for this table, these two keys (user_id and medication_id) would form a composite primary key -- this will ensure that the impossibility of duplicating this key in the database [same for MedRes and MedVid tables]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False, primary_key=True)
    creation_date = db.Column(db.String(120))
    last_modification_date = db.Column(db.String(120))

    def __repr__(self):
      return f'<MedLog: user_id: {self.name}, medication_id: {self.medication_id}, creation_date: {self.creation_date}, last_modification_date: {self.last_modification_date}>'

    def __init__(self, user_id, medication_id, creation_date, last_modification_date):
        self.user_id = user_id
        self.medication_id = medication_id
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "user_id": self.user_id,
            "medication_id": self.medication_id,
            "creation_date": self.creation_date,
            "last_modification_date": self.last_modification_date
        }


class MedRes(db.Model):
    __tablename__ = 'MedRes'

    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False, primary_key=True)
    date = db.Column(db.String(120))

    def __repr__(self):
      return f'<MedRes: resource_id: {self.resource_id}, medication_id: {self.medication_id}, date: {self.date}>'

    def __init__(self, resource_id, medication_id, date):
        self.resource_id = resource_id
        self.medication_id = medication_id
        self.date = date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "resource_id": self.resource_id,
            "medication_id": self.medication_id,
            "date": self.date
        }

class MedVid(db.Model):
    __tablename__ = 'MedVid'

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False, primary_key=True)
    date = db.Column(db.String(120))
    
    

    def __repr__(self):
      return f'<MedVid: video_id: {self.video_id}, medication_id: {self.medication_id}, date: {self.date}>'

    def __init__(self, video_id, medication_id, date):
        self.video_id = video_id
        self.medication_id = medication_id
        self.date = date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "video_id": self.video_id,
            "medication_id": self.medication_id,
            "date": self.date,
        }