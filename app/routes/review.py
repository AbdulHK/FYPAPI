import os,simplejson,json
from app import app, db,auth
from flask import jsonify, request, abort , g , Flask
from flask import send_from_directory
from flask import url_for
from model.review import Review
from model.user import User
from werkzeug.utils import secure_filename


@app.route('/api/review/add/',methods=['POST'])
@auth.login_required
def add_review():
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    rate = request.args['rate']
    id=g.user.username
    res=request.args['rest']
    desc = request.args['desc']
    title = request.args['title']
    #review there already
    if Review.query.filter_by(username=id,rest_id=res,deleted=0).first() is not None:
        abort(400)
    if 'file' in request.files:
        f = request.files['file']
        if f.filename == '':
            return jsonify({"file": "no name"})
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            fname=id+ res+ filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            url= url_for('upload_file', filename=fname)
    review = Review(username=id,rest_id=res,discription=desc,overall_rate=rate,title=title,image_filename=fname,image_url=url)
    db.session.add(review)
    db.session.commit()
    return jsonify({'data': 'Done! Review Added'})

@app.route('/api/review/get/',methods=['GET'])
def get_review():
    id = request.args['rest']
    review = Review.query.filter_by(rest_id=id,deleted=0)
    return jsonify(reviews=[i.serialize for i in review])

@app.route('/api/review/get/limit/',methods=['GET'])
def get_review_limit():
    id = request.args['rest']
    review = Review.query.filter_by(rest_id=id,deleted=0).limit(0)
    return jsonify(reviews=[i.serialize for i in review])


@app.route('/api/review/update/',methods=['PUT'])
@auth.login_required
def update_review():
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    id = g.user.username
    res=request.args['rest']
    review = Review.query.filter_by(username=id, rest_id=res,deleted=0).first()
    try:
        if 'desc' in request.args:
            review.discription = request.args['desc']
        if 'rate' in request.args:
            review.overall_rate= request.args['rate']
        if 'title' in request.args:
            review.title = request.args['title']
        if 'file' in request.files:
            f = request.files['file']
            if f.filename == '':
                return jsonify({"file": "no name"})
            print("no name")
            if f and allowed_file(f.filename):
                print("i am here, final stage")
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], id+ res+filename))
                review.image_filename = id+ res+filename
                review.image_url = url_for('upload_file', filename=id +res+filename)
        db.session.commit()
    except:
        print("Error")
        db.session.rollback()
        db.session.flush()
    return jsonify({'reviews':review.serialize})

@app.route('/api/review/delete/',methods=['PUT'])
@auth.login_required
def del_review():
    id= request.args['id']
    review = Review.query.filter_by(id=id,deleted=0)
    try:
        review.deleted = 1

        db.session.commit()
    except:
        print("Error")
        db.session.rollback()
        db.session.flush()
    return jsonify({'data': 'Review deleted'})

@app.route('/api/review/get/user/',methods=['GET'])
@auth.login_required
def get_user_review():
    username = g.user.username
    res = request.args['rest']
    review = Review.query.filter_by(username=username,rest_id=res,deleted=0).first()
    if review is None:
        return jsonify({"Test":"PleaseWork"})
    else:
        return jsonify({'reviews': review.serialize})


@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)