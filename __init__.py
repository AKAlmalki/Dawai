from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_migrate import Migrate
import os
from flask_moment import Moment
from .models import *

#---------------------------------------------------------------#
# App Constant Variables
#---------------------------------------------------------------#

SECRET_KEY = "Dawai-2000"

#---------------------------------------------------------------#
# App Configuration
#---------------------------------------------------------------#

# initialize app instance
app = Flask(__name__, template_folder='./templates')
moment = Moment(app)

# Config App and Secrets
app.config.from_pyfile('config.py')
app.secret_key = SECRET_KEY

# to initiate the db imported from models file
db.init_app(app)

# Flask-Migrate 
migrate = Migrate(app, db)

# the toolbar is only enabled in debug mode:
app.debug = True

#---------------------------------------------------------------#
# Controllers
#---------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/index.html')

# ------- Medication ------------

@app.route('/medications')
def get_all_medications():

    # get all medications in the database
    medications = Medication.query.order_by(Medication.id).all()

    # format the medications to return it as list of medications objects
    formatted_medications = [medication.format() for medication in medications]

    # total number of medication
    total_medications = len(Medication.query.all())
    
    return render_template('pages/index.html', medications=formatted_medications, total_med=total_medications)

@app.route('/medications/<int:med_id>')
def get_medication(med_id):

    # get all medications in the database
    medication = Medication.query.filter_by(id=med_id).one_or_none()

    # format the medications to return it as list of medications objects
    formatted_medication = medication.format()

    med_resources = db.session.query(Resource).join(MedRes).filter(MedRes.medication_id==med_id).all()

    med_res = []

    for med_resource in med_resources:
        med_res.extend([{
            "name": med_resource.name,
            "website_link": med_resource.website_link
        }])

    # med_res = MedRes.query.filter(MedRes.medication_id==med_id).all()

    return render_template('pages/med_info.html', medication=formatted_medication, med_resources=med_res)

@app.route('/medications/new', methods=['POST'])
def new_medication():

    # get the request and format it into a dictionary (JSON format)
    body = request.get_json()

    # grab the values of 'body' dictionary by the key
    name = body.get("name", None)
    commercial_names = body.get("commercial_names", None)
    concentration_APD = body.get("concentration_APD", None)
    concentration_TOB = body.get("concentration_TOB", None)
    emergency_case = body.get("emergency_case", None)
    side_effect = body.get("side_effect", None)
    side_effect_MP = body.get("side_effect_MP", None)
    a_ping = body.get("a_ping", None)
    dosage_form = body.get("dosage_form", None)
    indications = body.get("indications", None)
    image_url = body.get("image_url", None)
    treat_for = body.get("treat_for", None)
    status = body.get("status", None)

    # creating a new instance of Medication object and initializing it with all the parameters
    medication = Medication(name, commercial_names, concentration_APD, concentration_TOB, emergency_case, side_effect, side_effect_MP, a_ping, dosage_form, indications, image_url, treat_for, status)

    # inserting the instance into the database AND committing the changes
    medication.insert()

    return jsonify(
        {
            "success": True,
            "medication_formatted": medication.format(),
            "total_medications": len(Medication.query.all())
        }
    )


@app.route('/medications/<int:med_id>', methods=['DELETE'])
def remove_medication(med_id):

    # get the medications instance with the specified id
    medication = Medication.query.filter(Medication.id == med_id).one_or_none()

    if medication is None:
        abort(404)

    # remove the medication from DB
    medication.delete()

    # format the medication information
    formatted_medication = medication.format()

    return jsonify(
        {
            "success": True,
            "deleted_medication": formatted_medication,
            "total_medications": len(Medication.query.all())
        }
    )

# ------- User ------------

@app.route('/users')
def get_all_users():

    # get all users in the database
    users = User.query.order_by(User.id).all()

    # format the users to return it as list of users objects
    formatted_users = [user.format() for user in users]

    return jsonify(
        {
            "success": True,
            "users": formatted_users,
            "total_users": len(User.query.all())
        }
    )

@app.route('/users/new', methods=['POST'])
def new_user():

    # get the request and format it into a dictionary (JSON format)
    body = request.get_json()

    # grab the values of 'body' dictionary by the key
    name = body.get("name", None)
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    email = body.get("email", None)
    role = body.get("role", None)
    phone_number = body.get("phone_number", None)
    genres = body.get("genres", None)
    address = body.get("address", None)
    profile_picture = body.get("profile_picture", None)
    date_of_birth = body.get("date_of_birth", None)
    status = body.get("status", None)

    # creating a new instance of User object and initializing it with all the parameters
    user = User(name, user_name, password, email, role, phone_number, genres, address, profile_picture, date_of_birth, status)

    # inserting the instance into the database AND committing the changes
    user.insert()

    return jsonify(
        {
            "success": True,
            "formatted_user": user.format(),
            "total_users": len(User.query.all())
        }
    )


@app.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):

    # get the users instance with the specified id
    user = User.query.filter(User.id == user_id).one_or_none()

    if user is None:
        abort(404)

    # remove the user from DB
    user.delete()

    # format the user information
    formatted_user = user.format()

    return jsonify(
        {
            "success": True,
            "deleted_user": formatted_user,
            "total_users": len(User.query.all())
        }
    )

# ------- Resource ------------

@app.route('/resources')
def get_all_resources():

    # get all resources in the database
    resources = Resource.query.order_by(Resource.id).all()

    # format the resources to return it as list of resources objects
    formatted_resources = [resource.format() for resource in resources]

    return jsonify(
        {
            "success": True,
            "resources": formatted_resources,
            "total_resources": len(Resource.query.all())
        }
    )

@app.route('/resources/new', methods=['POST'])
def new_resource():

    # get the request and format it into a dictionary (JSON format)
    body = request.get_json()

    # grab the values of 'body' dictionary by the key
    name = body.get("name", None)
    website_link = body.get("website_link", None)
    additional_info = body.get("additional_info", None)
    status = body.get("status", None)

    # creating a new instance of Resource object and initializing it with all the parameters
    resource = Resource(name, website_link, additional_info, status)

    # inserting the instance into the database AND committing the changes
    resource.insert()

    return jsonify(
        {
            "success": True,
            "formatted_resource": resource.format(),
            "total_resources": len(Resource.query.all())
        }
    )


@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def remove_resource(resource_id):

    # get the users instance with the specified id
    resource = Resource.query.filter(Resource.id == resource_id).one_or_none()

    if resource is None:
        abort(404)

    # remove the resource from DB
    resource.delete()

    # format the resource information
    formatted_resource = resource.format()

    return jsonify(
        {
            "success": True,
            "deleted_resource": formatted_resource,
            "total_resources": len(Resource.query.all())
        }
    )

# ------- Video ------------

@app.route('/videos')
def get_all_videos():

    # get all videos in the database
    videos = Video.query.order_by(Video.id).all()

    # format the videos to return it as list of videos objects
    formatted_videos = [video.format() for video in videos]

    return jsonify(
        {
            "success": True,
            "videos": formatted_videos,
            "total_videos": len(Video.query.all())
        }
    )

@app.route('/videos/new', methods=['POST'])
def new_video():

    # get the request and format it into a dictionary (JSON format)
    body = request.get_json()

    # grab the values of 'body' dictionary by the key
    title = body.get("title", None)
    classification = body.get("classification", None)
    creation_date = body.get("creation_date", None)
    last_modification_date = body.get("last_modification_date", None)
    url = body.get("url", None)
    status = body.get("status", None)

    # creating a new instance of Video object and initializing it with all the parameters
    video = Video(title, classification, creation_date, last_modification_date, url, status)

    # inserting the instance into the database AND committing the changes
    video.insert()

    return jsonify(
        {
            "success": True,
            "formatted_video": video.format(),
            "total_videos": len(Video.query.all())
        }
    )


@app.route('/videos/<int:video_id>', methods=['DELETE'])
def remove_video(video_id):

    # get the videos instance with the specified id
    video = Video.query.filter(Video.id == video_id).one_or_none()

    if video is None:
        abort(404)

    # remove the video from DB
    video.delete()

    # format the video information
    formatted_video = video.format()

    return jsonify(
        {
            "success": True,
            "deleted_video": formatted_video,
            "total_videos": len(Video.query.all())
        }
    )

# ------- MedLog ------------

@app.route('/medlogs')
def get_all_medlogs():

    # get all medlogs in the database
    medlogs = MedLog.query.order_by(MedLog.user_id).all()

    # format the medlogs to return it as list of medlogs objects
    formatted_medlogs = [medlog.format() for medlog in medlogs]

    return jsonify(
        {
            "success": True,
            "medlogs": formatted_medlogs,
            "total_medlogs": len(MedLog.query.all())
        }
    )

@app.route('/medlogs/new', methods=['POST'])
def new_medlog():

    # get the request and format it into a dictionary (JSON format)
    body = request.get_json()

    # grab the values of 'body' dictionary by the key
    user_id = body.get("user_id", None)
    medication_id = body.get("medication_id", None)
    creation_date = body.get("creation_date", None)
    last_modification_date = body.get("last_modification_date", None)

    # creating a new instance of MedLog object and initializing it with all the parameters
    medlog = MedLog(user_id, medication_id, creation_date, last_modification_date)

    # inserting the instance into the database AND committing the changes
    medlog.insert()

    return jsonify(
        {
            "success": True,
            "formatted_medlog": medlog.format(),
            "total_medlogs": len(MedLog.query.all())
        }
    )


@app.route('/medlogs/<int:user_id>', methods=['DELETE'])
def remove_medlog(user_id):

    # get the medlogs instance with the specified id
    medlog = MedLog.query.filter(MedLog.user_id == user_id).one_or_none()

    if medlog is None:
        abort(404)

    # remove the medlog from DB
    medlog.delete()

    # format the medlog information
    formatted_medlog = medlog.format()

    return jsonify(
        {
            "success": True,
            "deleted_medlog": formatted_medlog,
            "total_medlogs": len(MedLog.query.all())
        }
    )

# ------- MedRes ------------

@app.route('/medresources')
def get_all_medresources():

    # get all medresources in the database
    medresources = MedRes.query.order_by(MedRes.resource_id).all()

    # format the medresources to return it as list of medresources objects
    formatted_medresources = [medresource.format() for medresource in medresources]

    return jsonify(
        {
            "success": True,
            "medresources": formatted_medresources,
            "total_medresources": len(MedRes.query.all())
        }
    )

@app.route('/medresources/new', methods=['POST'])
def new_medresource():

    # get the request and format it into a dictionary (JSON format)
    body = request.get_json()

    # grab the values of 'body' dictionary by the key
    resource_id = body.get("resource_id", None)
    medication_id = body.get("medication_id", None)
    date = body.get("date", None)

    # creating a new instance of MedRes object and initializing it with all the parameters
    medresource = MedRes(resource_id, medication_id, date)

    # inserting the instance into the database AND committing the changes
    medresource.insert()

    return jsonify(
        {
            "success": True,
            "formatted_medresource": medresource.format(),
            "total_medresources": len(MedRes.query.all())
        }
    )


@app.route('/medresources/<int:resource_id>', methods=['DELETE'])
def remove_medresource(resource_id):

    # get the medresource instance with the specified id
    medresource = MedRes.query.filter(MedRes.resource_id == resource_id).one_or_none()

    if medresource is None:
        abort(404)

    # remove the medresource from DB
    medresource.delete()

    # format the medresource information
    formatted_medresource = medresource.format()

    return jsonify(
        {
            "success": True,
            "deleted_medresource": formatted_medresource,
            "total_medresources": len(MedRes.query.all())
        }
    )

# ------- MedVid ------------

@app.route('/medvideos')
def get_all_medvideos():

    # get all medvideos in the database
    medvideos = MedVid.query.order_by(MedVid.video_id).all()

    # format the medvideos to return it as list of medvideos objects
    formatted_medvideos = [medvideo.format() for medvideo in medvideos]

    return jsonify(
        {
            "success": True,
            "medvideos": formatted_medvideos,
            "total_medvideos": len(MedVid.query.all())
        }
    )

@app.route('/medvideos/new', methods=['POST'])
def new_medvideos():

    # get the request and format it into a dictionary (JSON format)
    body = request.get_json()

    # grab the values of 'body' dictionary by the key
    video_id = body.get("video_id", None)
    medication_id = body.get("medication_id", None)
    date = body.get("date", None)

    # creating a new instance of MedVid object and initializing it with all the parameters
    medvideo = MedVid(video_id, medication_id, date)

    # inserting the instance into the database AND committing the changes
    medvideo.insert()

    return jsonify(
        {
            "success": True,
            "formatted_medvideo": medvideo.format(),
            "total_medvideos": len(MedVid.query.all())
        }
    )


@app.route('/medvideos/<int:video_id>', methods=['DELETE'])
def remove_medvideos(video_id):

    # get the medvideos instance with the specified id
    medvideo = MedVid.query.filter(MedVid.video_id == video_id).one_or_none()

    if medvideo is None:
        abort(404)

    # remove the medvideos from DB
    medvideo.delete()

    # format the medvideos information
    formatted_medvideo = medvideo.format()

    return jsonify(
        {
            "success": True,
            "deleted_medvideo": formatted_medvideo,
            "total_medvideos": len(MedVid.query.all())
        }
    )

#---------------------------------------------------------------#
# Error Handlers
#---------------------------------------------------------------#

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

#---------------------------------------------------------------#
# Launch.
#---------------------------------------------------------------#

# specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
