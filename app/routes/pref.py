from ..model.userpref import UserPref
from app import app, db,auth
from flask import jsonify, request, abort , g , Flask


@app.route('/api/user/addpref/', methods=['POST'])
@auth.login_required
def add_pref():
    id= g.user.id
    pref1 = request.args['preferance1']
    pref2 = request.args['preferance2']
    pref3 = request.args['preferance3']
    preferance = UserPref(userid=id,pre1=pref1,pre2=pref2,pre3=pref3)
    db.session.add(preferance)
    db.session.commit()
    return jsonify({'Response': "Done"})

@app.route('/api/user/getpref/', methods=['GET'])
@auth.login_required
def get_pref():
    user_id= g.user.id
    pref = UserPref.query.filter_by(userid=user_id).first()
    return  (jsonify({"preferance":pref.serialize}))

@app.route('/api/user/updatepref/', methods=['PUT','POST'])
@auth.login_required
def update_pref():
    id= g.user.id
    pref=UserPref.query.filter_by(userid=id).first()
    try:
        if 'preferance1' in request.args:
            pref.pre1 = request.args['preferance1']
        if 'preferance2' in request.args:
            pref.pre2 = request.args['preferance2']
        if 'preferance3' in request.args:
            pref.pre3 = request.args['preferance3']

        db.session.commit()
    except:
        print("Error")
        db.session.rollback()
        db.session.flush()
    return  (jsonify({"preferance":pref.serialize}))


