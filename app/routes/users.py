import os,simplejson
from app import app, db,auth
from flask import flash,send_from_directory
from flask import jsonify, request, abort,g
from flask import url_for
from ..model.user import User
from werkzeug.utils import secure_filename, redirect
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/api/user/add/', methods=['POST'])
def new_user():
    username = request.args['uname']
    password = request.args['pass']
    address = request.args['address']
    firstname = request.args['firstname']
    lastname = request.args['lastname']
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username,deleted=0).first() is not None:
        abort(400)    # existing user
    user = User(username=username,address=address,firstname=firstname,lastname=lastname)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'user':{'username': user.username,'ID': user.id}}))

@app.route('/api/user/search/',methods=['GET'])
@auth.login_required
def get_user():
    id = g.user.id
    user= User.query.filter_by(id=id,deleted=0).first()
    return jsonify({'user':user.serialize})


@app.route('/api/user/update/', methods=['PUT'])
@auth.login_required
def update_user():
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

        # check if the post request has the file part
    user = User.query.filter_by(id=g.user.id,deleted=0).first()
    try:
        if 'uname' in request.args:
            user.username = request.args['uname']
        if 'password' in request.args:
            user.hash_password(request.args['password'])
        if 'lname' in request.args:
            user.lastname = request.args['lname']
        if 'fname' in request.args:
            user.firstname = request.args['fname']
        if 'address' in request.args:
            user.address = request.args['address']
        if 'preferance1' in request.args:
            user.pre1 = request.args['preferance1']
        if 'preferance2' in request.args:
            user.pre2 = request.args['preferance2']
        if 'preferance3' in request.args:
            user.pre3 = request.args['preferance3']
        if 'file' in request.files:
            f = request.files['file']
            if f.filename == '':
                return jsonify({"file" :"no name"})
                print("no name")

            if f and allowed_file(f.filename):
                print("i am here, final stage")

                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print("saving filename")
                user.image_filename = filename
                print (user.image_filename)
                user.image_url = url_for('uploaded_file', filename=filename)
                print (user.image_url)

        print("lets commit!")
        db.session.commit()
    except:
        print("Error")
        db.session.rollback()
        db.session.flush()
    return jsonify({'user':user.serialize})


@app.route('/api/user/token/')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(None)
    print (token)
    return jsonify({'Token':{'token': token.decode('ascii'),'duration': None,'UserID':g.user.id} })



@app.route('/api/deluser/',methods=['PUT'])
@auth.login_required
def del_user():
    id=g.user.id
    user= User.query.filter_by(id=id, deleted=0).first_or_404()
    user.deleted=1
    db.session.commit()
    return jsonify({'Response': "Good bye %s" % user.firstname})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)