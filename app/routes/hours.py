from app import app,db,auth
from flask import abort
from flask import jsonify, request
from ..model.hours import Hours


@app.route('/api/restaurant/time/all/',methods=['GET'])
def gettimes():
    res = request.args['rest']
    time = Hours.query.filter_by(restid=res)
    return jsonify(times=[i.serialize for i in time])


@app.route('/api/restaurant/time/',methods=['POST'])
@auth.login_required
def add_times():
    res = request.args['rest']


    if 'day0' in request.args:
        mon = request.args['day0']
        if 'MonTo' in request.args:
            monto = request.args['MonTo']
        else:
            monto = None
        if 'MonFrom' in request.args:
            monfrom = request.args['MonFrom']
        else:
            monfrom = None
    else:
        mon = None
    if 'day1' in request.args:
        tue = request.args['day1']
        if 'TueTo' in request.args:
            tueto = request.args['TueTo']
        else:
            tueto = None
        if 'TueFrom' in request.args:
            tuefrom = request.args['TueFrom']
        else:
            tuefrom = None
    else:
        tue=None
    if 'day2' in request.args:
        wed = request.args['day2']
        if 'WedTo' in request.args:
            wedto = request.args['WedTo']
        else:
            wedto = None
        if 'WedFrom' in request.args:
            wedfrom = request.args['WedFrom']
        else:
            wedfrom = None
    else:
        wed=None
    if 'day3' in request.args:
        thr = request.args['day3']
        if 'ThrTo' in request.args:
            thrto = request.args['ThrTo']
        else:
            thrto = None
        if 'ThrFrom' in request.args:
            thrfrom = request.args['ThrFrom']
        else:
            thrfrom = None
    else:
        thr=None
    if 'day4' in request.args:
        fri = request.args['day4']
        if 'FriTo' in request.args:
            frito = request.args['FriTo']
        else:
            frito = None
        if 'FroFrom' in request.args:
            frifrom = request.args['FriFrom']
        else:
            frifrom = None
    else:
        fri=None
    if 'day5' in request.args:
        sat = request.args['day5']
        if 'SatTo' in request.args:
            satto = request.args['SatTo']
        else:
            satto= None
        if 'SatFrom' in request.args:
            satfrom = request.args['SatFrom']
        else:
            satfrom = None
    else:
        sat=None
    if 'day6' in request.args:
        sun = request.args['day6']
        if 'SunTo' in request.args:
            sunto = request.args['SunTo']
        else:
            sunto = None
        if 'SunFrom' in request.args:
            sunfrom = request.args['SunFrom']
        else:
            sunfrom = None
    else:
        sun=None
    if mon is "0":
        time=Hours(restid=res,Day=mon,StartTime=monfrom,FinishTime=monto)
        db.session.add(time)

    if tue is "1":
        time=Hours(restid=res,Day=tue,StartTime=tuefrom,FinishTime=tueto)
        db.session.add(time)

    if wed is "2":
        time = Hours(restid=res, Day=wed, StartTime=wedfrom, FinishTime=wedto)
        db.session.add(time)

    if thr is "3":
        time=Hours(restid=res,Day=thr,StartTime=thrfrom,FinishTime=thrto)
        db.session.add(time)

    if fri is "4":
        time=Hours(restid=res,Day=fri,StartTime=frifrom,FinishTime=frito)
        db.session.add(time)

    if sat is "5":
        time=Hours(restid=res,Day=sat,StartTime=satfrom,FinishTime=satto)
        db.session.add(time)

    if sun is "6":
        time=Hours(restid=res,Day=sun,StartTime=sunfrom,FinishTime=sunto)
        db.session.add(time)
    db.session.commit()
    return jsonify({"Done": "stored"})
