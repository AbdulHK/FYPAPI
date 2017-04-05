from app import app,db,auth
from flask import jsonify, request,send_from_directory,url_for
from model.restaurant import Restaurant
from geopy.geocoders import Nominatim
from werkzeug.utils import secure_filename
import os,ssl,simplejson
@app.route('/api/restaurants/search/',methods=['GET'])
def search():
    key = request.args['key']
    col = request.args['col']

    if col in Restaurant.__table__.c:
        if (col== 'cost'):
            keycast = int(key)
            cost1 = keycast - 10
            cost2 = keycast + 10
            restaurant = Restaurant.query.filter(Restaurant.cost.between(cost1, cost2)).all()
        elif (col == 'offer'):
            restaurant = Restaurant.query.filter(Restaurant.offer is not None)
        elif(col=='phone'):
            restaurant =Restaurant.query.filter(Restaurant.phone is not None)
        elif (col == 'offer'):
            restaurant = Restaurant.query.filter(Restaurant.offer is not None)
        elif (col == 'phone'):
            restaurant = Restaurant.query.filter(Restaurant.phone is not None)
        elif (col == 'has_reservation'):
            restaurant = Restaurant.query.filter(Restaurant.has_reservation != "0").all()
        elif (col == 'has_parking'):
            restaurant = Restaurant.query.filter(Restaurant.has_parking != "0").all()
        elif (col == 'has_wifi'):
            restaurant = Restaurant.query.filter(Restaurant.has_wifi != "0").all()
        elif (col == 'has_bar'):
            restaurant = Restaurant.query.filter(Restaurant.has_bar != "0").all()
        elif (col == 'has_terrace'):
            restaurant = Restaurant.query.filter(Restaurant.has_terrace != "0").all()
        elif (col == 'has_deliver'):
            restaurant = Restaurant.query.filter(Restaurant.has_delivery != "0").all()
        elif (col == 'has_cards'):
            restaurant = Restaurant.query.filter(Restaurant.has_cards != "0").all()
        else:
            restaurant = Restaurant.query.filter(getattr(Restaurant, col).like("%"+key+"%")).all()

    else:
        raise RuntimeError('Restaurant table doesn`t have column %s' % col)
    return jsonify(restaurants=[i.serialize for i in restaurant])

@app.route('/api/restaurants/search/limit/',methods=['GET'])
def testloc():
    key = request.args['key']
    col = request.args['col']
    if col in Restaurant.__table__.c:
        if (col == 'cost'):
            keycast = int(key)
            cost1 = keycast - 10
            cost2 = keycast + 10
            restaurant = Restaurant.query.filter(Restaurant.cost.between(cost1, cost2)).all()
        elif (col == 'offer'):
            restaurant = Restaurant.query.filter(Restaurant.offer is not None)
        elif (col == 'phone'):
            restaurant = Restaurant.query.filter(Restaurant.phone is not None)
        elif (col == 'has_reservation'):
            restaurant = Restaurant.query.filter(Restaurant.has_reservation != "0").limit(15).all()
        elif (col == 'has_parking'):
            restaurant = Restaurant.query.filter(Restaurant.has_parking != "0").limit(15).all()
        elif (col == 'has_wifi'):
            restaurant = Restaurant.query.filter(Restaurant.has_wifi != "0").limit(15).all()
        elif (col == 'has_bar'):
            restaurant = Restaurant.query.filter(Restaurant.has_bar != "0").limit(15).all()
        elif (col == 'has_terrace'):
            restaurant = Restaurant.query.filter(Restaurant.has_terrace != "0").limit(15).all()
        elif (col == 'has_delivery'):
            restaurant = Restaurant.query.filter(Restaurant.has_delivery != "0").limit(15).all()
        elif (col == 'has_cards'):
            restaurant = Restaurant.query.filter(Restaurant.has_cards != "0").limit(15).all()
        else:
            restaurant = Restaurant.query.filter(getattr(Restaurant, col).like("%" + key + "%")).limit(15).all()
    else:
        raise RuntimeError('Restaurant table doesn`t have column %s' % col)
    return jsonify(restaurants=[i.serialize for i in restaurant])


@app.route('/api/restaurants/search/nearby',methods=['GET'])
def nearby():
    lat = request.args['lat']
    lng = request.args['lng']
    restaurant=("SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(-122) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM Restaurant HAVING distance < 25 ORDER BY distance LIMIT 0 , 20")


    return jsonify(restaurants=[i.serialize for i in restaurant])



@app.route('/api/restaurants/add/',methods=['POST'])
@auth.login_required
def add_restaurant():
    geolocator = Nominatim()
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    name = request.args['name']
    addr1 = request.args['address1']
    addr2 = request.args['address2']
    menu = request.args['menu']
    if 'park' in request.args:
        park = request.args['park']
    else:
        park = None
    if 'offer' in request.args:
        offer = request.args['offer']
    else:
        offer = None
    if 'card' in request.args:
        card = request.args['card']
    else:
        card = None
    if 'wifi' in request.args:
        wifi = request.args['wifi']
    else:
        wifi = None
    if 'cost' in request.args:
        cost = request.args['cost']
    else:
        wifi = None
    if 'delivery' in request.args:
        delivery = request.args['delivery']
    else:
        delivery = None
    if 'reservation' in request.args:
        reservation = request.args['reservation']
    else:
        reservation = None
    if 'terrace' in request.args:
        terrace = request.args['terrace']
    else:
        terrace = None
    phone = request.args['phone']
    if 'lat' in request.args and 'lng' in request.args :
        lat = request.args['lat']
        lng = request.args['lng']
    else:
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        location = geolocator.geocode(addr1 +" "+ addr2)
        print(location.address)
        lat=location.latitude
        lng=location.longitude
        print(lat,lng)
    if 'file' in request.files:
        f = request.files['file']
        if f.filename == '':
            return jsonify({"file": "no name"})
        print("no name")
        if f and allowed_file(f.filename):
            print("i am here, final stage")
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], name + phone + filename))
            fname = name + phone + filename
            furl = url_for('rest_img', filename=name + phone + filename)
    else:
        fname=None
        furl=None
    restaurant = Restaurant(name=name,address1=addr1,address2=addr2,menu_type=menu,
                            phone=phone,has_delivery=delivery,has_parking=park,
                            has_cards=card,has_reservation=reservation,has_terrace=terrace,
                            has_wifi=wifi,offer=offer,cost=cost,lat=lat,lng=lng,
                            image_filename=fname,image_url=furl)
    db.session.add(restaurant)
    db.session.commit()
    return jsonify({'restaurant':{"id": restaurant.id}})


@app.route('/api/restaurants/update/', methods=['PUT'])
@auth.login_required
def update_restaurant():
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    id=  request.args['id']
    restaurant = Restaurant.query.filter_by(id=id,deleted=0).first()
    name= restaurant.name
    phone= restaurant.phone
    try:
        if 'menu' in request.args:
            restaurant.menu_type = request.args['menu']
        if 'cost' in request.args:
            restaurant.cost=request.args['cost']
        if 'addr1' in request.args:
            restaurant.address1 = request.args['addr1']
        if 'addr2' in request.args:
            restaurant.address2=request.args['addr2']
        if 'parking' in request.args:
            restaurant.has_parking = request.args['parking']
        if 'card' in request.args:
            restaurant.has_cards = request.args['card']
        if 'delivery' in request.args:
            restaurant.has_delivery = request.args['delivery']
        if 'terrace' in request.args:
            restaurant.has_terrace = request.args['terrace']
        if 'bar' in request.args:
            restaurant.has_bar = request.args['bar']
        if 'wifi' in request.args:
            restaurant.has_wifi = request.args['wifi']
        if 'reservation' in request.args:
            restaurant.has_reservation = request.args['reservation']
        if 'file' in request.files:
            f = request.files['file']
            if f.filename == '':
                return jsonify({"file":"no name"})
                print("no name")

            if f and allowed_file(f.filename):
                print("i am here, final stage")
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], name + phone + filename))
                print("saving filename")
                restaurant.image_filename = filename
                restaurant.image_url = url_for('rest_img', filename=name + phone+ filename)

        print("lets commit!")
        db.session.commit()
    except:
        print("Error")
        db.session.rollback()
        db.session.flush()
    return jsonify({'Done':"Committed"})




@app.route('/uploads/<filename>')
def rest_img(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
